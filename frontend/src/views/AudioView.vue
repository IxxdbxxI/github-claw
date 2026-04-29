<script setup>
import { computed, ref } from 'vue'
import { resolveDownloadUrl, submitMedia } from '@/services/api'

const file = ref(null)
const outputFormat = ref('mp3')
const bitrate = ref('128k')
const loading = ref(false)
const result = ref(null)
const error = ref('')

const onFileChange = (event) => {
  const [selected] = event.target.files
  file.value = selected || null
  result.value = null
  error.value = ''
}

const formatSize = (size) => {
  if (!size && size !== 0) {
    return '未知'
  }
  if (size < 1024) {
    return `${size} B`
  }
  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`
  }
  return `${(size / (1024 * 1024)).toFixed(2)} MB`
}

const downloadUrl = computed(() => resolveDownloadUrl(result.value?.download_url))

const onSubmit = async () => {
  if (!file.value) {
    error.value = '请先选择音频文件。'
    return
  }
  loading.value = true
  error.value = ''
  result.value = null
  try {
    result.value = await submitMedia('audio', {
      file: file.value,
      output_format: outputFormat.value,
      bitrate: bitrate.value,
    })
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="card">
    <h2>音频压缩与格式转换</h2>
    <p>支持 MP3 / AAC / OGG / WAV，可设置输出码率。</p>
    <form class="form-grid" @submit.prevent="onSubmit">
      <label class="field">
        <span>选择音频文件</span>
        <input type="file" accept="audio/*" @change="onFileChange" />
      </label>
      <div class="field-row">
        <label class="field">
          <span>输出格式</span>
          <select v-model="outputFormat">
            <option value="mp3">MP3</option>
            <option value="aac">AAC</option>
            <option value="ogg">OGG</option>
            <option value="wav">WAV</option>
          </select>
        </label>
        <label class="field">
          <span>码率</span>
          <select v-model="bitrate">
            <option value="64k">64k</option>
            <option value="96k">96k</option>
            <option value="128k">128k</option>
            <option value="192k">192k</option>
            <option value="256k">256k</option>
          </select>
        </label>
      </div>
      <button class="primary" type="submit" :disabled="loading || !file">
        {{ loading ? '处理中...' : '开始处理' }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </section>

  <section v-if="result" class="card">
    <h3>处理结果</h3>
    <ul class="list">
      <li>任务 ID：{{ result.job.id }}</li>
      <li>状态：{{ result.job.status }}</li>
      <li>输出格式：{{ result.job.output_format }}</li>
      <li>输出大小：{{ formatSize(result.job.output_size) }}</li>
    </ul>
    <a class="primary" :href="downloadUrl" download>下载结果</a>
  </section>
</template>
