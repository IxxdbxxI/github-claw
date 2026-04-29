<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div>
        <h1>多媒体处理平台</h1>
        <p>支持图片、音频、视频的压缩与格式转换</p>
      </div>
      <nav class="nav-links">
        <RouterLink to="/">概览</RouterLink>
        <RouterLink to="/image">图片</RouterLink>
        <RouterLink to="/audio">音频</RouterLink>
        <RouterLink to="/video">视频</RouterLink>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <footer class="app-footer">
      <span>API 默认代理 /api，可在 .env 中配置 VITE_API_BASE。</span>
    </footer>
  </div>
</template>
