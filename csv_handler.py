import csv

class CSVWriter:
    def __init__(self, path):
        self.path = path
        with open(self.path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["frame", "x1", "y1", "x2", "y2", "z", "is_speaking"])

    def append(self, row):
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
