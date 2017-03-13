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

## Usage

| Mode                       | Syntax                                    |
|----------------------------|-------------------------------------------|
| Single target              | `main.py <HOST> [PORT] [NUM_CONNECTIONS]` |
| Multiple targets           | `main.py <FILE>`                          |
| File format (one per line) | `<HOST> [PORT] [NUM_CONNECTIONS]`         |

### Running

For Linux/macOS/WSL users:

1. `$ git clone https://github.com/ProjectMayhem/PySlowLoris.git`
2. `$ cd PySlowLoris`
3. `$ python src/main.py <HOST> [PORT] [NUM_CONNECTIONS]`

For Windows users:

1. Open an instance of the command-line processor (`cmd.exe`)
2. `> git clone https://github.com/ProjectMayhem/PySlowLoris.git`
3. `> cd PySlowLoris`
4. `> python src\main.py <HOST> [PORT] [NUM_CONNECTIONS]`

### Extra

Installing Git and Python on Windows:

1. Download and install [Git for Windows][git_scm]
2. Download and install [Python 2][py2_win] or [Python 3][py3_win]<br>
3. Restart or log out and in again to apply `PATH` changes


[wikipedia_slowloris]: https://en.wikipedia.org/wiki/Slowloris_(computer_security)
[py2_win]: https://www.python.org/downloads/release/python-2713/
[py3_win]: https://www.python.org/downloads/release/python-360/
[git_scm]: https://git-for-windows.github.io/
