import streamlit as st
import heapq

st.set_page_config(page_title="A* Maze Solver", page_icon="🧩", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

/* ── DEEP SPACE BACKGROUND ── */
.stApp {
    background: radial-gradient(ellipse at 20% 10%, #1a0533 0%, #07090f 55%, #001a2c 100%);
    min-height: 100vh;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0118 0%, #060b18 100%) !important;
    border-right: 1px solid rgba(168,85,247,0.15) !important;
}

/* ── HEADER ── */
.hero {
    font-size: 2.3rem; font-weight: 700; letter-spacing: -0.02em;
    background: linear-gradient(100deg, #e879f9 0%, #a855f7 35%, #6366f1 65%, #22d3ee 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 24px rgba(168,85,247,0.4));
}
.sub {
    font-family: 'JetBrains Mono', monospace; color: #4b3f6b;
    font-size: 0.75rem; letter-spacing: .12em; margin-bottom: 1rem;
}

/* ── MAZE GRID ── */
.maze-wrap {
    display: flex; flex-direction: column; gap: 3px;
    width: fit-content; margin: 0 auto;
    padding: 14px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(168,85,247,0.12);
    border-radius: 16px;
    box-shadow: 0 0 60px rgba(99,102,241,0.08), inset 0 0 40px rgba(0,0,0,0.3);
}
.maze-row { display: flex; gap: 3px; }
.cell {
    width: 46px; height: 46px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 1rem;
    position: relative; transition: all .12s ease;
}

/* FREE — subtle grid tile */
.cell-free {
    background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
    border: 1px solid rgba(255,255,255,0.04);
}
/* WALL — obsidian block */
.cell-wall {
    background: linear-gradient(135deg, #020407 0%, #060a12 100%);
    border: 1px solid rgba(99,102,241,0.06);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
}
/* PLAYER — neon lime pulse */
.cell-player {
    background: linear-gradient(135deg, #4ade80 0%, #22c55e 60%, #16a34a 100%);
    border: 2px solid #86efac;
    box-shadow: 0 0 16px rgba(74,222,128,0.7), 0 0 4px rgba(74,222,128,0.4) inset;
    color: #052e16; font-size: 1.1rem;
    animation: pulse-green 1.6s ease-in-out infinite;
}
@keyframes pulse-green {
    0%,100% { box-shadow: 0 0 16px rgba(74,222,128,0.7); }
    50%      { box-shadow: 0 0 28px rgba(74,222,128,0.95), 0 0 8px rgba(74,222,128,0.5) inset; }
}
/* GOAL — amber beacon */
.cell-goal {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 60%, #d97706 100%);
    border: 2px solid #fde68a;
    box-shadow: 0 0 18px rgba(251,191,36,0.65), 0 0 6px rgba(251,191,36,0.3) inset;
    color: #451a03; font-size: 1.1rem;
    animation: pulse-amber 2s ease-in-out infinite;
}
@keyframes pulse-amber {
    0%,100% { box-shadow: 0 0 18px rgba(251,191,36,0.65); }
    50%      { box-shadow: 0 0 30px rgba(251,191,36,0.9); }
}
/* A* PATH HINT — violet glow trail */
.cell-apath {
    background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 60%, #7c3aed 100%);
    border: 1px solid rgba(167,139,250,0.5);
    box-shadow: 0 0 10px rgba(124,58,237,0.5);
    color: #ddd6fe;
}
/* PLAYER TRAIL — deep teal footprint */
.cell-trail {
    background: linear-gradient(135deg, #042f2e 0%, #064e3b 60%, #065f46 100%);
    border: 1px solid rgba(52,211,153,0.2);
    color: rgba(52,211,153,0.4);
}
/* START marker */
.cell-start {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    border: 1px solid rgba(129,140,248,0.3);
    color: #818cf8;
}

/* ── STAT CARDS ── */
.stat-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(168,85,247,0.05) 100%);
    border: 1px solid rgba(168,85,247,0.18);
    border-radius: 12px; padding: .75rem 1rem;
    text-align: center; margin-bottom: .5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.stat-num {
    font-size: 1.6rem; font-weight: 700;
    background: linear-gradient(90deg, #e879f9, #a855f7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-family: 'JetBrains Mono', monospace;
}
.stat-lbl { font-size: .67rem; color: #4b3f6b; text-transform: uppercase; letter-spacing: .12em; margin-top: 2px; }

/* ── INFO BOX ── */
.info-box {
    background: linear-gradient(90deg, rgba(34,211,238,0.06) 0%, transparent 100%);
    border-left: 3px solid #22d3ee;
    border-radius: 0 10px 10px 0;
    padding: .65rem 1rem; font-size: .82rem; color: #7dd3fc; margin: .6rem 0;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #9333ea 100%) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 22px rgba(124,58,237,0.55) !important;
    transform: translateY(-1px) !important;
}

/* ── BANNERS ── */
.win-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(5,150,105,0.1) 100%);
    border: 1px solid #10b981;
    border-radius: 14px; padding: 1.1rem 1.5rem;
    text-align: center; color: #6ee7b7;
    font-size: 1.05rem; font-weight: 700; margin: .8rem 0;
    box-shadow: 0 0 30px rgba(16,185,129,0.15);
}
.lose-banner {
    background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px; padding: .8rem 1.2rem;
    text-align: center; color: #fca5a5; font-size: .88rem; margin: .8rem 0;
}

/* ── SCROLLABLE LOG ── */
.log-box {
    background: rgba(0,0,0,0.45);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 10px; padding: .75rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .71rem; color: #a78bfa;
    max-height: 260px; overflow-y: auto;
    line-height: 1.7;
}
.log-box-green {
    background: rgba(0,0,0,0.45);
    border: 1px solid rgba(52,211,153,0.15);
    border-radius: 10px; padding: .75rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .71rem; color: #6ee7b7;
    max-height: 180px; overflow-y: auto;
    line-height: 1.7;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stRadio"] label { color: #7c6fa0 !important; font-size: .82rem !important; }
hr { border-color: rgba(168,85,247,0.12) !important; }
</style>
""", unsafe_allow_html=True)

# ── MAZES ─────────────────────────────────────────────────────────────────────
MAZES = {
    "Easy 10×10": {
        "rows":10,"cols":10,"start":(0,0),"goal":(9,9),
        "walls":[
            (1,1),(1,2),(1,3),(2,3),(3,3),(3,4),(3,5),
            (4,1),(4,2),(5,5),(5,6),(6,6),(7,6),(7,7),
            (8,3),(8,4),(8,5),(6,2),(6,3)
        ]
    },
    "Medium 12×12": {
        "rows":12,"cols":12,"start":(0,0),"goal":(11,11),
        "walls":[
            (0,2),(1,2),(2,2),(3,2),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
            (2,4),(3,4),(6,4),(7,4),(8,4),(9,4),
            (6,6),(6,7),(6,8),(6,9),(6,10),
            (8,6),(9,6),(10,6),(2,8),(3,8),(4,8),(5,8),
            (10,8),(10,9),(10,10)
        ]
    },
    "Hard 14×14": {
        "rows":14,"cols":14,"start":(0,0),"goal":(13,13),
        "walls":[
            *[(0,c) for c in range(2,10)],
            *[(r,2) for r in range(1,6)],
            *[(5,c) for c in range(2,9)],
            *[(r,8) for r in range(5,10)],
            *[(9,c) for c in range(3,9)],
            *[(r,3) for r in range(10,13)],
            *[(12,c) for c in range(3,11)],
            *[(r,10) for r in range(7,12)],
            (1,12),(2,12),(3,12),(4,12),(4,11),(4,10),(4,9),
            (6,11),(6,12),(7,11),(7,12),(8,11),(8,12),
        ]
    },
    "Blocked (No Solution)": {
        "rows":8,"cols":8,"start":(0,0),"goal":(7,7),
        "walls":[(r,3) for r in range(8)]
    },
}

# ── A* ─────────────────────────────────────────────────────────────────────────
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = [(0, start)]
    came_from = {}
    g = {start: 0}
    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == goal:
            path = []
            while cur in came_from:
                path.append(cur); cur = came_from[cur]
            path.append(start); path.reverse()
            return path
        r, c = cur
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0:
                nb = (nr,nc)
                tg = g[cur]+1
                if tg < g.get(nb, 9999):
                    came_from[nb]=cur; g[nb]=tg
                    heapq.heappush(open_set,(tg+heuristic(nb,goal),nb))
    return None

# ── SESSION STATE ──────────────────────────────────────────────────────────────
def reset(name):
    m = MAZES[name]
    rows, cols = m["rows"], m["cols"]
    grid = [[0]*cols for _ in range(rows)]
    for r,c in m["walls"]: grid[r][c]=1
    apath = astar(grid, m["start"], m["goal"])
    st.session_state.update({
        "maze_name": name, "grid": grid,
        "rows": rows, "cols": cols,
        "start": m["start"], "goal": m["goal"],
        "player": m["start"],
        "trail": {m["start"]},
        "apath": apath,
        "apath_set": set(apath) if apath else set(),
        "show_hint": False, "moves": 0,
        "won": False, "no_solution": apath is None,
        "steps_taken": [],
    })

if "maze_name" not in st.session_state:
    reset("Easy 10×10")

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero">🧩 A* Maze Solver</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">// SYNTECXHUB AI INTERNSHIP · WEEK 1 · PROJECT 1 · Muhammad Mamoon</div>', unsafe_allow_html=True)
st.markdown("""<div class="info-box">
<strong>You</strong> navigate with the arrow buttons in the sidebar.
Toggle <em>Show A* Path</em> for the optimal hint in violet.
Reach the 🏆 amber beacon to win!
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗺️ Choose Maze")
    chosen = st.selectbox("Maze", list(MAZES.keys()),
                          index=list(MAZES.keys()).index(st.session_state.maze_name))
    if chosen != st.session_state.maze_name:
        reset(chosen); st.rerun()

    st.markdown("---")
    st.markdown("### 🎮 Move Player")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("⬆️", use_container_width=True): st.session_state["_move"]="up"
    c4,c5,c6 = st.columns(3)
    with c4:
        if st.button("⬅️", use_container_width=True): st.session_state["_move"]="left"
    with c5:
        if st.button("⬇️", use_container_width=True): st.session_state["_move"]="down"
    with c6:
        if st.button("➡️", use_container_width=True): st.session_state["_move"]="right"

    st.markdown("---")
    hint_label = "🔮 Hide A* Hint" if st.session_state.show_hint else "🔮 Show A* Hint"
    if st.button(hint_label, use_container_width=True):
        st.session_state.show_hint = not st.session_state.show_hint
        st.rerun()
    if st.button("🔄 Restart Maze", use_container_width=True):
        reset(st.session_state.maze_name); st.rerun()

    st.markdown("---")
    st.markdown("### 📐 Legend")
    items = [
        ("#4ade80","▶ You (Player)", "#052e16"),
        ("#f59e0b","🏆 Goal", "#451a03"),
        ("#065f46","· Your Trail", "#34d399"),
        ("#6d28d9","· A* Hint Path", "#ddd6fe"),
        ("#060a12","  Wall", "#1e293b"),
        ("#111827","  Free Cell", "#1e293b"),
    ]
    for bg, lbl, _ in items:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:9px;margin:4px 0">'
            f'<div style="width:14px;height:14px;background:{bg};border-radius:4px;'
            f'border:1px solid rgba(255,255,255,0.08);flex-shrink:0"></div>'
            f'<span style="font-size:.79rem;color:#7c6fa0">{lbl}</span></div>',
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:.74rem;
    background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(168,85,247,0.07));
    border:1px solid rgba(168,85,247,0.2);border-radius:10px;padding:.7rem;">
    <span style="color:#e879f9;font-weight:600">f(n)</span>
    <span style="color:#4b3f6b"> = </span>
    <span style="color:#818cf8">g(n)</span>
    <span style="color:#4b3f6b"> + </span>
    <span style="color:#22d3ee">h(n)</span><br><br>
    <span style="color:#4b3f6b">g(n)</span><span style="color:#6b7280"> steps from start</span><br>
    <span style="color:#4b3f6b">h(n)</span><span style="color:#6b7280"> Manhattan to goal</span><br>
    <span style="color:#4b3f6b">f(n)</span><span style="color:#6b7280"> total priority</span>
    </div>""", unsafe_allow_html=True)

# ── PROCESS MOVE ───────────────────────────────────────────────────────────────
move = st.session_state.pop("_move", None)
if move and not st.session_state.won:
    pr, pc = st.session_state.player
    delta = {"up":(-1,0),"down":(1,0),"left":(0,-1),"right":(0,1)}[move]
    nr, nc = pr+delta[0], pc+delta[1]
    R, C = st.session_state.rows, st.session_state.cols
    if 0<=nr<R and 0<=nc<C and st.session_state.grid[nr][nc]==0:
        st.session_state.player = (nr,nc)
        st.session_state.trail.add((nr,nc))
        st.session_state.moves += 1
        st.session_state.steps_taken.append((nr,nc))
        if (nr,nc) == st.session_state.goal:
            st.session_state.won = True
    st.rerun()

# ── RENDER GRID ────────────────────────────────────────────────────────────────
col_maze, col_panel = st.columns([2.2, 1])

with col_maze:
    grid      = st.session_state.grid
    player    = st.session_state.player
    start     = st.session_state.start
    goal      = st.session_state.goal
    trail     = st.session_state.trail
    apath_set = st.session_state.apath_set if st.session_state.show_hint else set()
    R, C      = st.session_state.rows, st.session_state.cols

    rows_html = []
    for r in range(R):
        cells = []
        for c in range(C):
            pos = (r,c)
            if pos == player:
                cls,txt = "cell cell-player","●"
            elif pos == goal:
                cls,txt = "cell cell-goal","🏆"
            elif pos == start and pos not in trail:
                cls,txt = "cell cell-start","S"
            elif grid[r][c]==1:
                cls,txt = "cell cell-wall",""
            elif pos in apath_set and pos not in trail:
                cls,txt = "cell cell-apath","·"
            elif pos in trail:
                cls,txt = "cell cell-trail","·"
            else:
                cls,txt = "cell cell-free",""
            cells.append(f'<div class="{cls}">{txt}</div>')
        rows_html.append(f'<div class="maze-row">{"".join(cells)}</div>')

    st.markdown(f'<div class="maze-wrap">{"".join(rows_html)}</div>', unsafe_allow_html=True)

    if st.session_state.won:
        optimal = len(st.session_state.apath)-1 if st.session_state.apath else "?"
        extra   = st.session_state.moves - int(optimal) if st.session_state.apath else "?"
        st.markdown(f"""<div class="win-banner">
        🎉 GOAL REACHED! &nbsp;·&nbsp;
        Your moves: <strong>{st.session_state.moves}</strong> &nbsp;·&nbsp;
        A* Optimal: <strong>{optimal}</strong> &nbsp;·&nbsp;
        Extra: <strong>{extra}</strong>
        </div>""", unsafe_allow_html=True)
    elif st.session_state.no_solution:
        st.markdown('<div class="lose-banner">⚠️ No solution exists — this maze is completely blocked.</div>',
                    unsafe_allow_html=True)

# ── RIGHT PANEL ────────────────────────────────────────────────────────────────
with col_panel:
    apath   = st.session_state.apath
    moves   = st.session_state.moves
    optimal = len(apath)-1 if apath else None

    st.markdown(f"""
    <div class="stat-card"><div class="stat-num">{moves}</div><div class="stat-lbl">Your Moves</div></div>
    <div class="stat-card"><div class="stat-num">{optimal if optimal is not None else "N/A"}</div><div class="stat-lbl">A* Optimal</div></div>
    <div class="stat-card"><div class="stat-num">{len(trail)-1}</div><div class="stat-lbl">Cells Visited</div></div>
    """, unsafe_allow_html=True)

    if apath and moves>0 and optimal is not None:
        diff = moves - optimal
        if diff==0:   st.success("🏅 Perfect — you matched A*!")
        elif diff<=3: st.info(f"👍 {diff} extra step(s) vs A*")
        else:         st.warning(f"📊 {diff} extra steps — try the hint!")

    st.markdown("---")

    if apath:
        st.markdown("#### 🤖 A* Optimal Path")
        lines = []
        for i,(r,c) in enumerate(apath):
            marker = "▶" if (r,c)==player else " "
            clr = "#e879f9" if (r,c)==player else "#a78bfa"
            lines.append(f'<span style="color:{clr}">{marker}[{i:02d}] ({r},{c})</span>')
        st.markdown(f'<div class="log-box">{"<br>".join(lines)}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">No A* path for this maze.</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.steps_taken:
        st.markdown("#### 👣 Your Trail")
        lines2 = [f'[{i:02d}] ({r},{c})' for i,(r,c) in enumerate(st.session_state.steps_taken[-20:])]
        st.markdown(f'<div class="log-box-green">{"<br>".join(lines2)}</div>', unsafe_allow_html=True)

st.markdown("""<div style="text-align:center;font-family:'JetBrains Mono',monospace;
font-size:.66rem;color:#2d1f4a;margin-top:2rem;letter-spacing:.08em">
MUHAMMAD MAMOON · mamoonxeikh-byte · SYNTECXHUB AI INTERNSHIP · WEEK 1 · PROJECT 1
</div>""", unsafe_allow_html=True)