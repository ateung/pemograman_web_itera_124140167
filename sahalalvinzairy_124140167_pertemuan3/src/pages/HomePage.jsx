import { useState } from 'react'
import BookFilter from '../components/BookFilter.jsx'
import BookForm from '../components/BookForm.jsx'
import BookList from '../components/BookList.jsx'
import { useBooks } from '../context/useBooks.js'
import { useBookStats } from '../hooks/useBookStats.js'

function HomePage() {
  const { books, addBook, updateBook, deleteBook } = useBooks()
  const stats = useBookStats(books)
  const [status, setStatus] = useState('all')
  const [search, setSearch] = useState('')
  const [editingBook, setEditingBook] = useState(null)
  const [message, setMessage] = useState('')

  const visibleBooks = books.filter((book) => {
    const matchesStatus = status === 'all' || book.status === status
    const words = `${book.title} ${book.author}`.toLowerCase()
    const matchesSearch = words.includes(search.toLowerCase())
    return matchesStatus && matchesSearch
  })

  function handleSave(bookData) {
    if (editingBook) {
      updateBook({ ...editingBook, ...bookData })
      setMessage('Buku berhasil diperbarui.')
      setEditingBook(null)
    } else {
      addBook(bookData)
      setMessage('Buku berhasil ditambahkan.')
    }
  }

  function handleDelete(bookId) {
    const isConfirmed = window.confirm('Hapus buku ini dari daftar?')
    if (isConfirmed) {
      deleteBook(bookId)
      if (editingBook?.id === bookId) setEditingBook(null)
      setMessage('Buku berhasil dihapus.')
    }
  }

  return (
    <div className="home-page">
      <section className="page-heading">
        <div>
          <p className="small-heading">DAFTAR PRIBADI</p>
          <h1>Daftar buku saya</h1>
          <p>Catat buku yang sudah dimiliki, sedang dibaca, atau ingin dibeli.</p>
        </div>
        <div className="book-total"><strong>{stats.total}</strong><span> buku</span></div>
      </section>

      {message && <p className="success-message" role="status">{message}</p>}

      <div className="page-columns">
        <div className="list-column">
          <section className="panel list-panel">
            <h2>Buku saya</h2>
            <BookFilter
              status={status}
              search={search}
              onStatusChange={setStatus}
              onSearchChange={setSearch}
            />
            <BookList books={visibleBooks} onEdit={setEditingBook} onDelete={handleDelete} />
          </section>
        </div>
        <aside className="form-column">
          <BookForm
            key={editingBook?.id ?? 'new'}
            book={editingBook}
            onSave={handleSave}
            onCancel={() => setEditingBook(null)}
          />
          <section className="small-note">
            <h2>Catatan</h2>
            <p>Daftar buku tersimpan di browser ini, jadi tidak hilang saat halaman dimuat ulang.</p>
          </section>
        </aside>
      </div>
    </div>
  )
}

HomePage.propTypes = {}

export default HomePage
