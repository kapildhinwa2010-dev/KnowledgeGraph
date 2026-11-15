import pytest

from knowledgegraph import Fact, KnowledgeNet


def test_fact_basic():
    fact = Fact("alice", "knows", "bob")
    assert fact.as_tuple() == ("alice", "knows", "bob")


def test_fact_rejects_empty():
    with pytest.raises(ValueError):
        Fact("", "knows", "bob")


def test_add_and_len():
    net = KnowledgeNet()
    assert net.add("a", "knows", "b") is True
    assert net.add("a", "knows", "b") is False
    assert len(net) == 1


def test_query_pattern():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("b", "knows", "c")
    assert len(net.query(subject="a")) == 1
    assert len(net.query(predicate="knows")) == 2


def test_chain_walk():
    net = KnowledgeNet()
    net.add("a", "next", "b")
    net.add("b", "next", "c")
    assert net.chain("a", "next") == ["b", "c"]


# --- graph operations (KnowledgeGraph-specific) ---


def test_nodes_deduplicated_and_sorted():
    net = KnowledgeNet()
    net.add("b", "knows", "a")
    net.add("a", "knows", "c")
    assert net.nodes() == ["a", "b", "c"]


def test_edges_sorted_tuples():
    net = KnowledgeNet()
    net.add("b", "knows", "a")
    net.add("a", "likes", "c")
    assert net.edges() == [("a", "likes", "c"), ("b", "knows", "a")]


def test_degree_in_plus_out():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("c", "knows", "a")
    net.add("a", "likes", "d")
    assert net.degree("a") == 3
    assert net.degree("b") == 1
    assert net.degree("zzz") == 0


def test_neighbors_both_directions():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("c", "knows", "a")
    assert net.neighbors("a") == ["b", "c"]


def test_neighbors_filtered_by_predicate():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("a", "likes", "c")
    assert net.neighbors("a", predicate="likes") == ["c"]


def test_neighbors_empty():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    assert net.neighbors("zzz") == []