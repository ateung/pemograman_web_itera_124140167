import { useContext } from 'react'
import { BookContext } from './bookContext.js'

export function useBooks() {
  const context = useContext(BookContext)
  if (!context) {
    throw new Error('useBooks harus digunakan di dalam BookProvider')
  }
  return context
}
