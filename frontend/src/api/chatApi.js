import { apiClient } from './apiClient'

export async function fetchHistory() {
  const res = await apiClient.get('/history')
  return res.json()
}

export async function streamChat(messages, signal) {
  return apiClient.post('/chat', { messages }, { signal })
}
