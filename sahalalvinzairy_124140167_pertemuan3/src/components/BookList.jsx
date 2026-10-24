import PropTypes from 'prop-types'
import { bookPropType } from '../propTypes.js'
import BookItem from './BookItem.jsx'

function BookList({ books, onEdit, onDelete }) {
  if (books.length === 0) {
    return (
      <div className="empty-message">
        <p>Belum ada buku yang cocok.</p>
        <p>Tambah buku baru atau ubah pencarian dan filter.</p>
      </div>
    )
  }

  return (
    <ul className="book-list">
      {books.map((book) => (
        <BookItem key={book.id} book={book} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </ul>
  )
}

BookList.propTypes = {
  books: PropTypes.arrayOf(bookPropType).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
}

export default BookList
