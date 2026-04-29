from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from db import create_job, fetch_job, init_db, update_job
from media import ProcessingError, process_audio, process_image, process_video

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"
OUTPUT_DIR = BASE_DIR / "storage" / "outputs"
DB_PATH = DATA_DIR / "app.db"

ALLOWED_FORMATS = {
    "image": {"jpg", "jpeg", "png", "webp"},
    "audio": {"mp3", "aac", "wav", "ogg"},
    "video": {"mp4", "webm", "mkv"},
}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
init_db(DB_PATH)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 500
CORS(app, resources={r"/api/*": {"origins": "*"}})


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_format(value: str | None) -> str:
    if not value:
        return ""
    return value.strip().lower()


def response_job(job_id: str, download_url: str | None = None):
    job = fetch_job(DB_PATH, job_id)
    payload = {"job": job, "download_url": download_url}
    return payload


@app.get("/api/health")
def health() -> tuple[dict, int]:
    return {"status": "ok", "timestamp": utc_now()}, 200


@app.post("/api/<media_type>")
def handle_media(media_type: str):
    if media_type not in ALLOWED_FORMATS:
        return jsonify({"error": "不支持的媒体类型。"}), 404

    upload = request.files.get("file")
    if not upload or upload.filename == "":
        return jsonify({"error": "请上传文件。"}), 400

    output_format = normalize_format(request.form.get("output_format"))
    if output_format not in ALLOWED_FORMATS[media_type]:
        return jsonify({"error": "不支持的输出格式。"}), 400

    job_id = str(uuid.uuid4())
    safe_name = secure_filename(upload.filename)
    suffix = Path(safe_name).suffix.lower() if safe_name else ""
    if not suffix:
        suffix = ".bin"
    input_path = UPLOAD_DIR / f"{job_id}{suffix}"
    upload.save(input_path)
    output_extension = "jpg" if output_format == "jpeg" else output_format
    output_path = OUTPUT_DIR / f"{job_id}.{output_extension}"

    options = {
        "output_format": output_format,
        "quality": request.form.get("quality"),
        "bitrate": request.form.get("bitrate"),
        "preset": request.form.get("preset"),
    }

    created_at = utc_now()
    create_job(
        DB_PATH,
        {
            "id": job_id,
            "type": media_type,
            "input_name": safe_name or upload.filename,
            "input_path": str(input_path),
            "input_size": input_path.stat().st_size if input_path.exists() else None,
            "output_format": output_format,
            "output_path": str(output_path),
            "output_size": None,
            "status": "processing",
            "options": options,
            "created_at": created_at,
            "updated_at": created_at,
            "error": None,
        },
    )

    try:
        if media_type == "image":
            process_image(input_path, output_path, output_format, options.get("quality"))
        elif media_type == "audio":
            process_audio(input_path, output_path, output_format, options.get("bitrate"))
        elif media_type == "video":
            process_video(
                input_path,
                output_path,
                output_format,
                options.get("quality"),
                options.get("preset"),
            )
    except ProcessingError as exc:
        update_job(DB_PATH, job_id, {"status": "failed", "error": str(exc)})
        return jsonify({"error": str(exc), **response_job(job_id)}), 500

    output_size = output_path.stat().st_size if output_path.exists() else None
    update_job(DB_PATH, job_id, {"status": "completed", "output_size": output_size})
    download_url = f"/api/jobs/{job_id}/download"
    return jsonify(response_job(job_id, download_url)), 200


@app.get("/api/jobs/<job_id>")
def job_detail(job_id: str):
    job = fetch_job(DB_PATH, job_id)
    if not job:
        return jsonify({"error": "任务不存在。"}), 404
    return jsonify({"job": job}), 200


@app.get("/api/jobs/<job_id>/download")
def job_download(job_id: str):
    job = fetch_job(DB_PATH, job_id)
    if not job or not job.get("output_path"):
        return jsonify({"error": "任务不存在或未生成输出。"}), 404
    output_path = Path(job["output_path"])
    if not output_path.exists():
        return jsonify({"error": "输出文件不存在。"}), 404
    filename = f"{job_id}.{job.get('output_format') or output_path.suffix.lstrip('.')}"
    return send_file(output_path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
