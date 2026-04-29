<template>
  <section class="card">
    <h2>功能概览</h2>
    <p>上传多媒体文件，即可完成压缩和格式转换，并下载结果。</p>
    <ul class="list">
      <li>图片：JPG / PNG / WebP</li>
      <li>音频：MP3 / AAC / OGG / WAV</li>
      <li>视频：MP4 / WebM / MKV</li>
    </ul>
  </section>

  <section class="grid">
    <div class="card">
      <h3>图片处理</h3>
      <p>适合批量压缩、格式切换、图像体积优化。</p>
    </div>
    <div class="card">
      <h3>音频处理</h3>
      <p>支持设置码率，快速生成不同格式的音频文件。</p>
    </div>
    <div class="card">
      <h3>视频处理</h3>
      <p>支持设置压缩质量与预设，输出常用视频格式。</p>
    </div>
  </section>

  <section class="card">
    <h3>快速开始</h3>
    <ol class="list">
      <li>启动后端服务：<code>python backend/app.py</code></li>
      <li>启动前端：<code>npm run dev</code></li>
      <li>使用 <code>sample_data/</code> 内的示例文件进行测试</li>
    </ol>
  </section>
</template>
