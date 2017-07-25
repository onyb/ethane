import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Message, Button, Header, Container, Modal, Input, Label, Grid, Icon } from 'semantic-ui-react'

class CurrentTokenContainer extends Component {
  static propTypes = {
    token: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired,
  }
  state = { modalOpen: false, value: '' }

  handleOpen = () => this.setState({
    modalOpen: true,
  })

  handleClose = () => this.setState({
    modalOpen: false,
  })

  handleInputChange(value) {
    this.setState({
      value,
    })
  }

  validateInputValue() {
    if (this.state.value && isNaN(this.state.value)) {
      return <Label basic color="red" pointing="left">Not a valid amount.</Label>
    }
    else if (this.state.value && parseFloat(this.state.value) > this.props.user.balance) {
      return <Label basic color="red" pointing="left">Not enough balance.</Label>
    }
    else if (this.state.value && parseFloat(this.state.value) === 0.0) {
      return <Label basic color="red" pointing="left">Enter a non-zero amount.</Label>
    }

    return null;
  }

  render() {
    return (
      <Container textAlign="center">
        <Header>{this.props.token.name}</Header>
        <Modal
          trigger={<Button onClick={this.handleOpen} color="blue">GET {this.props.token.symbol}!</Button>}
          open={this.state.modalOpen}
          onClose={this.handleClose}
        >
          <Modal.Content>
            <Header textAlign="center">Buy {this.props.token.name} ({this.props.token.symbol}) with Ether (ETH)</Header>
            <Message
              warning
              icon="warning circle"
              header="You are about to make a proxy transaction!"
              content="A random wallet pre-loaded with some fake Ether has been assigned to your session. We hold the private key to the same, allowing us to make the transaction on your behalf."
            />
            <Grid columns={2}>
              <Grid.Row>
                <Grid.Column>
                  <Label>Your address: {this.props.user.address}</Label>
                </Grid.Column>
                <Grid.Column>
                  <Label>Contract address: {this.props.token.contract_address}</Label>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <Label>Your ETH balance: {this.props.user.balance}</Label>
                </Grid.Column>
                <Grid.Column>
                  <Label>1 {this.props.token.symbol} = {this.props.token.rate} ETH</Label>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <Input
                    placeholder="Enter ETH amount"
                    value={this.state.value}
                    onChange={e => this.handleInputChange(e.target.value)}
                  />
                  {this.validateInputValue()}
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Modal.Content>
          <Modal.Actions>
            <Button
              color="green"
              disabled={this.state.value === '' || this.validateInputValue() !== null}
              onClick={this.handleSubmit}
            >
              <Icon name="checkmark" /> Send Transaction
            </Button>
          </Modal.Actions>
        </Modal>
      </Container>
    )
  }
}

export default CurrentTokenContainer
