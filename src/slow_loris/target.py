"""This module implements a SlowLoris target."""

class TargetInfo:
    """SlowLoris target."""

    def __init__(self, host, port, count):
        self.host = host
        self.port = port
        self.count = count
        self.connections = []
        self.reconnections = 0
        self.latest_latency_list = []
        self.dropped_connections = 0
        self.rejected_connections = 0
        self.rejected_initial_connections = 0

    def get_latency(self):
        """Gets the latency in milliseconds."""
        latency = 0
        element_count = len(self.latest_latency_list)
        if element_count == 0:
            return None
        for value in self.latest_latency_list:
            latency += value
        return latency / element_count
