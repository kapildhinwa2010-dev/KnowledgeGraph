# KnowledgeGraph

KnowledgeGraph is a small Python library for storing string-valued facts as directed, labelled `(subject, predicate, object)` triples and querying them as a graph. Version `0.1.0` provides an in-memory implementation; it is an early-stage, limited-scope utility rather than a general graph database.

## Features

- `Fact(subject, predicate, object)` validates that all three values are non-empty strings and can be represented as a tuple.
- `KnowledgeNet.add(subject, predicate, object)` adds a fact and returns `False` for an exact duplicate; `len(net)` reports the number of distinct facts.
- `query(subject=None, predicate=None, obj=None)` filters facts by any combination of fields. `facts()` returns sorted `Fact` objects.
- `nodes()` returns sorted distinct subjects and objects; `edges()` returns sorted triple tuples.
- `degree(node)` counts incident incoming and outgoing edges.
- `neighbors(node, predicate=None)` returns sorted, distinct adjacent nodes, optionally filtered by predicate. It does not distinguish incoming from outgoing relationships.
- `chain(start, predicate, max_hops=4)` follows a predicate for up to the hop limit and stops when no matching edge is found or the walk reaches a previously visited node.

## Installation

From the repository root, install the project with Python 3.9 or newer:

```bash
python -m pip install .
```

The project metadata declares `numpy>=1.24` as a dependency. The repository does not provide a command-line interface.

## Example

```python
from knowledgegraph import KnowledgeNet

net = KnowledgeNet()
net.add("a", "next", "b")
net.add("b", "next", "c")

print(net.nodes())                    # ['a', 'b', 'c']
print(net.edges())                    # [('a', 'next', 'b'), ('b', 'next', 'c')]
print(net.neighbors("b"))             # ['a', 'c']
print(net.degree("b"))                # 2
print(net.chain("a", "next"))         # ['b', 'c']
```

## Tests and checks

On the cloned repository commit `143636747ddca51d0230318b43581be4bfad77fc`, the test suite was run locally with Python 3.12.3: **11 tests passed**. `compileall` completed and the import smoke check instantiated `KnowledgeNet` successfully. These are local checks, not a claim about a hosted GitHub Actions run. The configured CI workflow runs pytest, compilation, and an import smoke check on Python 3.10, 3.11, and 3.12.

To run the tests from the repository root:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Limitations

- All facts and indexes are held in memory; there is no persistence or serialization layer.
- `chain` follows only the first matching outgoing edge at each step; it is a single walk, not branching path search.
- `neighbors` treats adjacency in either direction alike. There are no shortest-path, centrality, traversal-planning, or community-detection algorithms in this implementation.
- No performance benchmarks or production-readiness evidence are included in the repository.

## License

The repository includes an MIT License. See [LICENSE](LICENSE) for its full terms (copyright © 2026 Kapildhinwa2010-dev).
