import PropTypes from 'prop-types'
import { bookPropType } from '../propTypes.js'

const statusNames = {
  owned: 'Dimiliki',
  reading: 'Sedang dibaca',
  wishlist: 'Ingin dibeli',
}

function BookItem({ book, onEdit, onDelete }) {
  return (
    <li className="book-item">
      <div className="book-information">
        <h3>{book.title}</h3>
        <p>Penulis: {book.author}</p>
        <span className={`status-label status-${book.status}`}>{statusNames[book.status]}</span>
      </div>
      <div className="book-actions">
        <button type="button" className="button" onClick={() => onEdit(book)}>Edit</button>
        <button type="button" className="button button-delete" onClick={() => onDelete(book.id)}>Hapus</button>
      </div>
    </li>
  )
}

BookItem.propTypes = {
  book: bookPropType.isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
}

export default BookItem
