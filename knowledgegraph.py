# KnowledgeGraph - Fact graph: nodes, edges, degree and neighbor queries
# Part of the Kapildhinwa2010-dev Toolkit.

"""KnowledgeGraph - graph view of facts: nodes, edges, degree, neighbors.

Lineage: reserv.dean-part-2 (HELIX). Treats the triple store as a
directed labelled graph and adds GRAPH operations: node listing, edge
listing, in+out degree, and (optionally predicate-filtered) neighbor
queries. Semantic recall and causal analysis live in the sibling repos.
"""

from __future__ import annotations

from collections import defaultdict

__all__ = ["Fact", "KnowledgeNet"]


class Fact:
    """A single (subject, predicate, object) triple."""

    __slots__ = ("subject", "predicate", "object")

    def __init__(self, subject: str, predicate: str, obj: str) -> None:
        for value in (subject, predicate, obj):
            if not isinstance(value, str) or not value:
                raise ValueError("subject, predicate and object must be non-empty strings")
        self.subject = subject
        self.predicate = predicate
        self.object = obj

    def as_tuple(self):
        return (self.subject, self.predicate, self.object)

    def __eq__(self, other) -> bool:
        return isinstance(other, Fact) and self.as_tuple() == other.as_tuple()

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def __repr__(self) -> str:
        return "Fact({!r}, {!r}, {!r})".format(*self.as_tuple())


class KnowledgeNet:
    """Directed labelled graph of facts with indexed queries."""

    def __init__(self) -> None:
        self._facts: set = set()
        self._by_subject: dict = defaultdict(list)
        self._by_object: dict = defaultdict(list)

    def add(self, subject: str, predicate: str, obj: str) -> bool:
        """Add an edge; returns False if it already exists."""
        fact = Fact(subject, predicate, obj)
        if fact in self._facts:
            return False
        self._facts.add(fact)
        self._by_subject[fact.subject].append(fact)
        self._by_object[fact.object].append(fact)
        return True

    def facts(self):
        return sorted(self._facts, key=lambda f: f.as_tuple())

    def __len__(self) -> int:
        return len(self._facts)

    def query(self, subject=None, predicate=None, obj=None):
        """Return edges matching the given pattern (None = wildcard)."""
        results = self._facts
        if subject is not None:
            results = [f for f in results if f.subject == subject]
        if predicate is not None:
            results = [f for f in results if f.predicate == predicate]
        if obj is not None:
            results = [f for f in results if f.object == obj]
        return sorted(results, key=lambda f: f.as_tuple())

    def chain(self, start: str, predicate: str, max_hops: int = 4) -> list:
        """Multi-hop walk following ``predicate`` from ``start``."""
        if max_hops < 1:
            raise ValueError("max_hops must be >= 1")
        hops = []
        current = start
        seen = {start}
        for _ in range(max_hops):
            nxt = [f.object for f in self._by_subject.get(current, []) if f.predicate == predicate]
            if not nxt:
                break
            hops.append(nxt[0])
            if nxt[0] in seen:
                break
            seen.add(nxt[0])
            current = nxt[0]
        return hops

    def nodes(self) -> list:
        """Sorted list of distinct nodes (subjects and objects)."""
        return sorted({f.subject for f in self._facts} | {f.object for f in self._facts})

    def edges(self) -> list:
        """All edges as sorted (subject, predicate, object) tuples."""
        return [f.as_tuple() for f in self.facts()]

    def degree(self, node: str) -> int:
        """Number of edges touching ``node`` (in + out)."""
        return len(self._by_subject.get(node, [])) + len(self._by_object.get(node, []))

    def neighbors(self, node: str, predicate=None) -> list:
        """Sorted nodes adjacent to ``node``, optionally filtered by predicate."""
        nbrs: set = set()
        for f in self._by_subject.get(node, []):
            if predicate is None or f.predicate == predicate:
                nbrs.add(f.object)
        for f in self._by_object.get(node, []):
            if predicate is None or f.predicate == predicate:
                nbrs.add(f.subject)
        return sorted(nbrs)
