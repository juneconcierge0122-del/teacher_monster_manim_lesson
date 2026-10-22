"""Re-authorize the YouTube upload token, in two stages.

    python youtube_reauth.py url
    python youtube_reauth.py token 'http://localhost/?state=...&code=...'

The refresh token in `.secrets/youtube_token.json` dies every 7 days, because
the OAuth app's publishing status in the Google Cloud Console is still
"testing". Until someone switches that consent screen to production, this has
to be run by hand each time, so it lives in the repo instead of being rewritten
from scratch on every expiry (it has been, twice).

Two things make this fail if they are done the obvious way:

  * `flow.code_verifier` and `state` have to survive to the second stage, which
    is a new process. Without them the exchange is refused, because the library
    generates a fresh PKCE verifier per Flow object and the one the user's
    browser just committed to is the first stage's.

  * The exchange must be `flow.fetch_token(code=...)`, not
    `fetch_token(authorization_response=<the whole pasted URL>)`. The redirect
    is plain http, so oauthlib raises InsecureTransportError: OAuth 2 MUST
    utilize https. Passing the code alone skips that check, with no need for
    OAUTHLIB_INSECURE_TRANSPORT=1.

A successful refresh does not extend the refresh token's own 7-day life, so
testing before a render says nothing about whether the upload an hour later
will work. Test again immediately before uploading.

The token this writes can upload and nothing else -- it cannot delete a video.
"""
import json
import pathlib
import stat
import sys
import urllib.parse

from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = pathlib.Path(__file__).resolve().parent
CLIENT = ROOT / ".secrets/youtube_client_secret.json"
TOKEN = ROOT / ".secrets/youtube_token.json"
PENDING = ROOT / ".secrets/youtube_reauth_pending.json"
SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
REDIRECT = "http://localhost"


def private(path):
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def stage_url():
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT), SCOPE,
                                                     redirect_uri=REDIRECT)
    url, state = flow.authorization_url(access_type="offline", prompt="consent")
    PENDING.write_text(json.dumps({"state": state, "code_verifier": flow.code_verifier}))
    private(PENDING)
    print(url)


def stage_token(pasted):
    if not PENDING.exists():
        sys.exit("no pending re-authorization: run `url` first")
    saved = json.loads(PENDING.read_text())
    # the user may paste the whole redirect URL or just the code
    code = pasted.strip()
    if "code=" in code:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(code).query)
        if "error" in q:
            sys.exit(f"the consent screen returned an error: {q['error'][0]}")
        if q.get("state", [None])[0] != saved["state"]:
            sys.exit("state does not match the pending request: start again with `url`")
        code = q["code"][0]
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT), SCOPE,
                                                     redirect_uri=REDIRECT,
                                                     state=saved["state"])
    flow.code_verifier = saved["code_verifier"]
    flow.fetch_token(code=code)          # not authorization_response: see above
    TOKEN.write_text(flow.credentials.to_json())
    private(TOKEN)
    PENDING.unlink()
    print("token written, expiry", flow.credentials.expiry)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "url":
        stage_url()
    elif len(sys.argv) >= 3 and sys.argv[1] == "token":
        stage_token(sys.argv[2])
    else:
        sys.exit(__doc__.split("\n\n")[1].strip())
