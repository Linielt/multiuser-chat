# About
A simple multi-user chat application to learn the python socket library.

## Requirements

You should have Python 3.3 to install and use virtualenv.

### Installing virtualenv
```
$ pip install virtualenv
```
### Creating the virtual environemnt
```python
# Put your current python version here. For this example, I will use 3.8
$ python3.8 -m venv multiuser-chat
```
### Activating the virtual environment
```
$ .\venv\Scripts\activate
```

## How to run project
To run the project, you will require a server to receive and send packets to connected clients
and clients that will see the messages broadcasted by the server.

### To start the server
```
# You can choose your own port number, for this example I chose 3490
$ python chat-server.py 3490
```
### To create clients
To create a client, start another terminal and run this command:
```
# If you are running this on your own computer the host will usually be localhost
$ python chat-client.py [nickname] [host] [port_number]
```

## References
- [Beej's Guide to Network Concepts](https://beej.us/guide/bgnet0/)
  - This is the main resource I read to learn low-level networking concepts and write python code to work with networks.
- [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
  - Article from official documentation to get a better understanding of what sockets are.