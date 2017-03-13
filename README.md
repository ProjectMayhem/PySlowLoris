# PySlowLoris

Python Implementation of a SlowLoris DoS Tool

## The Slow Loris Attack

The [SlowLoris attack][wikipedia_slowloris] takes advantage of the way some versions of Apache and other smaller
webservers were written. These servers have a connection pool with a maximum amount of connections
that can be held simultaneously. In addition, many of these servers have either very long or nonexistent
timeouts for web requests. SlowLoris fills up this connection pool with fake requests and appends
useless data to these requests, while never terminating them. This prevents the server from accepting
any new legitimate requests from actual users.

The advantages of this style of attack are that it requires virtually no computing effort
to be effective. These servers can only handle 100-200 connections at one time, and requests
only need to be appended to about once every 10 seconds. This means that this attack can be
routed through Tor for anonymity, as well as launched from a cell phone.

The disadvantages of this attack are primarily that it only works on Apache 1x, 2x, dhpptd, and
some other minor servers. Servers like nginx are not vulnerable to this form of attack.

## Installation and Use

### Installation

#### Step 1 - Clone Repo

From a terminal or Git Bash, type the following:

```
$ git clone https://github.com/ProjectMayhem/PySlowLoris
```

#### Step 2 - Install Python

For Windows users it is recommended that you install Canopy (https://store.enthought.com/downloads/) and then
use the "Canopy Command Prompt" from here on out.

For Linux users Python usually comes pre-installed with most operating systems. Check to see if Python is installed
by running the following:

```
$ python --version
```

If not, then run one of these following commands (depending on your system):

Debian:

```
$ sudo apt-get install python
```

RedHat/Fedora/CentOS:

```
$ sudo yum install python
```

#### Step 3 - Change Directories

Either in terminal or in the Canopy Command Prompt, enter the following:

```
$ cd PySlowLoris/src
```

#### Step 4 - Run

Now we can invoke the ```main.py``` Python script, with any of the following syntax:

```
$ python main.py [IP]
```

```
$ python main.py [IP] [PORT]
```

```
$ python main.py [IP] [PORT] [CONNECTION_COUNT]
```

[wikipedia_slowloris]: https://en.wikipedia.org/wiki/Slowloris_(computer_security)