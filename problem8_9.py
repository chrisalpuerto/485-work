"""
Problem 8.9 - Sequencing by Hybridization (SBH) via the Eulerian path approach
    S = {ATG, GGG, GGT, GTA, GTG, TAT, TGG}

Builds the de Bruijn graph (2-mers are vertices, 3-mers are edges),
finds ALL Eulerian paths, and prints every sequence s with Spectrum(s, 3) = S.
"""
from collections import defaultdict

SPECTRUM = ["ATG", "GGG", "GGT", "GTA", "GTG", "TAT", "TGG"]


def de_bruijn_graph(kmers):
    """Each k-mer becomes a labeled edge: prefix --kmer--> suffix."""
    edges = [(kmer[:-1], kmer[1:], kmer) for kmer in kmers]
    vertices = sorted({v for u, w, _ in edges for v in (u, w)})
    return vertices, edges


def degree_table(vertices, edges):
    out_deg = defaultdict(int)
    in_deg = defaultdict(int)
    for u, w, _ in edges:
        out_deg[u] += 1
        in_deg[w] += 1
    return {v: (out_deg[v], in_deg[v]) for v in vertices}


def all_eulerian_paths(start, edges):
    """Backtracking: try every unused edge out of the current vertex.
    A path is complete when all edges have been used exactly once."""
    results = []
    used = [False] * len(edges)

    def walk(vertex, path):
        if len(path) == len(edges) + 1:
            results.append(list(path))
            return
        for i, (u, w, _) in enumerate(edges):
            if not used[i] and u == vertex:
                used[i] = True
                path.append(w)
                walk(w, path)
                path.pop()
                used[i] = False

    walk(start, [start])
    # Duplicate edges (if any) would give repeated paths, so dedupe
    unique = []
    for p in results:
        if p not in unique:
            unique.append(p)
    return unique


def spell(path):
    """First 2-mer in full, then the last letter of each next vertex."""
    return path[0] + "".join(v[-1] for v in path[1:])


def spectrum(s, k):
    return sorted(s[i:i + k] for i in range(len(s) - k + 1))


if __name__ == "__main__":
    k = 3
    vertices, edges = de_bruijn_graph(SPECTRUM)

    print("=" * 60)
    print("de Bruijn graph (2-mers = vertices, 3-mers = edges)")
    print("=" * 60)
    print(f"Vertices ({len(vertices)}): {', '.join(vertices)}")
    print(f"Edges ({len(edges)}):")
    for u, w, label in edges:
        note = "  (self-loop)" if u == w else ""
        print(f"  {u} --{label}--> {w}{note}")

    print("\nDegree check (out - in):")
    degrees = degree_table(vertices, edges)
    start = end = None
    for v in vertices:
        out_d, in_d = degrees[v]
        diff = out_d - in_d
        tag = ""
        if diff == 1:
            start, tag = v, "  <- start"
        elif diff == -1:
            end, tag = v, "  <- end"
        print(f"  {v}: out={out_d}, in={in_d}, out-in={diff:+d}{tag}")

    if start is None:  # balanced graph: Eulerian cycle, any vertex can start
        start = vertices[0]

    print()
    print("=" * 60)
    print("All Eulerian paths")
    print("=" * 60)
    paths = all_eulerian_paths(start, edges)
    target = sorted(SPECTRUM)
    for n, p in enumerate(paths, 1):
        s = spell(p)
        ok = spectrum(s, k) == target
        print(f"Path {n}: {' -> '.join(p)}")
        print(f"  Sequence: {s}")
        print(f"  3-mers:   {', '.join(s[i:i + k] for i in range(len(s) - k + 1))}")
        print(f"  Spectrum(s, 3) == S? {'Yes' if ok else 'No'}\n")

    print(f"Number of possible sequences: {len(paths)}")
    print("Answer:", " and ".join(spell(p) for p in paths))