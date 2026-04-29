# 多媒体处理平台 (Multimedia Processing Platform)

前后端完整可运行示例，支持图片、音频、视频的压缩与格式转换。

## 项目结构

```
backend/       后端服务（Python + Flask + SQLite + FFmpeg）
frontend/      前端应用（Vue 多页面）
sample_data/   示例媒体文件
```

## 本地运行

### 1. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

默认地址：`http://localhost:5000`

> 需要提前安装 FFmpeg 并确保 `ffmpeg` 命令可用。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

默认地址：`http://localhost:5173`，已通过 Vite 代理 `/api` 到后端。

### 3. 示例数据

使用 `sample_data/` 下的文件进行测试：

- `sample_image.png`
- `sample_audio.wav`
- `sample_video.mp4`

## 功能说明

- **图片**：JPG / PNG / WebP 格式转换，质量可调
- **音频**：MP3 / AAC / OGG / WAV 格式转换，码率可选
- **视频**：MP4 / WebM / MKV 格式转换，质量与预设可调

## API 示例

```bash
curl -F "file=@sample_data/sample_image.png" \
  -F "output_format=webp" \
  -F "quality=80" \
  http://localhost:5000/api/image
```
