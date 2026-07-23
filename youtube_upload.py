#!/usr/bin/env python3
"""Authorize a YouTube channel and upload lesson videos as private videos."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]


def authorize(client_secret: Path, token_file: Path) -> Credentials:
    credentials = None
    if token_file.exists():
        credentials = Credentials.from_authorized_user_file(token_file, UPLOAD_SCOPE)
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secret), UPLOAD_SCOPE, redirect_uri="http://localhost"
        )
        authorization_url, _ = flow.authorization_url(
            access_type="offline", prompt="consent"
        )
        print("\n請在瀏覽器開啟以下 Google 授權網址：", flush=True)
        print(authorization_url, flush=True)
        print(
            "\n同意後瀏覽器可能顯示無法連線，這是正常的。"
            "請複製網址列中完整的 http://localhost/?code=... 網址並貼回來。",
            flush=True,
        )
        authorization_response = input("授權後的完整網址：").strip()
        # OAuthlib blocks plain HTTP by default. This exception is scoped to the
        # OAuth desktop-app loopback URI registered in the client JSON.
        if not authorization_response.startswith("http://localhost/"):
            raise ValueError("授權回呼網址必須以 http://localhost/ 開頭")
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(credentials.to_json(), encoding="utf-8")
        token_file.chmod(0o600)
    return credentials


def upload(youtube, spec: dict) -> str:
    path = Path(spec["file"])
    if not path.is_file():
        raise FileNotFoundError(path)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": spec["title"],
                "description": spec["description"],
                "tags": spec.get("tags", []),
                "categoryId": "27",
                "defaultLanguage": spec["language"],
            },
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(str(path), chunksize=8 * 1024 * 1024, resumable=True),
    )
    response = None
    while response is None:
        progress, response = request.next_chunk()
        if progress:
            print(f"上傳進度：{progress.progress() * 100:.1f}%", flush=True)
    return response["id"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-secret", type=Path, required=True)
    parser.add_argument("--token", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    specs = json.loads(args.manifest.read_text(encoding="utf-8"))
    credentials = authorize(args.client_secret, args.token)
    youtube = build("youtube", "v3", credentials=credentials, cache_discovery=False)
    for spec in specs:
        video_id = upload(youtube, spec)
        print(f"UPLOAD_OK {spec['language']} https://youtu.be/{video_id}", flush=True)


if __name__ == "__main__":
    main()
