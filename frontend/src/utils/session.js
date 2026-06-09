export function getSessionId() {
  const match = document.cookie.match(/(?:^|;\s*)session_id=([^;]+)/)
  if (match) return match[1]
  const id = crypto.randomUUID()
  document.cookie = `session_id=${id}; path=/; SameSite=Lax; max-age=2592000`
  return id
}
