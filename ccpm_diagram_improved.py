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
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch
from matplotlib import rcParams

# ---------- Type Definitions ----------
Point = Tuple[float, float]
Box = Tuple[float, float, float, float]  # (x, y, width, height)
ShapeData = namedtuple("ShapeData", ["points", "box"])

# ---------- Theme & Colors ----------
rcParams["pdf.fonttype"] = 42
rcParams["ps.fonttype"]  = 42
rcParams["font.size"]    = 10

EDGE       = "#222222"
TASK_COLOR = "#E8E8E8"   # tasks
FB_COLOR   = "#8EC9FF"   # feeding buffers
PB_COLOR   = "#FFC933"   # project buffer
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

# ---------- Diagram Generation ----------
def create_ccpm_diagram() -> None:
    """Generate and export the CCPM diagram."""
    # Figure setup
    fig, ax = plt.subplots(figsize=(12.6, 5.0))
    fig.suptitle("Critical Chain Schedule with Buffers", fontsize=14, fontweight="bold", y=0.98)
    fig.text(0.5, 0.945, "(Online Examination System Upgrade)", ha="center", va="center", fontsize=11)

    # Layout constants (uniform spacing)
    x0, dx = 0.8, 2.4  # start and horizontal step
    y_main = 1.0
    y_feed_1 = 2.10   # F feeder row
    y_feed_2 = 1.60   # G feeder row
    gap = 0.20        # visual air gap for feeder arrows
    
    # ---------- Critical Chain (Main Tasks) ----------
    A = task(ax, x0 + 0*dx, y_main, txt="A")
    B = task(ax, x0 + 1*dx, y_main, txt="B")
    C = task(ax, x0 + 2*dx, y_main, txt="C")
    D = task(ax, x0 + 3*dx, y_main, txt="D")
    E = task(ax, x0 + 4*dx, y_main, txt="E")
    H = task(ax, x0 + 5*dx, y_main, txt="H")
    I = task(ax, x0 + 6*dx, y_main, txt="I")
    PB_data = trap_left(ax, x0 + 7*dx, y_main, txt="PB", color=PB_COLOR)

    # Chain arrows (sequential connections)
    chain = [(A, B), (B, C), (C, D), (D, E), (E, H), (H, I)]
    for from_task, to_task in chain:
        arrow(ax, right_mid(from_task), left_mid(to_task))

    # I -> PB: aim at the PB left-edge midpoint
    pb_left_mid = (PB_data.points[0][0], (PB_data.points[0][1] + PB_data.points[3][1]) / 2.0)
    arrow(ax, right_mid(I), pb_left_mid)

    # ---------- Feeders (Parallel Tasks with Buffers) ----------
    def create_feeder(feeder_task: Box, feeder_y: float, buffer_x: float,
                      main_task: Box, buffer_label: str = "FB") -> None:
        """Create a feeder task -> buffer -> main task connection."""
        fb_data = trap_left(ax, buffer_x, feeder_y, txt=buffer_label, color=FB_COLOR)
        arrow(ax, center(feeder_task), left_mid(fb_data.box))
        
        bm_buffer = bottom_mid(fb_data.box)
        tm_task = top_mid(main_task)
        arrow(ax, (bm_buffer[0], bm_buffer[1] - gap), (tm_task[0], tm_task[1] + gap))

    # F -> FB1 -> E
    F = task(ax, x0 + 2.6*dx, y_feed_1, txt="F")
    create_feeder(F, y_feed_1, x0 + 4.15*dx, E)

    # G -> FB2 -> H
    G = task(ax, x0 + 3.45*dx, y_feed_2, txt="G")
    create_feeder(G, y_feed_2, x0 + 5.00*dx, H)

    # ---------- Resource Buffers (Flags) ----------
    def create_resource_flag(flag_x: float, flag_y: float, target_task: Box,
                             target_offset: float, label: str) -> None:
        """Create a resource buffer flag pointing to a task."""
        rb_flag(ax, flag_x, flag_y, label=label)
        rb_pos = (flag_x + FLAG_SIZE/2, flag_y - 0.40)
        target_point = (target_task[0] + target_task[2]*target_offset, target_task[1] + gap)
        arrow(ax, rb_pos, target_point)

    # RB before C (DBA)
    create_resource_flag(x0 + 2*dx - 1.0, y_main - 1.00, C, 0.78, "RB (DBA)")

    # RB before H (QA)
    create_resource_flag(x0 + 5*dx - 1.0, y_main - 1.00, H, 0.78, "RB (QA)")

    # ---------- Legend & Formatting ----------
    legend_text = (
        "Legend: Task = Rectangle  |  PB/FB = Left-facing Trapezoid (Buffers)  |  RB = Triangle Flag"
    )
    fig.text(0.5, 0.075, legend_text, ha="center", va="center", fontsize=10)

    # Canvas setup
    ax.set_xlim(0, x0 + 8.4*dx)
    ax.set_ylim(-0.9, 2.8)
    ax.axis("off")
    plt.tight_layout(rect=[0.03, 0.10, 0.97, 0.90])

    # Export
    output_base = "ccpm_from_slides_clean"
    formats = ["png", "pdf", "svg"]
    for fmt in formats:
        filename = f"{output_base}.{fmt}"
        kwargs = {"bbox_inches": "tight"}
        if fmt == "png":
            kwargs["dpi"] = 300
        plt.savefig(filename, **kwargs)
    
    print(f"✅ Exported: {', '.join(f'{output_base}.{fmt}' for fmt in formats)}")
    plt.show()


if __name__ == "__main__":
    create_ccpm_diagram()
