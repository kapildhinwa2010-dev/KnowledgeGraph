import pytest
import torch
from knowledgegraph import KnowledgeGraph, create_knowledgegraph

class TestKnowledgeGraph:
    def test_init(self):
        m = KnowledgeGraph(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = KnowledgeGraph(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_knowledgegraph()
        assert isinstance(m, KnowledgeGraph)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
