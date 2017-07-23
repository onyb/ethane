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
- [Solidity](https://solidity.readthedocs.io) for writing the smart contracts.
- [OpenZepplin](https://openzeppelin.org) as a secure base for Ethane contracts.
- [Truffle](http://truffleframework.com) for compiling and deploying Solidity contracts.


###### Ethane front
- [React](https://facebook.github.io/react)
