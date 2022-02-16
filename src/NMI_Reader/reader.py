import csv

from src.NMI_Reader.interval import Interval
from src.NMI_Reader.meter import Meter


class Reader:
    """For reading NMI data."""

    def __init__(self, filename):
        self.filename = filename
        self.meters = []

    def compartmentalise(self):
        initiated = False
        with open(self.filename, "r") as f:
            # TODO: handle multiple files.
            reader = csv.reader(f, delimiter=",")
            for i, line in enumerate(reader):
                match line[0]:
                    case '200':
                        # New Meter:
                        if initiated:
                            self.meters.append(meter)
                        else:
                            initiated = True
                        meter = Meter(line)

                    case '300':
                        # Add Interval to current Meter:
                        interval = Interval(line)
                        try:
                            meter.add_interval(interval)
                        except NameError as e:
                            print(e)

                    case '400':
                        # Add Error Interval to Meter
                        # TODO: Handle this.
                        pass

    def get_meters(self):
        return self.meters
