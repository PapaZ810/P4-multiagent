# distance.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

class ManhattanDistanceCalculator:
  def getDistance(self, pos1, pos2):
    return manhattanDistance(pos1, pos2)

class Calculator:
  """
  Your agent should create and store a distance calculator once at initialization time
  and call the getDistance function as necessary.  The remaining functions can be
  ignored.
  """
  def __init__(self, layout, default = 10000):
    """
    Initialize with DistanceCalculator(layout).  Changing default is unnecessary.
    """
    print("Calculating position distances...")
    self._distances = {}
    self.default = default
    self.calculateDistances(layout)
    print("done.")

  def getDistance(self, pos1, pos2):
    """
    The getDistance function is the only one you'll need after you create the object.
    """
    if self.isInt(pos1) and self.isInt(pos2):
      return self.getDistanceOnGrid(pos1, pos2)
    pos1Grids = self.getGrids2D(pos1)
    pos2Grids = self.getGrids2D(pos2)
    bestDistance = self.default
    for pos1Snap, snap1Distance in pos1Grids:
      for pos2Snap, snap2Distance in pos2Grids:
        gridDistance = self.getDistanceOnGrid(pos1Snap, pos2Snap)
        distance = gridDistance + snap1Distance + snap2Distance
        if bestDistance > distance:
          bestDistance = distance
    return bestDistance

  def getDistanceOnGrid(self, pos1, pos2):
    key = (pos1, pos2)
    if key in self._distances:
      return self._distances[key]
    return self.default

  def isInt(self, pos):
    x, y = pos
    return x == int(x) and y == int(y)


  def getGrids2D(self, pos):
    grids = []
    for x, xDistance in self.getGrids1D(pos[0]):
      for y, yDistance in self.getGrids1D(pos[1]):
        grids.append(((x, y), xDistance + yDistance))
    return grids

  def getGrids1D(self, x):
    intX = int(x)
    if x == int(x):
      return [(x, 0)]
    return [(intX, x-intX), (intX+1, intX+1-x)]

  def manhattanDistance(self, x, y ):
    return abs( x[0] - y[0] ) + abs( x[1] - y[1] )

  def calculateDistances(self, layout):
    allNodes = layout.walls.asList(False)
    remainingNodes = allNodes[:]
    for node in allNodes:
      self._distances[(node, node)] = 0.0
      for otherNode in allNodes:
        if self.manhattanDistance(node, otherNode) == 1.0:
          self._distances[(node, otherNode)] = 1.0
    while len(remainingNodes) > 0:
      node = remainingNodes.pop()
      for node1 in allNodes:
        dist1 = self.getDistanceOnGrid(node1, node)
        for node2 in allNodes:
          oldDist = self.getDistanceOnGrid(node1, node2)
          if dist1 > oldDist:
            continue
          dist2 = self.getDistanceOnGrid(node2, node)
          newDist = dist1 + dist2
          if newDist < oldDist:
            self._distances[(node1, node2)] = newDist
            self._distances[(node2, node1)] = newDist
