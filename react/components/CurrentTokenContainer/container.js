import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';

import CurrentTokenContainer from './component'

import { updateBalances } from '../../redux/actions'

const mapStateToProps = state => ({
  token: state.tokens[state.currentToken],
  user: state.user,
})

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
      { updateBalances },
      dispatch
    );
}


export default connect(mapStateToProps, mapDispatchToProps)(CurrentTokenContainer)
