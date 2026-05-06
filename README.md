# 🗺 RouteIQ — Algorithm Visualizer

A full-stack web application that visually demonstrates and compares three fundamental graph algorithms:
- **Dijkstra's Algorithm** — optimal shortest path
- **Greedy Best-First Search** — heuristic-driven fast pathfinding
- **Dynamic Programming (Memoized)** — recursive optimal substructure

Built with Python (Flask) + vanilla HTML/CSS/JS.

---

## 📸 Features

- Interactive graph with 6 nodes and weighted edges
- Select any **start** and **end** node
- All three algorithms run simultaneously and compare:
  - Path found
  - Total cost
  - Step-by-step traversal
  - Optimality
- Color-coded visualization on the canvas (Dijkstra = cyan, Greedy = orange, DP = green)
- Comparison table with time complexity info

---

## 🚀 Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/route-optimizer.git
cd route-optimizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open browser
# http://localhost:5050
```

---

## 🧠 Algorithm Details

### Dijkstra's Algorithm
- **Type:** Shortest path (non-negative weights)
- **Time Complexity:** O((V + E) log V)
- **Space Complexity:** O(V)
- **Guarantee:** Always finds the optimal path
- Uses a **min-heap** priority queue

### Greedy Best-First Search
- **Type:** Heuristic search
- **Time Complexity:** O(E log V)
- **Space Complexity:** O(V)
- **Guarantee:** Fast but not always optimal
- Uses **straight-line distance** as heuristic

### Dynamic Programming (Memoized)
- **Type:** Exhaustive optimal search with memoization
- **Time Complexity:** O(2ⁿ × V) — exponential due to subset states
- **Space Complexity:** O(2ⁿ × V)
- **Guarantee:** Always finds the globally optimal path
- Caches subproblems to avoid recomputation

---

## 📊 Comparison

| Algorithm | Optimal? | Best For |
|-----------|----------|----------|
| Dijkstra | ✅ Yes | General shortest paths |
| Greedy BFS | ❌ Not always | Speed-critical applications |
| DP Memoized | ✅ Yes | Exhaustive analysis, small graphs |

---

## 🛠 Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5 Canvas, CSS3, Vanilla JavaScript
- **Fonts:** Google Fonts (Syne, Space Mono)

---

## 📁 Project Structure

```
route_optimizer/
├── app.py              # Flask server + all algorithm implementations
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Full UI with Canvas visualization
└── README.md
```

---

## 🎓 Academic Context

Submitted as part of the CCC Algorithm Project.
Demonstrates: Greedy algorithms, Dynamic Programming, and Dijkstra's shortest path.
