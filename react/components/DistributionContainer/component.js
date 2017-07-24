import React from 'react'
import PropTypes from 'prop-types'
import { Container, Label, Grid, Header, Progress } from 'semantic-ui-react'

const DistributionContainer = ({ token }) => (
  <Container>
    <Header>{`${token.symbol} Token distribution`}</Header>
    <div>
      <Label>TOTAL DISTRIBUTED: {token.currentlyDistributed}</Label>
      <Progress
        percent={(100 * token.currentlyDistributed) / token.totalToDistribute}
        indicating label={`${token.currentlyDistributed}/${token.totalToDistribute}`}
      />
    </div>
    <Grid columns={2}>
      <Grid.Row>
        <Grid.Column>
          <Label>ETH rate: {token.rate}</Label>
        </Grid.Column>
        <Grid.Column>
          <Label>ETH received: {token.ethReceived}</Label>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column>
          <Label>Contract address: {token.contract_address}</Label>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  </Container>
)
DistributionContainer.propTypes = {
  token: PropTypes.object.isRequired,
}

export default DistributionContainer
