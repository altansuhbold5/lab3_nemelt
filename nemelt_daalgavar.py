import networkx as nx
import matplotlib.pyplot as plt

class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint = constraint
        self.nodes = 0
def is_valid(csp, var, value, assignment):
    for neighbor in csp.neighbors[var]:
        if neighbor in assignment:
            if not csp.constraint(
                var,
                value,
                neighbor,
                assignment[neighbor]
            ):
                return False
    return True
def get_available_values(csp, node, assignment):
    available = []

    for value in csp.domains[node]:
        if is_valid(csp, node, value, assignment):
            available.append(value)

    return available
def select_node(csp, assignment):
    unassigned = [
        node for node in csp.variables
        if node not in assignment
    ]
    if not unassigned:
        return None
    return min(
        unassigned,
        key=lambda node: (
            len(get_available_values(csp, node, assignment)),
            -sum(
                1 for n in csp.neighbors[node]
                if n not in assignment
            )
        )
    )
def backtracking(csp, assignment):
    if len(assignment) == len(csp.variables):
        return assignment

    node = select_node(csp, assignment)
    available_values = get_available_values(
        csp,
        node,
        assignment
    )
    for value in available_values:
        csp.nodes += 1
        assignment[node] = value

        result = backtracking(
            csp,
            assignment
        )
        if result:
            return result

        del assignment[node]

    return None
def check_solution(csp, assignment):
    if assignment is None:
        return False

    if len(assignment) != len(csp.variables):
        return False

    for node in csp.variables:
        for neighbor in csp.neighbors[node]:
            if not csp.constraint(
                node,
                assignment[node],
                neighbor,
                assignment[neighbor]
            ):
                return False

    return True
def make_timetable():
    teacher = {
        "AI": "A",
        "DM": "A",
        "NET": "B",
        "OS": "B",
        "MATH": "C",
        "ENG": "C"
    }

    group = {
        "AI": 1,
        "DM": 2,
        "NET": 1,
        "OS": 2,
        "MATH": 2,
        "ENG": 1
    }

    variables = list(teacher)

    domains = {
        node: [1, 2]
        if teacher[node] == "B"
        else [1, 2, 3, 4]
        for node in variables
    }

    def constraint(A, a, B, b):
        if teacher[A] == teacher[B] and a == b:
            return False

        if group[A] == group[B] and a == b:
            return False

        if A == "AI" and B == "DM":
            return a < b

        if A == "DM" and B == "AI":
            return b < a

        return True

    neighbors = {
        node: []
        for node in variables
    }
    for A in variables:
        for B in variables:
            if A != B:
                if (
                    teacher[A] == teacher[B]
                    or group[A] == group[B]
                ):
                    neighbors[A].append(B)

    return CSP(
        variables,
        domains,
        neighbors,
        constraint
    )
def draw_timetable(solution):
    G = nx.Graph()
    for subject in solution:
        G.add_node(subject)
    pos = {}
    slot_count = {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }
    for subject, slot in solution.items():
        pos[subject] = (
            slot,
            -slot_count[slot]
        )

        slot_count[slot] += 1

    plt.figure(figsize=(10, 5))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        font_weight="bold"
    )

    plt.xticks(
        [1, 2, 3, 4],
        [
            "Slot 1",
            "Slot 2",
            "Slot 3",
            "Slot 4"
        ]
    )
    plt.yticks([])
    plt.title("Timetable")
    plt.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    plt.show()
def make_map(colors):
    edges = [
        ("WA", "NT"),
        ("WA", "SA"),
        ("NT", "SA"),
        ("NT", "Q"),
        ("SA", "Q"),
        ("SA", "NSW"),
        ("SA", "V"),
        ("Q", "NSW"),
        ("NSW", "V")
    ]
    variables = [
        "WA",
        "NT",
        "SA",
        "Q",
        "NSW",
        "V",
        "T"
    ]
    domains = {
        node: list(colors)
        for node in variables
    }

    neighbors = {
        node: []
        for node in variables
    }
    for A, B in edges:
        neighbors[A].append(B)
        neighbors[B].append(A)

    def constraint(A, a, B, b):
        return a != b

    csp = CSP(
        variables,
        domains,
        neighbors,
        constraint
    )

    return csp, edges
def draw_map(solution, edges):
    G = nx.Graph()

    G.add_edges_from(edges)
    pos = {
        "WA": (0, 2),
        "NT": (1, 3),
        "SA": (1, 1),
        "Q": (2, 3),
        "NSW": (2, 1),
        "V": (3, 1),
        "T": (3, 0)
    }

    node_colors = [
        solution[node]
        for node in G.nodes()
    ]
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_weight="bold"
    )

    plt.title("Australia Map - 2 Colors")
    plt.show()
timetable = make_timetable()

timetable_solution = backtracking(
    timetable,
    {}
)
print("=== Timetable ===")
print("Solution:", timetable_solution)
print(
    "Valid:",
    check_solution(
        timetable,
        timetable_solution
    )
)
print("Nodes:", timetable.nodes)

draw_timetable(timetable_solution)
map_csp, edges = make_map(
    ["red", "blue"]
)

map_solution = backtracking(
    map_csp,
    {}
)
print("\n=== Australia Map - 2 Colors ===")
print("Solution:", map_solution)
print(
    "Valid:",
    check_solution(
        map_csp,
        map_solution
    )
)
print("Nodes:", map_csp.nodes)
if map_solution:
    draw_map(
        map_solution,
        edges
    )