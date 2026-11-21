"""
Problem 8.6 - Shortest common superstring for eight 3-mers
    {AGT, AAA, ACT, AAC, CTT, GTA, TTT, TAA}

Part 1: Hamiltonian path approach (overlap graph: 3-mers are VERTICES)
Part 2: Eulerian path approach   (de Bruijn graph: 3-mers are EDGES)
"""
from collections import defaultdict

KMERS = ["AGT", "AAA", "ACT", "AAC", "CTT", "GTA", "TTT", "TAA"]


def spell(path, k):
    """Glue a path of overlapping strings: first one in full, then the last char of each next one."""
    return path[0] + "".join(node[-1] for node in path[1:])

# part 1: Hamiltonian path
def overlap_graph(kmers):
    """Edge x -> y when suffix(x) (last k-1 chars) == prefix(y) (first k-1 chars)."""
    graph = defaultdict(list)
    for x in kmers:
        for y in kmers:
            if x[1:] == y[:-1]:
                graph[x].append(y)
    return graph


def hamiltonian_path(graph, nodes):
    #Backtracking search for a path that visits every vertex exactly once.
    def extend(path, visited):
        if len(path) == len(nodes):
            return path
        for nxt in graph[path[-1]]:
            if nxt not in visited:
                visited.add(nxt)
                result = extend(path + [nxt], visited)
                if result:
                    return result
                visited.remove(nxt)
        return None

    for start in nodes:
        result = extend([start], {start})
        if result:
            return result
    return None


# p 2: Eulerian path
def de_bruijn_graph(kmers):
    """Each k-mer becomes an edge prefix -> suffix between (k-1)-mer vertices."""
    graph = defaultdict(list)
    for kmer in kmers:
        graph[kmer[:-1]].append(kmer[1:])
    return graph


def eulerian_path(graph):
    """Hierholzer's algorithm: uses every edge exactly once."""
    out_deg = defaultdict(int)
    in_deg = defaultdict(int)
    for u, vs in graph.items():
        for v in vs:
            out_deg[u] += 1
            in_deg[v] += 1

    # Start at the vertex with one more outgoing than incoming edge
    nodes = set(out_deg) | set(in_deg)
    start = next((n for n in nodes if out_deg[n] - in_deg[n] == 1), next(iter(graph)))

    adj = {u: list(vs) for u, vs in graph.items()}
    stack, path = [start], []
    while stack:
        u = stack[-1]
        if adj.get(u):
            stack.append(adj[u].pop())
        else:
            path.append(stack.pop())
    return path[::-1]
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    k = 3

    print("=" * 60)
    print("PART 1: Hamiltonian path (3-mers are vertices)")
    print("=" * 60)
    og = overlap_graph(KMERS)
    all_edges = [(u, v) for u in KMERS for v in og[u]]
    print(f"Overlap graph: {len(KMERS)} vertices, {len(all_edges)} edges")
    for u in KMERS:
        print(f"  {u} -> {', '.join(og[u]) or '(none)'}")

    ham = hamiltonian_path(og, KMERS)
    used = set(zip(ham, ham[1:]))
    unused = [e for e in all_edges if e not in used]
    print("\nHamiltonian path:", " -> ".join(ham))
    print(f"Edges used: {len(used)} of {len(all_edges)}")
    print("Visits every edge?", "Yes" if not unused else "No")
    print("Unused edges:", ", ".join(f"{u}->{v}" for u, v in unused))
    print("Superstring:", spell(ham, k))

    print()
    print("=" * 60)
    print("PART 2: Eulerian path (3-mers are edges)")
    print("=" * 60)
    db = de_bruijn_graph(KMERS)
    vertices = sorted({v for kmer in KMERS for v in (kmer[:-1], kmer[1:])})
    print(f"de Bruijn graph: {len(vertices)} vertices, {len(KMERS)} edges")
    for u in vertices:
        print(f"  {u} -> {', '.join(db[u]) or '(none)'}")

    eul = eulerian_path(db)
    print("\nEulerian path:", " -> ".join(eul))
    print(f"Edges used: {len(eul) - 1} of {len(KMERS)}")
    repeats = sorted({v for v in eul if eul.count(v) > 1})
    print("Visits every vertex exactly once?", "Yes" if not repeats else "No")
    print("Vertices visited more than once:",
          ", ".join(f"{v} ({eul.count(v)}x)" for v in repeats))
    print("Superstring:", spell(eul, k))
