import PropTypes from 'prop-types'
import { useLocalStorage } from '../hooks/useLocalStorage.js'
import { BookContext } from './bookContext.js'

export function BookProvider({ children }) {
  const [savedBooks, setSavedBooks] = useLocalStorage('rak-buku-saya', [])
  const books = Array.isArray(savedBooks) ? savedBooks : []

  function addBook(bookData) {
    const newBook = {
      ...bookData,
      id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    }
    setSavedBooks((currentBooks) => [...(Array.isArray(currentBooks) ? currentBooks : []), newBook])
  }

  function updateBook(updatedBook) {
    setSavedBooks((currentBooks) =>
      currentBooks.map((book) => (book.id === updatedBook.id ? updatedBook : book)),
    )
  }

  function deleteBook(bookId) {
    setSavedBooks((currentBooks) => currentBooks.filter((book) => book.id !== bookId))
  }

  const contextValue = { books, addBook, updateBook, deleteBook }

  return <BookContext.Provider value={contextValue}>{children}</BookContext.Provider>
}

BookProvider.propTypes = {
  children: PropTypes.node.isRequired,
}
