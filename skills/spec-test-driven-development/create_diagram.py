import ast
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

CHAR_WIDTH = 7.5
LINE_HEIGHT = 17
COLUMN_GAP = 60
ROW_GAP = 60
MARGIN = 40
LANE_GAP = 14


@dataclass
class Node:
    label: str
    diamond: bool
    terminal: bool = False
    rank: int = 0
    x: float = 0
    y: float = 0

    @property
    def lines(self) -> list[str]:
        return textwrap.wrap(self.label, 26)

    @property
    def width(self) -> float:
        text = max(len(line) for line in self.lines) * CHAR_WIDTH
        return text * 1.5 + 30 if self.diamond else text + 30

    @property
    def height(self) -> float:
        return len(self.lines) * LINE_HEIGHT + (36 if self.diamond else 18)


@dataclass
class Edge:
    source: int
    target: int
    label: str
    back: bool


class Diagram:
    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.questions: dict[str, str] = {}
        self.asked: dict[str, int] = {}
        self.breaks: list[list[tuple[int, str]]] = []

    def add(self, label: str, diamond: bool = False, terminal: bool = False) -> int:
        self.nodes.append(Node(label, diamond, terminal))
        return len(self.nodes) - 1

    def link(self, exits: list[tuple[int, str]], target: int, back: bool = False) -> None:
        for source, label in exits:
            self.edges.append(Edge(source, target, label, back))

    def block(self, statements: list[ast.stmt], exits: list[tuple[int, str]]) -> list[tuple[int, str]]:
        for statement in statements:
            exits = self.statement(statement, exits)
        return exits

    def statement(self, statement: ast.stmt, exits: list[tuple[int, str]]) -> list[tuple[int, str]]:
        if isinstance(statement, ast.Expr) and call_name(statement.value) == "run_skill":
            box = self.add(first_argument(statement.value))
            self.link(exits, box)
            return [(box, "")]
        if isinstance(statement, ast.Assign) and call_name(statement.value) == "ask_user":
            self.questions[statement.targets[0].id] = first_argument(statement.value)
            return exits
        if isinstance(statement, ast.If):
            return self.branch(statement, exits)
        if isinstance(statement, ast.While):
            return self.loop(statement, exits)
        if isinstance(statement, ast.Break):
            self.breaks[-1].extend(exits)
            return []
        return exits

    def branch(self, statement: ast.If, exits: list[tuple[int, str]]) -> list[tuple[int, str]]:
        label, then_edge, else_edge = self.condition(statement.test)
        asked = self.asked.get(getattr(getattr(statement.test, "left", None), "id", None))
        if asked is not None and exits == [(asked, "answer")]:
            diamond = asked
        else:
            diamond = self.add(label, diamond=True)
            self.link(exits, diamond)
        then_exits = self.block(statement.body, [(diamond, then_edge)])
        else_exits = self.block(statement.orelse, [(diamond, else_edge)])
        return then_exits + else_exits

    def loop(self, statement: ast.While, exits: list[tuple[int, str]]) -> list[tuple[int, str]]:
        self.questions[statement.test.target.id] = first_argument(statement.test.value)
        diamond = self.add(first_argument(statement.test.value), diamond=True)
        self.asked[statement.test.target.id] = diamond
        self.link(exits, diamond)
        self.breaks.append([])
        self.link(self.block(statement.body, [(diamond, "answer")]), diamond, back=True)
        return [(diamond, "blank")] + self.breaks.pop()

    def condition(self, test: ast.expr) -> tuple[str, str, str]:
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            label, then_edge, else_edge = self.condition(test.operand)
            return label, else_edge, then_edge
        if call_name(test) == "check_if":
            return first_argument(test), "yes", "no"
        return self.questions[test.left.id], test.comparators[0].value, "otherwise"

    def parent(self, index: int) -> int | None:
        for edge in self.edges:
            if edge.target == index and not edge.back:
                return edge.source
        return None

    def place(self, row: list[int]) -> None:
        groups: dict[int | None, list[int]] = {}
        for index in row:
            groups.setdefault(self.parent(index), []).append(index)
        for index in row:
            sources = [self.nodes[e.source].x for e in self.edges if e.target == index and not e.back]
            if self.nodes[index].terminal and len(sources) > 1:
                groups[self.parent(index)].remove(index)
                self.nodes[index].x = sum(sources) / len(sources)
        for parent, group in groups.items():
            centre = 0 if parent is None else self.nodes[parent].x
            total = sum(self.nodes[i].width for i in group) + COLUMN_GAP * (len(group) - 1)
            left = centre - total / 2
            for i in group:
                self.nodes[i].x = left + self.nodes[i].width / 2
                left += self.nodes[i].width + COLUMN_GAP
        row.sort(key=lambda i: self.nodes[i].x)
        for before, after in zip(row, row[1:]):
            earliest = self.nodes[before].x + self.nodes[before].width / 2 + COLUMN_GAP + self.nodes[after].width / 2
            self.nodes[after].x = max(self.nodes[after].x, earliest)

    def span(self, low: int, high: int) -> list[Node]:
        return [n for n in self.nodes if low <= n.rank <= high]

    def layout(self) -> tuple[dict[int, float], float, float]:
        changed = True
        while changed:
            changed = False
            for edge in self.edges:
                source, target = self.nodes[edge.source], self.nodes[edge.target]
                if not edge.back and target.rank <= source.rank:
                    target.rank = source.rank + 1
                    changed = True
        sinks = [i for i, n in enumerate(self.nodes) if n.terminal and not any(e.source == i for e in self.edges)]
        last = max(n.rank for i, n in enumerate(self.nodes) if i not in sinks) + 1
        for i in sinks:
            self.nodes[i].rank = last
        y = MARGIN
        for rank in range(max(n.rank for n in self.nodes) + 1):
            row = [i for i, n in enumerate(self.nodes) if n.rank == rank]
            self.place(row)
            for i in row:
                self.nodes[i].y = y
            y += max(self.nodes[i].height for i in row) + ROW_GAP
        lanes: dict[int, float] = {}
        for index, edge in enumerate(self.edges):
            low, high = sorted((self.nodes[edge.source].rank, self.nodes[edge.target].rank))
            if edge.back:
                lanes[index] = max(n.x + n.width / 2 for n in self.span(low, high)) + 30 + LANE_GAP * len(lanes)
            elif high - low > 1 and self.nodes[edge.source].diamond:
                lanes[index] = max(n.x + n.width / 2 for n in self.span(low, high)) + 30 + LANE_GAP * len(lanes)
            elif high - low > 1:
                lanes[index] = min(n.x - n.width / 2 for n in self.span(low, high)) - 30 - LANE_GAP * len(lanes)
        left = min([n.x - n.width / 2 for n in self.nodes] + list(lanes.values()))
        right = max([n.x + n.width / 2 for n in self.nodes] + list(lanes.values()))
        for node in self.nodes:
            node.x += MARGIN - left
        return {i: x + MARGIN - left for i, x in lanes.items()}, right - left + 2 * MARGIN, y - ROW_GAP + MARGIN

    def svg(self) -> str:
        lanes, width, height = self.layout()
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" font-family="sans-serif" font-size="13">',
            '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            '<path d="M0,0 L10,4 L0,8 z" fill="#555"/></marker></defs>',
            f'<rect width="{width:.0f}" height="{height:.0f}" fill="white"/>',
        ]
        for index, edge in enumerate(self.edges):
            parts.append(self.edge_svg(edge, lanes.get(index)))
        for node in self.nodes:
            parts.append(self.node_svg(node))
        parts.append("</svg>")
        return "\n".join(parts)

    def node_svg(self, node: Node) -> str:
        half_width, half_height = node.width / 2, node.height / 2
        cx, cy = node.x, node.y + half_height
        if node.diamond:
            shape = f'<polygon points="{cx},{cy - half_height} {cx + half_width},{cy} {cx},{cy + half_height} {cx - half_width},{cy}" fill="#fff4d6" stroke="#b8860b"/>'
        elif node.terminal:
            shape = f'<rect x="{cx - half_width}" y="{cy - half_height}" width="{node.width}" height="{node.height}" rx="{half_height}" fill="#e3f4e8" stroke="#3b7d4f"/>'
        else:
            shape = f'<rect x="{cx - half_width}" y="{cy - half_height}" width="{node.width}" height="{node.height}" rx="6" fill="#e8f0fe" stroke="#4a6fa5"/>'
        top = cy - (len(node.lines) - 1) * LINE_HEIGHT / 2
        text = "".join(
            f'<text x="{cx}" y="{top + i * LINE_HEIGHT + 4}" text-anchor="middle" fill="#222">{escape(line)}</text>'
            for i, line in enumerate(node.lines)
        )
        return shape + text

    def edge_svg(self, edge: Edge, lane: float | None) -> str:
        source, target = self.nodes[edge.source], self.nodes[edge.target]
        x1, y1 = source.x, source.y + source.height
        if edge.back:
            x2, y2 = target.x + target.width / 2, target.y + target.height / 2
            path = f"M{x1},{y1} L{x1},{y1 + 20} L{lane},{y1 + 20} L{lane},{y2} L{x2},{y2}"
            label_x, label_y = lane, (y1 + y2) / 2
        elif lane is not None:
            x2, y2 = target.x, target.y
            if source.diamond:
                x1, y1 = source.x + source.width / 2, source.y + source.height / 2
                path = f"M{x1},{y1} L{lane},{y1} L{lane},{y2 - 20} L{x2},{y2 - 20} L{x2},{y2}"
                label_x, label_y = (x1 + lane) / 2, y1 - 6
            else:
                path = f"M{x1},{y1} L{x1},{y1 + 20} L{lane},{y1 + 20} L{lane},{y2 - 20} L{x2},{y2 - 20} L{x2},{y2}"
                label_x, label_y = (x1 + lane) / 2, y1 + 14
        else:
            x2, y2 = target.x, target.y
            drop = max((y2 - y1) / 2, 20)
            path = f"M{x1},{y1} C{x1},{y1 + drop} {x2},{y2 - drop} {x2},{y2}"
            label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
        line = f'<path d="{path}" fill="none" stroke="#555" marker-end="url(#arrow)"/>'
        if not edge.label:
            return line
        label = f'<text x="{label_x}" y="{label_y}" text-anchor="middle" fill="#555" stroke="white" stroke-width="4" paint-order="stroke">{escape(edge.label)}</text>'
        return line + label


def call_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id
    return None


def first_argument(call: ast.Call) -> str:
    return call.args[0].value


def build(source: Path) -> Diagram:
    diagram = Diagram()
    tree = ast.parse(source.read_text())
    start = diagram.add("start", terminal=True)
    exits = diagram.block([s for s in tree.body if not isinstance(s, (ast.ImportFrom, ast.FunctionDef))], [(start, "")])
    diagram.link(exits, diagram.add("end", terminal=True))
    return diagram


if __name__ == "__main__":
    Path(sys.argv[2]).write_text(build(Path(sys.argv[1])).svg())
