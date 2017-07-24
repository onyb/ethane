import { connect } from 'react-redux'

import DistributionContainer from './component'

const mapStateToProps = state => ({
  token: state.tokens[state.currentToken],
})


export default connect(mapStateToProps)(DistributionContainer)
