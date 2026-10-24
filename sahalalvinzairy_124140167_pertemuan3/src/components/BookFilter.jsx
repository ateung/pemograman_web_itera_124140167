import PropTypes from 'prop-types'

function BookFilter({ status, search, onStatusChange, onSearchChange }) {
  return (
    <section className="filter-row" aria-label="Cari dan filter buku">
      <div className="form-field search-field">
        <label htmlFor="book-search">Cari judul atau penulis</label>
        <input
          id="book-search"
          type="search"
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Ketik kata kunci"
        />
      </div>
      <div className="form-field filter-field">
        <label htmlFor="status-filter">Filter status</label>
        <select id="status-filter" value={status} onChange={(event) => onStatusChange(event.target.value)}>
          <option value="all">Semua buku</option>
          <option value="owned">Dimiliki</option>
          <option value="reading">Sedang dibaca</option>
          <option value="wishlist">Ingin dibeli</option>
        </select>
      </div>
    </section>
  )
}

BookFilter.propTypes = {
  status: PropTypes.string.isRequired,
  search: PropTypes.string.isRequired,
  onStatusChange: PropTypes.func.isRequired,
  onSearchChange: PropTypes.func.isRequired,
}

export default BookFilter
