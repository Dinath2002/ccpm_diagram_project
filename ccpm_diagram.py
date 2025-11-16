<<<<<<< HEAD
# ccpm_from_slides_clean.py
# Clean CCPM diagram: slide-accurate shapes, uniform gaps, no overlaps.

=======
"""
Critical Chain Project Management (CCPM) Diagram Generator

Creates a professional CCPM schedule visualization with:
- Critical chain tasks (rectangles)
- Feeding buffers (left-facing trapezoids)
- Project buffer (project completion buffer)
- Resource buffers (triangle flags)
"""

from typing import Tuple, List
from collections import namedtuple
>>>>>>> 5823195 (Update CCPM diagram project)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch
from matplotlib import rcParams

<<<<<<< HEAD
# ---------- Theme ----------
rcParams["pdf.fonttype"] = 42
rcParams["ps.fonttype"]  = 42
rcParams["font.size"]    = 10
=======
# ---------- Type Definitions ----------
Point = Tuple[float, float]
Box = Tuple[float, float, float, float]  # (x, y, width, height)
ShapeData = namedtuple("ShapeData", ["points", "box"])

# ---------- Theme & Colors ----------
rcParams["pdf.fonttype"] = 42
rcParams["ps.fonttype"]  = 42
rcParams["font.size"]    = 10

>>>>>>> 5823195 (Update CCPM diagram project)
EDGE       = "#222222"
TASK_COLOR = "#E8E8E8"   # tasks
FB_COLOR   = "#8EC9FF"   # feeding buffers
PB_COLOR   = "#FFC933"   # project buffer
<<<<<<< HEAD
RB_COLOR   = "#FFB0B0"   # resource flags

# ---------- Shape helpers ----------
def task(ax, x, y, w=1.8, h=0.8, txt=""):
    r = Rectangle((x, y), w, h, facecolor=TASK_COLOR, edgecolor=EDGE, linewidth=1.4)
    ax.add_patch(r)
    ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=11, fontweight="bold", color="#1a1a1a")
    return (x, y, w, h)

def trap_left(ax, x, y, w=1.6, h=0.8, txt="FB", color=FB_COLOR):
    # left-facing trapezoid (as in slides)
    pts = [(x, y), (x+w, y), (x+w, y+h), (x+0.4*w, y+h)]
    poly = Polygon(pts, closed=True, facecolor=color, edgecolor=EDGE, linewidth=1.4)
    ax.add_patch(poly)
    ax.text(x+0.70*w, y+h/2, txt, ha="center", va="center", fontsize=11, fontweight="bold")
    return pts, (x, y, w, h)  # polygon points + rect-like box for anchors

def rb_flag(ax, x, y, s=0.5, label="RB"):
    tri = Polygon([(x, y), (x+s, y), (x+0.5*s, y+0.58*s)],
                  closed=True, facecolor=RB_COLOR, edgecolor=EDGE, linewidth=1.4)
    ax.add_patch(tri)
    ax.text(x+0.5*s, y+0.8*s, label, ha="center", va="bottom", fontsize=10, fontweight="bold")
    return tri

# ---------- Anchor helpers ----------
def left_mid(b):   x,y,w,h=b; return (x,     y+h/2)
def right_mid(b):  x,y,w,h=b; return (x+w,   y+h/2)
def top_mid(b):    x,y,w,h=b; return (x+w/2, y+h)
def bottom_mid(b): x,y,w,h=b; return (x+w/2, y)
def center(b):     x,y,w,h=b; return (x+w/2, y+h/2)

def arrow(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="->", mutation_scale=12,
                                 linewidth=1.4, color=EDGE))
=======
RB_COLOR   = "#FFB0B0"   # resource buffers/flags

# ---------- Layout Constants ----------
TASK_WIDTH = 1.8
TASK_HEIGHT = 0.8
BUFFER_WIDTH = 1.6
BUFFER_HEIGHT = 0.8
TRAP_INDENT = 0.4  # trapezoid left indent factor
FLAG_SIZE = 0.5
TEXT_SIZE = 11
FLAG_TEXT_SIZE = 10
FONT_WEIGHT = "bold"
TEXT_COLOR = "#1a1a1a"

# ---------- Shape Helpers ----------
def task(ax: plt.Axes, x: float, y: float, w: float = TASK_WIDTH,
         h: float = TASK_HEIGHT, txt: str = "") -> Box:
    """Create a rectangular task box on the diagram."""
    rect = Rectangle((x, y), w, h, facecolor=TASK_COLOR, edgecolor=EDGE, linewidth=1.4)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, txt, ha="center", va="center",
            fontsize=TEXT_SIZE, fontweight=FONT_WEIGHT, color=TEXT_COLOR)
    return (x, y, w, h)


def trap_left(ax: plt.Axes, x: float, y: float, w: float = BUFFER_WIDTH,
              h: float = BUFFER_HEIGHT, txt: str = "FB", color: str = FB_COLOR) -> ShapeData:
    """Create a left-facing trapezoid (buffer) on the diagram.
    
    Returns:
        ShapeData with polygon points and bounding box.
    """
    indent = TRAP_INDENT * w
    pts = [(x, y), (x + w, y), (x + w, y + h), (x + indent, y + h)]
    poly = Polygon(pts, closed=True, facecolor=color, edgecolor=EDGE, linewidth=1.4)
    ax.add_patch(poly)
    ax.text(x + 0.70*w, y + h/2, txt, ha="center", va="center",
            fontsize=TEXT_SIZE, fontweight=FONT_WEIGHT)
    return ShapeData(points=pts, box=(x, y, w, h))


def rb_flag(ax: plt.Axes, x: float, y: float, s: float = FLAG_SIZE,
            label: str = "RB") -> Polygon:
    """Create a triangle flag (resource buffer) on the diagram."""
    tri = Polygon([(x, y), (x + s, y), (x + 0.5*s, y + 0.58*s)],
                  closed=True, facecolor=RB_COLOR, edgecolor=EDGE, linewidth=1.4)
    ax.add_patch(tri)
    ax.text(x + 0.5*s, y + 0.8*s, label, ha="center", va="bottom",
            fontsize=FLAG_TEXT_SIZE, fontweight=FONT_WEIGHT)
    return tri

# ---------- Anchor Helpers ----------
def left_mid(box: Box) -> Point:
    """Get the midpoint of the left edge of a box."""
    x, y, w, h = box
    return (x, y + h/2)


def right_mid(box: Box) -> Point:
    """Get the midpoint of the right edge of a box."""
    x, y, w, h = box
    return (x + w, y + h/2)


def top_mid(box: Box) -> Point:
    """Get the midpoint of the top edge of a box."""
    x, y, w, h = box
    return (x + w/2, y + h)


def bottom_mid(box: Box) -> Point:
    """Get the midpoint of the bottom edge of a box."""
    x, y, w, h = box
    return (x + w/2, y)


def center(box: Box) -> Point:
    """Get the center point of a box."""
    x, y, w, h = box
    return (x + w/2, y + h/2)


def arrow(ax: plt.Axes, p1: Point, p2: Point, width: float = 1.4) -> None:
    """Draw an arrow between two points."""
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="->", mutation_scale=12,
                                 linewidth=width, color=EDGE))
>>>>>>> 5823195 (Update CCPM diagram project)

# ---------- Figure ----------
fig, ax = plt.subplots(figsize=(12.6, 5.0))
fig.suptitle("Critical Chain Schedule with Buffers", fontsize=14, fontweight="bold", y=0.98)
fig.text(0.5, 0.945, "(Online Examination System Upgrade)", ha="center", va="center", fontsize=11)

# Layout constants (uniform spacing)
x0, dx   = 0.8, 2.4          # start and step (controls horizontal gap)
y_main   = 1.0
y_feed_1 = 2.10              # F feeder row
y_feed_2 = 1.60              # G feeder row
gap      = 0.20              # visual air gap for feeder arrows landing

# ---------- Critical chain (rectangles) ----------
A = task(ax, x0 + 0*dx, y_main, txt="A")
B = task(ax, x0 + 1*dx, y_main, txt="B")
C = task(ax, x0 + 2*dx, y_main, txt="C")
D = task(ax, x0 + 3*dx, y_main, txt="D")
E = task(ax, x0 + 4*dx, y_main, txt="E")
H = task(ax, x0 + 5*dx, y_main, txt="H")
I = task(ax, x0 + 6*dx, y_main, txt="I")
PB_pts, PB_box = trap_left(ax, x0 + 7*dx, y_main, txt="PB", color=PB_COLOR)

# chain arrows (box-to-box, nothing touches)
for f, t in [(A,B),(B,C),(C,D),(D,E),(E,H),(H,I)]:
    arrow(ax, right_mid(f), left_mid(t))

# I -> PB: aim at the PB left-edge midpoint (between pts[0] & pts[3])
pb_left_mid = (PB_pts[0][0], (PB_pts[0][1] + PB_pts[3][1]) / 2.0)
arrow(ax, right_mid(I), pb_left_mid)

# ---------- Feeders (do NOT touch tasks; land with a small gap) ----------
# F -> FB1 -> E
F  = task(ax, x0 + 2.6*dx, y_feed_1, txt="F")
FB1_pts, FB1_box = trap_left(ax, x0 + 4.15*dx, y_feed_1, txt="FB", color=FB_COLOR)
arrow(ax, center(F), left_mid(FB1_box))                         # F to FB1
# FB1 to E: bottom-mid of FB1 to top-mid of E, subtract small gap so arrow tip doesn’t overlap
bm_FB1 = bottom_mid(FB1_box)
tm_E   = top_mid(E)
arrow(ax, (bm_FB1[0], bm_FB1[1]-gap), (tm_E[0], tm_E[1]+gap))

# G -> FB2 -> H
G  = task(ax, x0 + 3.45*dx, y_feed_2, txt="G")
FB2_pts, FB2_box = trap_left(ax, x0 + 5.00*dx, y_feed_2, txt="FB", color=FB_COLOR)
arrow(ax, center(G), left_mid(FB2_box))                         # G to FB2
bm_FB2 = bottom_mid(FB2_box)
tm_H   = top_mid(H)
arrow(ax, (bm_FB2[0], bm_FB2[1]-gap), (tm_H[0], tm_H[1]+gap))

# ---------- Resource buffers (triangle flags) ----------
# RB before C (DBA): point to bottom edge of C near right side
rb_flag(ax, x0 + 2*dx - 1.0, y_main - 1.00, label="RB (DBA)")
arrow(ax, (x0 + 2*dx - 0.50, y_main - 0.40), (C[0] + C[2]*0.78, C[1] + gap))

# RB before H (QA): point to bottom edge of H near right side
rb_flag(ax, x0 + 5*dx - 1.0, y_main - 1.00, label="RB (QA)")
arrow(ax, (x0 + 5*dx - 0.50, y_main - 0.40), (H[0] + H[2]*0.78, H[1] + gap))

# ---------- Legend ----------
fig.text(0.5, 0.075,
         "Legend: Task = Rectangle  |  PB/FB = Left-facing Trapezoid (Buffers)  |  RB = Triangle Flag",
         ha="center", va="center", fontsize=10)

# ---------- Canvas / export ----------
ax.set_xlim(0, x0 + 8.4*dx)
ax.set_ylim(-0.9, 2.8)
ax.axis("off")
plt.tight_layout(rect=[0.03, 0.10, 0.97, 0.90])

plt.savefig("ccpm_from_slides_clean.png", dpi=300, bbox_inches="tight")
plt.savefig("ccpm_from_slides_clean.pdf", bbox_inches="tight")
plt.savefig("ccpm_from_slides_clean.svg", bbox_inches="tight")
print("✅ Exported: ccpm_from_slides_clean.png / .pdf / .svg")

<<<<<<< HEAD
plt.show()
=======
plt.show()
>>>>>>> 5823195 (Update CCPM diagram project)
