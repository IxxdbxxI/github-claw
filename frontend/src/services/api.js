const API_BASE = import.meta.env.VITE_API_BASE || ''

export const submitMedia = async (type, payload) => {
  const formData = new FormData()
  formData.append('file', payload.file)
  formData.append('output_format', payload.output_format)
  if (payload.quality !== undefined) {
    formData.append('quality', payload.quality)
  }
  if (payload.bitrate) {
    formData.append('bitrate', payload.bitrate)
  }
  if (payload.preset) {
    formData.append('preset', payload.preset)
  }

  const response = await fetch(`${API_BASE}/api/${type}`, {
    method: 'POST',
    body: formData,
  })
  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.error || '处理失败，请稍后再试。')
  }
  return data
}

export const resolveDownloadUrl = (path) => {
  if (!path) {
    return ''
  }
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  return API_BASE ? `${API_BASE}${path}` : path
}
