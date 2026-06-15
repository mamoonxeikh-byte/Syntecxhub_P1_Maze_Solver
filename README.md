# 🧩 A* Maze Solver

**Syntecxhub AI Internship — Week 1, Project 1**
**Intern:** Muhammad Mamoon | `mamoonxeikh-byte`

---

## 📌 Overview

An interactive Maze Solver built with **A\* Search Algorithm** and **Streamlit**, featuring real-time visualization, step-by-step inference logging, and multiple preset mazes.

## ✨ Features

- **A\* Search** with Manhattan & Euclidean heuristics
- **4 preset mazes** including a no-solution case
- **Full visualization** — explored nodes (blue), final path (purple), start (green), goal (orange)
- **Inference log** showing every step: node explored, g/h/f scores
- **Search efficiency metric** — path nodes vs total explored
- Dark-themed professional UI

## 🚀 Run Locally

```bash
git clone https://github.com/mamoonxeikh-byte/Syntecxhub_Maze_Solver.git
cd Syntecxhub_Maze_Solver
pip install -r requirements.txt
streamlit run app.py
```

## 🧠 Algorithm

A* uses: **f(n) = g(n) + h(n)**

| Term | Meaning |
|------|---------|
| `g(n)` | Actual cost from start to node n |
| `h(n)` | Heuristic estimate from n to goal |
| `f(n)` | Total priority (lower = explored first) |

**Manhattan heuristic:** `|row1-row2| + |col1-col2|`  
**Euclidean heuristic:** `√((row1-row2)² + (col1-col2)²)`

## 📁 Structure

```
Syntecxhub_Maze_Solver/
├── app.py            # Main Streamlit app + A* logic
├── requirements.txt
└── README.md
```

## 🏢 Internship

**Company:** Syntecxhub (Create | Think | Solve)  
**Track:** Artificial Intelligence  
**Duration:** Week 1 Task Submission
