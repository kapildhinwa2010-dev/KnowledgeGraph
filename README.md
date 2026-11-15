# KnowledgeGraph

[![CI](https://github.com/kapildhinwa2010-dev/KnowledgeGraph/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/KnowledgeGraph/actions/workflows/ci.yml)
[![CI](https://github.com/kapildhinwa2010-dev/KnowledgeGraph/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/KnowledgeGraph/actions/workflows/codeql.yml)

Graph view of facts: nodes, edges, in+out degree and neighbor queries.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

KnowledgeGraph treats the triple store as a directed labelled graph:
node listing, edge listing, in+out degree, and optionally
predicate-filtered neighbor queries. Semantic recall lives in
SemanticMemory; causal analysis in CausalMemory; storage extras in
FactBase.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from knowledgegraph import KnowledgeNet

net = KnowledgeNet()
net.add("a", "next", "b")
net.add("b", "next", "c")
print(net.neighbors("b"))   # ["a", "c"]
print(net.degree("b"))      # 2
```

## API

- add / query / facts / chain - shared triple store
- nodes() - sorted distinct subjects and objects
- edges() - all (subject, predicate, object) tuples
- degree(node) - in + out edge count
- neighbors(node, predicate=None) - adjacent nodes

## Honest results and limitations

- No graph algorithms beyond degree/neighbors/walk: no centrality,
  shortest path, or community detection (see ChainReasoner for
  reachability and paths).
- Edges are unweighted; neighbors() does not show direction.
- In-memory only; no persistence.

## License

MIT - see [LICENSE](LICENSE).
