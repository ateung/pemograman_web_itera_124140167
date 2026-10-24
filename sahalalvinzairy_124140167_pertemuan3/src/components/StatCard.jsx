import PropTypes from 'prop-types'

function StatCard({ label, count }) {
  return (
    <article className="stat-card">
      <p>{label}</p>
      <strong>{count}</strong>
    </article>
  )
}

StatCard.propTypes = {
  label: PropTypes.string.isRequired,
  count: PropTypes.number.isRequired,
}

export default StatCard
