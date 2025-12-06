import numpy as np
from collections import deque
from scipy.signal import medfilt

class SimpleCentroidTracker:
    def __init__(self, max_lost=10):
        self.nextObjectID = 0
        self.objects = {}
        self.lost = {}
        self.max_lost = max_lost
        self.history = {}

    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.lost[self.nextObjectID] = 0
        self.history[self.nextObjectID] = deque(maxlen=5)
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.lost[objectID]
        del self.history[objectID]

    def update(self, rects):
        if len(rects) == 0:
            for objectID in list(self.lost.keys()):
                self.lost[objectID] += 1
                if self.lost[objectID] > self.max_lost:
                    self.deregister(objectID)
            return self.objects

        input_centroids = np.zeros((len(rects), 2), dtype="int")

        for i, (x1, y1, x2, y2) in enumerate(rects):
            cX = int((x1 + x2) / 2)
            cY = int((y1 + y2) / 2)
            input_centroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i])
            return self.objects

        objectIDs = list(self.objects.keys())
        objectCentroids = list(self.objects.values())

        D = np.linalg.norm(
            np.array(objectCentroids)[:, None] - input_centroids[None, :],
            axis=2
        )

        rows = np.min(D, axis=1).argsort()
        cols = np.argmin(D, axis=1)[rows]

        usedCols = set()
        usedRows = set()

        for (row, col) in zip(rows, cols):
            if col in usedCols:
                continue

            objectID = objectIDs[row]
            self.objects[objectID] = input_centroids[col]
            self.lost[objectID] = 0
            self.history[objectID].append(input_centroids[col])

            usedCols.add(col)
            usedRows.add(row)

        unusedCols = set(range(0, D.shape[1])).difference(usedCols)
        for col in unusedCols:
            self.register(input_centroids[col])

        unusedRows = set(range(0, D.shape[0])).difference(usedRows)
        for row in unusedRows:
            objectID = objectIDs[row]
            self.lost[objectID] += 1
            if self.lost[objectID] > self.max_lost:
                self.deregister(objectID)

        return self.objects
