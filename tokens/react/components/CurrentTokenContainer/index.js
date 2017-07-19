import React, { Component } from 'react'
import { Button, Header, Container, Modal, Input, Label, Grid, Icon } from 'semantic-ui-react'

class CurrentTokenContainer extends Component {
  state = { modalOpen: false }

  handleOpen = () => this.setState({
    modalOpen: true,
  })

  handleClose = () => this.setState({
    modalOpen: false,
  })

  render() {
    return (
      <Container textAlign="center">
        <Header>Yolaw-$</Header>
        <Modal
          trigger={<Button onClick={this.handleOpen} color="blue">GET YL$!</Button>}
          open={this.state.modalOpen}
          onClose={this.handleClose}
        >
          <Modal.Content>
            <Header textAlign="center">Yolaw-$</Header>
            <Grid columns={2}>
              <Grid.Row>
                <Grid.Column>
                  <Label>Your adress: 0xza934t471b72ba2f1ccf0a70fczka712a5eecd8d</Label>
                </Grid.Column>
                <Grid.Column>
                  <Label>Contract adress: 0xcd234a471b72ba2f1ccf0a70fcaba648a5eecd8d</Label>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <Label>Your ETH balance: 1.0</Label>
                </Grid.Column>
                <Grid.Column>
                  <Label>ETH rate: 0.06</Label>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <Input placeholder="Enter ETH amount" />
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Modal.Content>
          <Modal.Actions>
            <Button color="green" onClick={this.handleClose}>
              <Icon name="checkmark" /> Purchase
            </Button>
          </Modal.Actions>
        </Modal>
      </Container>
    )
  }
}

export default CurrentTokenContainer
