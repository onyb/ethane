import { Grid } from 'semantic-ui-react'

import CurrentTokenContainer from './components/CurrentTokenContainer'
import DistributionContainer from './components/DistributionContainer'

export default () => (
  <Grid columns={2}>
    <Grid.Row>
      <Grid.Column width={3}>
        <CurrentTokenContainer />
      </Grid.Column>
      <Grid.Column width={5}>
        <DistributionContainer />
      </Grid.Column>
    </Grid.Row>
  </Grid>
)
