import { connect } from 'react-redux'

import CurrentTokenContainer from './component'


const mapStateToProps = state => ({
  token: state.tokens[state.currentToken],
  user: state.user,
})


export default connect(mapStateToProps)(CurrentTokenContainer)
