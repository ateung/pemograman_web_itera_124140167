import { useState } from 'react'
import PropTypes from 'prop-types'
import { bookPropType } from '../propTypes.js'

const emptyForm = {
  title: '',
  author: '',
  status: 'owned',
}

function BookForm({ book, onSave, onCancel }) {
  const [formData, setFormData] = useState(() => book ? {
    title: book.title,
    author: book.author,
    status: book.status,
  } : emptyForm)
  const [errors, setErrors] = useState({})

  function handleChange(event) {
    const { name, value } = event.target
    setFormData({ ...formData, [name]: value })
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' })
    }
  }

  function handleSubmit(event) {
    event.preventDefault()
    const newErrors = {}

    if (!formData.title.trim()) newErrors.title = 'Judul buku wajib diisi.'
    if (!formData.author.trim()) newErrors.author = 'Nama penulis wajib diisi.'

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    onSave({
      ...formData,
      title: formData.title.trim(),
      author: formData.author.trim(),
      ...(book ? { id: book.id } : {}),
    })

    setFormData(emptyForm)
    setErrors({})
  }

  return (
    <section className="panel form-panel">
      <h2>{book ? 'Edit buku' : 'Tambah buku'}</h2>
      <form onSubmit={handleSubmit} noValidate>
        <div className="form-field">
          <label htmlFor="book-title">Judul buku</label>
          <input
            id="book-title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Contoh: Laskar Pelangi"
            aria-invalid={Boolean(errors.title)}
            aria-describedby={errors.title ? 'title-error' : undefined}
          />
          {errors.title && <small className="field-error" id="title-error">{errors.title}</small>}
        </div>

        <div className="form-field">
          <label htmlFor="book-author">Penulis</label>
          <input
            id="book-author"
            name="author"
            value={formData.author}
            onChange={handleChange}
            placeholder="Contoh: Andrea Hirata"
            aria-invalid={Boolean(errors.author)}
            aria-describedby={errors.author ? 'author-error' : undefined}
          />
          {errors.author && <small className="field-error" id="author-error">{errors.author}</small>}
        </div>

        <div className="form-field">
          <label htmlFor="book-status">Status buku</label>
          <select id="book-status" name="status" value={formData.status} onChange={handleChange}>
            <option value="owned">Dimiliki</option>
            <option value="reading">Sedang dibaca</option>
            <option value="wishlist">Ingin dibeli</option>
          </select>
        </div>

        <div className="form-buttons">
          <button type="submit" className="button button-primary">
            {book ? 'Simpan perubahan' : 'Tambah buku'}
          </button>
          {book && <button type="button" className="button" onClick={onCancel}>Batal</button>}
        </div>
      </form>
    </section>
  )
}

BookForm.propTypes = {
  book: bookPropType,
  onSave: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
}

export default BookForm
