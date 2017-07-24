import { Grid } from 'semantic-ui-react'

import CurrentTokenContainer from './components/CurrentTokenContainer'
import DistributionContainer from './components/DistributionContainer'
import TokenDropdown from './components/TokenDropdown'

export default () => (
  <Grid columns={3}>
    <Grid.Row>
      <Grid.Column width={2}>
        <TokenDropdown />
      </Grid.Column>
      <Grid.Column width={3}>
        <CurrentTokenContainer />
      </Grid.Column>
      <Grid.Column width={5}>
        <DistributionContainer />
      </Grid.Column>
    </Grid.Row>
  </Grid>
)
