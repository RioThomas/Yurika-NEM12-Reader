
class Meter:
    """Represent a unique meter."""

    def __init__(self, header):
        self.NMI_reference = header[1]
        self.NMI_suffix = header[3]
        self.meter_number = header[6]
        self.unit = header[7]
        self.time_interval = header[8]

        self.intervals = []

    def add_interval(self, interval):
        self.intervals.append(interval)
