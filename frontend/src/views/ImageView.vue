<script setup>
import { computed, ref } from 'vue'
import { resolveDownloadUrl, submitMedia } from '@/services/api'

const file = ref(null)
const outputFormat = ref('jpg')
const quality = ref(80)
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
    error.value = '请先选择图片文件。'
    return
  }
  loading.value = true
  error.value = ''
  result.value = null
  try {
    result.value = await submitMedia('image', {
      file: file.value,
      output_format: outputFormat.value,
      quality: quality.value,
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
    <h2>图片压缩与格式转换</h2>
    <p>支持 JPG / PNG / WebP，可通过质量调节压缩体积。</p>
    <form class="form-grid" @submit.prevent="onSubmit">
      <label class="field">
        <span>选择图片文件</span>
        <input type="file" accept="image/*" @change="onFileChange" />
      </label>
      <div class="field-row">
        <label class="field">
          <span>输出格式</span>
          <select v-model="outputFormat">
            <option value="jpg">JPG</option>
            <option value="png">PNG</option>
            <option value="webp">WebP</option>
          </select>
        </label>
        <label class="field">
          <span>质量：{{ quality }}</span>
          <input v-model="quality" type="range" min="10" max="100" step="5" />
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
