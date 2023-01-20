import numpy as np

class Model:
    def __init__(self, nodes, paths, demands):
      self._nodes = nodes
      self._paths = sorted(paths, key=lambda path: path._distance, reverse=True)
      self._demands = demands
      
      self.createPathMap()
    

    def getDemands(self):
      return self._demands

    
    def createPathMap(self):
      self.pathMap = {}
      print("Generating all path maps for demands")
      for demand in self._demands:
        self.pathMap[demand.source] = self.findAllPaths(demand.source)
      print("Done")

    
    def findAllPaths(self, start):
      # using Dijkstra algorithm
      visited = []
      unvisited = self._nodes.copy()
      distances = {}
      for unvisitedNode in unvisited:
        distances[unvisitedNode.name] = (np.inf, "")
      distances[start] = (0, start)
      
      while len(unvisited) != len(visited):
        distances_without_visited = {k: distances[k] for k in distances.keys() - visited}
        cur_node = min(distances_without_visited, key=lambda node: distances_without_visited.get(node))
        for path in [path for path in self._paths if cur_node == path._source]:
          if distances[cur_node][0] + path._distance < distances[path._target][0]:
            distances[path._target] = (distances[cur_node][0] + path._distance, cur_node)
        visited.append(cur_node)
      
      return distances
    
    
    def getShortestPath(self, source, target):
        shortest_path = [target]
        start = target
        while source not in shortest_path:
          start = self.pathMap[source][start][1]
          shortest_path.append(start)
        shortest_path.reverse()
        
        return shortest_path

     

