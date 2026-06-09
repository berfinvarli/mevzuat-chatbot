import { useState, useEffect } from 'react'
import { fetchCmsValue } from '../api/cmsApi'

export function useCmsValue(key, fallback) {
  const [value, setValue] = useState(fallback)

  useEffect(() => {
    let active = true
    fetchCmsValue(key)
      .then((v) => {
        if (active && v != null) setValue(v)
      })
      .catch(() => {})
    return () => {
      active = false
    }
  }, [key])

  return value
}
