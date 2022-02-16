from datetime import datetime


class Interval:
    """Represent a day of meter data."""

    def __init__(self, raw_data):
        self.date = datetime.strptime(raw_data[1], '%Y%m%d')
        self.values = [float(i) for i in raw_data[2:-6]]
        self.interval_period = (24 * 60) / len(self.values)  # Minutes/Day / # Intervals = Interval Period (min)
        self.last_updated = datetime.strptime(raw_data[-3], '%Y%m%d%H%M%S')

    def get_value(self, period=None):
        if period is None:
            return self.values
        elif period < self.interval_period:
            # Can't do this (yet?)
            # TODO: this.
            print("WARNING: desired period is smaller than the original period.")
            return
        else:
            points_to_sum = int(period / self.interval_period)
            new_values = []
            for i in range(0, points_to_sum):
                start = i * points_to_sum
                end = (i + 1) * points_to_sum - 1
                new_values.append(sum(self.values[start:end]))

            return new_values
