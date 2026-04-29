<script setup>
import { computed, ref } from 'vue'
import { resolveDownloadUrl, submitMedia } from '@/services/api'

const file = ref(null)
const outputFormat = ref('mp4')
const quality = ref(80)
const preset = ref('medium')
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
    error.value = '请先选择视频文件。'
    return
  }
  loading.value = true
  error.value = ''
  result.value = null
  try {
    result.value = await submitMedia('video', {
      file: file.value,
      output_format: outputFormat.value,
      quality: quality.value,
      preset: preset.value,
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
    <h2>视频压缩与格式转换</h2>
    <p>支持 MP4 / WebM / MKV，可调整压缩质量与预设。</p>
    <form class="form-grid" @submit.prevent="onSubmit">
      <label class="field">
        <span>选择视频文件</span>
        <input type="file" accept="video/*" @change="onFileChange" />
      </label>
      <div class="field-row">
        <label class="field">
          <span>输出格式</span>
          <select v-model="outputFormat">
            <option value="mp4">MP4</option>
            <option value="webm">WebM</option>
            <option value="mkv">MKV</option>
          </select>
        </label>
        <label class="field">
          <span>预设</span>
          <select v-model="preset">
            <option value="ultrafast">ultrafast</option>
            <option value="fast">fast</option>
            <option value="medium">medium</option>
            <option value="slow">slow</option>
          </select>
        </label>
      </div>
      <label class="field">
        <span>质量：{{ quality }}</span>
        <input v-model="quality" type="range" min="10" max="100" step="5" />
      </label>
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
