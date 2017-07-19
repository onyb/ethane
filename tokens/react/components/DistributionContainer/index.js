import { Container, Label, Grid, Header, Progress } from 'semantic-ui-react'

const DistributionContainer = () => (
  <Container>
    <Header>YL$ Token distribution</Header>
    <div>
      <Label>TOTAL DISTRIBUTED: 42000</Label>
      <Progress percent={25} indicating label="42000/240000" />
    </div>
    <Grid columns={2}>
      <Grid.Row>
        <Grid.Column>
          <Label>ETH rate: 0.06</Label>
        </Grid.Column>
        <Grid.Column>
          <Label>ETH received: 77</Label>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column>
          <Label>Contact adress: 0xcd234a471b72ba2f1ccf0a70fcaba648a5eecd8d</Label>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  </Container>
)

export default DistributionContainer
