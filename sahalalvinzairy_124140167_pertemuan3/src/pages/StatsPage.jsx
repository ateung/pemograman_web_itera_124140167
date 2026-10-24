import StatCard from '../components/StatCard.jsx'
import { useBooks } from '../context/useBooks.js'
import { useBookStats } from '../hooks/useBookStats.js'

function StatsPage() {
  const { books } = useBooks()
  const stats = useBookStats(books)

  return (
    <section className="stats-page panel">
      <p className="small-heading">RINGKASAN</p>
      <h1>Statistik buku</h1>
      <p className="stats-intro">Ringkasan sederhana dari daftar buku yang kamu simpan.</p>
      <div className="stats-grid">
        <StatCard label="Semua buku" count={stats.total} />
        <StatCard label="Dimiliki" count={stats.owned} />
        <StatCard label="Sedang dibaca" count={stats.reading} />
        <StatCard label="Ingin dibeli" count={stats.wishlist} />
      </div>
      {books.length === 0 && <p className="empty-message">Belum ada data. Tambahkan buku dari halaman Daftar Buku.</p>}
    </section>
  )
}

StatsPage.propTypes = {}

export default StatsPage
