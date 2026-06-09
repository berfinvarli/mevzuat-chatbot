import { apiClient } from './apiClient'

export async function fetchCmsValue(key) {
  const res = await apiClient.get(`/cms/${encodeURIComponent(key)}`)
  const data = await res.json()
  return data.value
}
