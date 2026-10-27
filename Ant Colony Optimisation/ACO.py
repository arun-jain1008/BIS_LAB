import random

class CleanAntNetRouting:
    def __init__(self, topo_graph, alpha=1.0, beta=2.0, rho=0.1, Q=1.0):
        """
        Ant Colony Optimization for Network Routing using pure Python data types.
        Eliminates any reliance on NumPy data types (like np.int64).
        """
        self.graph = topo_graph
        # Force all node keys to be standard Python integers or strings
        self.nodes = [self._clean_type(node) for node in topo_graph.keys()]
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        
        # Initialize pure Python pheromone table
        self.pheromone = {}
        for dest in self.nodes:
            self.pheromone[dest] = {}
            for current in self.nodes:
                self.pheromone[dest][current] = {}
                neighbors = list(self.graph[current].keys())
                if neighbors:
                    initial_phero = 1.0 / len(neighbors)
                    for neighbor in neighbors:
                        # Ensure neighbor keys are native types
                        clean_nb = self._clean_type(neighbor)
                        self.pheromone[dest][current][clean_nb] = initial_phero

    def _clean_type(self, node):
        """Converts NumPy types or objects back to native Python integers or strings."""
        if hasattr(node, 'item'): 
            return node.item()  # Extracts standard Python scalar from numpy types
        return node

    def get_heuristic(self, current, neighbor):
        latency = self.graph[current][neighbor]
        return 1.0 / float(latency) if latency > 0 else 0.0

    def select_next_node(self, current, destination, visited):
        neighbors = list(self.graph[current].keys())
        allowed_neighbors = [self._clean_type(n) for n in neighbors if self._clean_type(n) not in visited]
        
        if not allowed_neighbors:
            allowed_neighbors = [self._clean_type(n) for n in neighbors]

        weights = []
        for neighbor in allowed_neighbors:
            phero = self.pheromone[destination][current].get(neighbor, 0.01)
            heuristic = self.get_heuristic(current, neighbor)
            weight = float((phero ** self.alpha) * (heuristic ** self.beta))
            weights.append(weight)
            
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(allowed_neighbors)
            
        probabilities = [w / total_weight for w in weights]
        # Return standard native type
        return self._clean_type(random.choices(allowed_neighbors, weights=probabilities, k=1)[0])

    def simulate_ant(self, source, destination):
        source = self._clean_type(source)
        destination = self._clean_type(destination)
        
        path = [source]
        current = source
        total_latency = 0.0
        max_hops = len(self.nodes) * 2 
        
        while current != destination and len(path) < max_hops:
            next_node = self.select_next_node(current, destination, path)
            total_latency += float(self.graph[current][next_node])
            path.append(next_node)
            current = next_node
            
        if path[-1] == destination:
            return path, total_latency
        return None, float('inf')

    def update_pheromones(self, path, total_latency, destination):
        if not path or total_latency == float('inf'):
            return

        destination = self._clean_type(destination)

        # Evaporation
        for node in self.nodes:
            for neighbor in self.pheromone[destination][node]:
                self.pheromone[destination][node][neighbor] *= (1.0 - self.rho)

        # Deposit
        deposit = float(self.Q / total_latency)
        for i in range(len(path) - 1):
            curr_node = path[i]
            next_node = path[i+1]
            self.pheromone[destination][curr_node][next_node] += deposit
            
        # Re-normalize to prevent float overflow over long runs
        for node in self.nodes:
            for neighbor in self.pheromone[destination][node]:
                self.pheromone[destination][node][neighbor] = max(self.pheromone[destination][node][neighbor], 0.0001)

    def optimize_routing(self, source, destination, iterations=100, ants_per_iter=10):
        source = self._clean_type(source)
        destination = self._clean_type(destination)
        
        best_path = None
        min_latency = float('inf')

        for _ in range(iterations):
            for _ in range(ants_per_iter):
                path, latency = self.simulate_ant(source, destination)
                if latency < min_latency:
                    min_latency = latency
                    best_path = path
                self.update_pheromones(path, latency, destination)
                
        return best_path, min_latency

# ==========================================
# EXECUTABLE EXAMPLE WITH NATIVE INT ROUTING
# ==========================================
if __name__ == "__main__":
    # Pure Python dictionary topology using standard integers as node IDs
    pure_integer_topology = {
        0: {1: 2.0, 2: 5.0},
        1: {0: 2.0, 2: 2.0, 3: 3.0},
        2: {0: 5.0, 1: 2.0, 4: 1.0},
        3: {1: 3.0, 4: 2.0, 5: 1.0},
        4: {2: 1.0, 3: 2.0, 5: 4.0},
        5: {3: 1.0, 4: 4.0}
    }

    # The router engine explicitly strips any structural typing down to float/int
    optimizer = CleanAntNetRouting(pure_integer_topology, alpha=1.0, beta=2.0, rho=0.1, Q=1.0)
    
    src_node, dest_node = 0, 5
    optimal_path, optimal_latency = optimizer.optimize_routing(src_node, dest_node, iterations=100, ants_per_iter=10)
    
    print("Optimization Complete (Standard Python Types Only):")
    print(f"Calculated Best Route Path : {optimal_path}")
    print(f"Total Accumulative Latency : {optimal_latency} ms")
