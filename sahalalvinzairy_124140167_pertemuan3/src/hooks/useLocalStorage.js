import { useEffect, useState } from 'react'

// Membaca data sekali saat aplikasi dibuka, lalu menyimpannya setiap ada perubahan.
export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const savedValue = window.localStorage.getItem(key)
      return savedValue ? JSON.parse(savedValue) : initialValue
    } catch (error) {
      console.warn('Data buku tidak dapat dibaca:', error)
      return initialValue
    }
  })

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.warn('Data buku tidak dapat disimpan:', error)
    }
  }, [key, value])

  return [value, setValue]
}
