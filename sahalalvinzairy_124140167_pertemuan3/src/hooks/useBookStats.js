export function useBookStats(books) {
  const safeBooks = Array.isArray(books) ? books : []

  return {
    total: safeBooks.length,
    owned: safeBooks.filter((book) => book.status === 'owned').length,
    reading: safeBooks.filter((book) => book.status === 'reading').length,
    wishlist: safeBooks.filter((book) => book.status === 'wishlist').length,
  }
}
