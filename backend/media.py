from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


class ProcessingError(RuntimeError):
    pass


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise ProcessingError("ffmpeg 未安装或不可用，请先安装后再试。")


def clamp_int(value: str | None, minimum: int, maximum: int, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


ALLOWED_FLAGS = {
    "-q:v",
    "-compression_level",
    "-quality",
    "-c:a",
    "-b:a",
    "-c:v",
    "-preset",
    "-crf",
    "-b:v",
    "-movflags",
}

ALLOWED_VALUE_PATTERN = re.compile(r"^[a-zA-Z0-9_+.-]+$")


def validate_args(args: list[str]) -> None:
    for item in args:
        if item.startswith("-"):
            if item not in ALLOWED_FLAGS:
                raise ProcessingError("检测到非法的转码参数。")
        else:
            if not ALLOWED_VALUE_PATTERN.match(item):
                raise ProcessingError("检测到非法的转码参数值。")


def run_ffmpeg(input_path: Path, output_path: Path, extra_args: list[str]) -> None:
    ensure_ffmpeg()
    validate_args(extra_args)
    command = ["ffmpeg", "-y", "-i", str(input_path), *extra_args, str(output_path)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or "ffmpeg 处理失败。"
        raise ProcessingError(detail)


def process_image(input_path: Path, output_path: Path, output_format: str, quality: str | None) -> None:
    normalized = output_format.lower()
    quality_value = clamp_int(quality, 10, 100, 80)
    if normalized in {"jpg", "jpeg"}:
        qv = max(2, min(31, int((100 - quality_value) / 3) + 2))
        args = ["-q:v", str(qv)]
    elif normalized == "png":
        compression = max(0, min(9, int((100 - quality_value) / 100 * 9)))
        args = ["-compression_level", str(compression)]
    elif normalized == "webp":
        args = ["-quality", str(quality_value)]
    else:
        raise ProcessingError("不支持的图片输出格式。")
    run_ffmpeg(input_path, output_path, args)


def process_audio(input_path: Path, output_path: Path, output_format: str, bitrate: str | None) -> None:
    normalized = output_format.lower()
    bitrate_value = bitrate if bitrate in {"64k", "96k", "128k", "192k", "256k"} else "128k"
    if normalized == "mp3":
        args = ["-c:a", "libmp3lame", "-b:a", bitrate_value]
    elif normalized == "aac":
        args = ["-c:a", "aac", "-b:a", bitrate_value]
    elif normalized == "ogg":
        args = ["-c:a", "libvorbis", "-b:a", bitrate_value]
    elif normalized == "wav":
        args = ["-c:a", "pcm_s16le"]
    else:
        raise ProcessingError("不支持的音频输出格式。")
    run_ffmpeg(input_path, output_path, args)


def process_video(
    input_path: Path,
    output_path: Path,
    output_format: str,
    quality: str | None,
    preset: str | None,
) -> None:
    normalized = output_format.lower()
    quality_value = clamp_int(quality, 10, 100, 80)
    crf = max(18, min(35, int((100 - quality_value) / 100 * 17) + 18))
    preset_value = preset if preset in {"ultrafast", "fast", "medium", "slow"} else "medium"
    if normalized == "mp4":
        args = [
            "-c:v",
            "libx264",
            "-preset",
            preset_value,
            "-crf",
            str(crf),
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
        ]
    elif normalized == "webm":
        args = [
            "-c:v",
            "libvpx-vp9",
            "-crf",
            str(crf),
            "-b:v",
            "0",
            "-c:a",
            "libopus",
        ]
    elif normalized == "mkv":
        args = [
            "-c:v",
            "libx264",
            "-preset",
            preset_value,
            "-crf",
            str(crf),
            "-c:a",
            "aac",
            "-b:a",
            "128k",
        ]
    else:
        raise ProcessingError("不支持的视频输出格式。")
    run_ffmpeg(input_path, output_path, args)
