import PropTypes from 'prop-types'

export const bookPropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  author: PropTypes.string.isRequired,
  status: PropTypes.oneOf(['owned', 'reading', 'wishlist']).isRequired,
})
