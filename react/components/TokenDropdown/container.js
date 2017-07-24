import { connect } from 'react-redux'

import { selectToken } from '../../redux/actions'
import TokenDropdown from './component'

const mapStateToProps = state => ({
  tokens: state.tokens,
  currentToken: state.currentToken,
})

const mapDispatchToProps = dispatch => ({
  onChange: (e, data) => {
    dispatch(selectToken(data.value))
  },
})


export default connect(mapStateToProps, mapDispatchToProps)(TokenDropdown)
