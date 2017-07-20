import React from 'react'
import PropTypes from 'prop-types'
import { Container, Dropdown } from 'semantic-ui-react'

const TokenDropdown = ({ tokens, currentToken, onChange }) => {
  const options = Object.keys(tokens).map(k => ({ key: k, text: tokens[k].name, value: k }))
  return (
    <Container textAlign="center">
      <Dropdown options={options} onChange={onChange} />
    </ Container>
  )
}
TokenDropdown.propTypes = {
  tokens: PropTypes.object.isRequired,
  currentToken: PropTypes.number.isRequired,
  onChange: PropTypes.func.isRequired,
}


export default TokenDropdown
