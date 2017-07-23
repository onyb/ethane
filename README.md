# ethane
A platform to create and participate in Initial Coin Offerings (ICO)

#### Running Ethane locally on Ubuntu

**Note:** Make sure you have Python 3.6 and the latest version of Node installed.

###### Launch the Ethereum test node

```sh
$ cd ethane
$ npm install
$ export PATH=`pwd`/node_modules/.bin:$PATH
$ testrpc
```
##### Launch the Django development server

(in a new tab)

```sh
$ virtualenv -p python3 ~/env
$ source ~/env/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ export PATH=`pwd`/node_modules/.bin:$PATH
$ python manage.py runserver
```


#### Tech Stack
###### Ethane Core
- [Ethereum](https://www.ethereum.org) as the blockchain app platform.
- [Solidity](https://solidity.readthedocs.io)  for writing smart-contracts.
- [OpenZepplin](https://openzeppelin.org) as a base for Solidity contracts, for security.
- [Truffle](http://truffleframework.com) for managing contract artifacts and deployment.
- [web3.js](https://github.com/ethereum/web3.js) - Javascript library to communicate with the Ethereum node through RPC calls.

###### Ethane front
- [React](https://facebook.github.io/react) for rendering the frontend
- [Redux](http://redux.js.org) - state management

##### Ethane backend
- Python/Django
- [PostgreSQL] as the database
