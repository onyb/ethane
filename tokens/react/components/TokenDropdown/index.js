import { Container, Dropdown } from 'semantic-ui-react'

const options = [
  { key: 'yolaw-$', text: 'Yolaw-$', value: 'yolaw-$' },
  { key: 'eos', text: 'EOS', value: 'eos' },
]

const TokenDropdown = () => (
  <Container textAlign="center">
    <Dropdown options={options} />
  </ Container>
)

export default TokenDropdown
