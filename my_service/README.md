# Teaching Monster

AI-powered educational video generation pipeline using Gemini, Manim, and edge-tts.

## Pipeline Architecture

```
Request → Gemini API → Transcript + Manim Code
       → Manim CLI → Video Segments
       → edge-tts → Audio + SRT
       → MoviePy → Final Video
```

## Folder Structure

```
src/
├── gemini_client.py       # Gemini API wrapper
├── content_generator.py   # Generates transcript + Manim code
├── manim_renderer.py     # Renders Manim code to video
├── server.py             # FastAPI REST API
├── config_schema.py      # Configuration schema
└── tts/
    └── tts.py            # edge-tts for audio + SRT

scripts/
└── T2V_pipeline.py       # Pipeline orchestration

tests/
├── test_gemini_client.py
├── test_manim_renderer.py
└── test_tts.py

config/
└── default.yaml          # Configuration file
```

## APIs Used

| Service | Purpose |
|---------|---------|
| Gemini 2.5 Pro | Content generation (transcript + Manim code) |
| edge-tts | Text-to-speech audio + SRT subtitles |
| Manim CLI | Animation rendering |
| MoviePy | Video compositing |

## Prerequisites

- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/welcome)
- **Python 3.10+** (the code uses `dict | None`-style typing that requires 3.10)
- **FFmpeg**: Required by MoviePy/Manim for video processing
- **LaTeX** (`texlive` + extras): Required by Manim to render math text. See `Dockerfile` for the exact apt packages, or run via Docker to skip installing these yourself.

## Environment Setup

```bash
# create an isolated env (conda example; venv works too)
conda create -n teacher-monster python=3.10 -y
conda activate teacher-monster

pip install -r requirements.txt   # now includes manim==0.19.1
```

### API key

The app reads `GEMINI_API_KEY` from the environment. `src/config_schema.py` loads it via `python-dotenv` from **`config/.env`** (not the project-root `.env`), so either:

```bash
mkdir -p config
echo "GEMINI_API_KEY=your_real_key_here" > config/.env
```

or export it directly in your shell/container: `export GEMINI_API_KEY=your_real_key_here`.

Do **not** put the key in `config/default.yaml` — leave `llm.api_key` as `""` and let it fall back to the env var (this is how `LLMConfig.inject_gemini_api_key` in `src/config_schema.py` resolves it).

## Running Tests

```bash
pytest tests/ -v
```
All 21 tests pass out of the box (2 are skipped — `test_generate` and `test_generate_with_custom_params` in `tests/test_gemini_client.py` are marked `@pytest.mark.skip(reason="Requires mock setup for google.genai")`, i.e. not yet implemented, not an env issue).

## Running the Pipeline

### CLI
```bash
python -m scripts.T2V_pipeline \
  -r "Explain quantum entanglement" \
  -p "Enthusiastic science teacher"
```

### API Server
```bash
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

Verified working: the server boots, `/health` returns `{"status":"healthy","pipeline_loaded":true}`, and `/v1/video/generate` correctly routes through Gemini → Manim → edge-tts → MoviePy (confirmed with a smoke-test request; it fails cleanly on an invalid key rather than crashing).

**Quick connectivity test without burning API quota** — send header `X-Dry-Run: true` and the endpoint short-circuits with a stub response:
```bash
curl -X POST http://localhost:8000/v1/video/generate \
  -H "Content-Type: application/json" \
  -H "X-Dry-Run: true" \
  -d '{"request_id":"test-001","course_requirement":"x","student_persona":"x"}'
```

### Real API Request
```bash
curl -X POST http://localhost:8000/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "test-001",
    "course_requirement": "Explain quantum entanglement",
    "student_persona": "Curious undergraduate physics student"
  }'
```
Response contains `video_url` / `subtitle_url` pointing at:
- `GET /v1/files/{request_id}/video`
- `GET /v1/files/{request_id}/subtitle`

### Docker
```bash
docker build -t teaching-monster .
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your_real_key_here \
  -e BASE_URL=http://localhost:8080 \
  teaching-monster
```
The `Dockerfile` installs ffmpeg/cairo/pango/texlive at the system level; `requirements.txt` (including `manim`) is installed on top, so no extra manual steps are needed inside the container.

## Configuration

Edit `config/default.yaml` (leave `api_key` empty — see [API key](#api-key) above):
```yaml
llm:
  provider: gemini
  default_model: gemini-2.5-pro
  default_temperature: 0.7
  default_max_tokens: 8192
  api_key: ""

output:
  tmp_dir: ./tmp/
  final_video_dir: ./output
```