# Multimedia Processing Backend

## 功能
- 图片 / 音频 / 视频的压缩与格式转换
- SQLite 记录任务信息
- FFmpeg 执行实际转码

## 本地运行

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

服务默认运行在 `http://localhost:5000`。

## 环境要求
- Python 3.11+
- FFmpeg（命令行可用）

## API 快速示例

```bash
curl -F "file=@../sample_data/sample_image.png" \
  -F "output_format=webp" \
  -F "quality=80" \
  http://localhost:5000/api/image
```
