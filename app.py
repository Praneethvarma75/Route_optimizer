from flask import Flask, render_template, request, jsonify
import heapq
import math
import time

app = Flask(__name__)

# ─────────────────────────────────────────────
# Graph definition (adjacency list with weights)
# ─────────────────────────────────────────────
DEFAULT_GRAPH = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2, "F": 6},
    "E": {"C": 10, "D": 2, "F": 3},
    "F": {"D": 6, "E": 3}
}

NODE_POSITIONS = {
    "A": (100, 250),
    "B": (250, 120),
    "C": (250, 380),
    "D": (450, 250),
    "E": (600, 380),
    "F": (750, 250)
}

# ─────────────────────────────────────────────
# Heuristic for Greedy Best-First & A* (straight-line distance)
# ─────────────────────────────────────────────
def heuristic(node, goal, positions):
    x1, y1 = positions[node]
    x2, y2 = positions[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) / 100

# ─────────────────────────────────────────────
# 1. DIJKSTRA'S ALGORITHM
# ─────────────────────────────────────────────
def dijkstra(graph, start, end):
    steps = []
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}
    pq = [(0, start)]
    visited = set()

    while pq:
        cost, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        steps.append({
            "visiting": u,
            "cost": cost,
            "distances": dict(dist),
            "visited": list(visited)
        })
        if u == end:
            break
        for v, w in graph[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    path = []
    node = end
    while node:
        path.append(node)
        node = prev[node]
    path.reverse()

    return {
        "algorithm": "Dijkstra",
        "path": path,
        "cost": dist[end],
        "steps": steps,
        "description": "Explores all nodes by shortest cumulative cost. Guarantees the optimal path."
    }

# ─────────────────────────────────────────────
# 2. GREEDY BEST-FIRST SEARCH
# ─────────────────────────────────────────────
def greedy_best_first(graph, start, end, positions):
    steps = []
    visited = set()
    prev = {start: None}
    pq = [(heuristic(start, end, positions), start)]

    while pq:
        h, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        steps.append({
            "visiting": u,
            "heuristic": round(h, 2),
            "visited": list(visited)
        })
        if u == end:
            break
        for v in graph[u]:
            if v not in visited:
                prev[v] = u
                heapq.heappush(pq, (heuristic(v, end, positions), v))

    path = []
    node = end
    visited_path = set()
    while node is not None and node not in visited_path:
        path.append(node)
        visited_path.add(node)
        node = prev.get(node)
    path.reverse()

    cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1)) if len(path) > 1 else 0

    return {
        "algorithm": "Greedy Best-First",
        "path": path,
        "cost": cost,
        "steps": steps,
        "description": "Always expands the node that appears closest to the goal using a heuristic. Fast but not always optimal."
    }

# ─────────────────────────────────────────────
# 3. DYNAMIC PROGRAMMING (memoized shortest path)
# ─────────────────────────────────────────────
def dp_shortest_path(graph, start, end):
    memo = {}
    steps = []

    def dp(node, visited_set):
        if node == end:
            return 0, [end]
        key = (node, tuple(sorted(visited_set)))
        if key in memo:
            return memo[key]

        best_cost = float('inf')
        best_path = []

        for neighbor, weight in graph[node].items():
            if neighbor not in visited_set:
                new_visited = visited_set | {neighbor}
                sub_cost, sub_path = dp(neighbor, new_visited)
                if sub_cost + weight < best_cost:
                    best_cost = sub_cost + weight
                    best_path = [node] + sub_path
                    steps.append({
                        "from": node,
                        "to": neighbor,
                        "cost": weight + sub_cost,
                        "path_so_far": best_path[:]
                    })

        memo[key] = (best_cost, best_path)
        return best_cost, best_path

    cost, path = dp(start, {start})

    return {
        "algorithm": "Dynamic Programming",
        "path": path,
        "cost": cost,
        "steps": steps[:20],
        "description": "Recursively solves subproblems with memoization. Finds the globally optimal path by avoiding redundant computations."
    }

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html',
                           nodes=list(DEFAULT_GRAPH.keys()),
                           positions=NODE_POSITIONS)

@app.route('/run', methods=['POST'])
def run():
    data = request.json
    start = data.get('start', 'A')
    end = data.get('end', 'F')

    if start not in DEFAULT_GRAPH or end not in DEFAULT_GRAPH:
        return jsonify({"error": "Invalid nodes"}), 400
    if start == end:
        return jsonify({"error": "Start and end must differ"}), 400

    results = {
        "dijkstra": dijkstra(DEFAULT_GRAPH, start, end),
        "greedy": greedy_best_first(DEFAULT_GRAPH, start, end, NODE_POSITIONS),
        "dp": dp_shortest_path(DEFAULT_GRAPH, start, end),
        "graph": DEFAULT_GRAPH,
        "positions": NODE_POSITIONS,
        "start": start,
        "end": end
    }
    return jsonify(sanitize(results))


def sanitize(obj):
    """Recursively replace float inf with 99999 for JSON safety."""
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    if isinstance(obj, float) and (obj == float('inf') or obj == float('-inf')):
        return 99999
    return obj

if __name__ == '__main__':
    app.run(debug=True, port=5050)
