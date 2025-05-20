"""
core/gnn_disambiguator.py

Graph Neural Network (GNN) disambiguator for Azerbaijani morphological analysis.
This module takes FST candidate analyses and selects the most probable one using context and learned patterns.
"""
import torch
import torch.nn as nn
from torch_geometric.data import Data, Batch
from typing import List, Dict, Any

class MorphoGNN(nn.Module):
    def __init__(self, num_morph_tags: int, hidden_dim: int = 64):
        super().__init__()
        from torch_geometric.nn import GCNConv
        self.embedding = nn.Embedding(num_morph_tags, hidden_dim)
        self.conv1 = GCNConv(hidden_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, 1)  # Output: score for each candidate

    def forward(self, x, edge_index):
        x = self.embedding(x)
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index).relu()
        x = self.fc(x)
        return x.squeeze(-1)  # (num_nodes,)

class GNNDisambiguator:
    """
    Loads a trained MorphoGNN and predicts the best analysis for a word in context.
    """
    def __init__(self, tag_vocab: Dict[str, int], model_path: str = None):
        self.tag_vocab = tag_vocab
        self.model = MorphoGNN(num_morph_tags=len(tag_vocab))
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()

    def build_graph(self, analyses: List[Dict[str, Any]], context: List[str] = None) -> Data:
        """
        Build a PyG graph from FST analyses and (optionally) context.
        Each candidate analysis is a node; edges can encode context or candidate similarity.
        """
        x = torch.tensor([self.encode_tags(a['tags']) for a in analyses], dtype=torch.long)
        edge_index = self.make_fully_connected(len(analyses))
        return Data(x=x, edge_index=edge_index)

    def encode_tags(self, tags: List[str]) -> int:
        # For simplicity, use the first tag (e.g., POS); can be extended for multi-hot encoding
        return self.tag_vocab.get(tags[0], 0)

    def make_fully_connected(self, n: int):
        import torch
        row = torch.arange(n).repeat_interleave(n)
        col = torch.arange(n).repeat(n)
        edge_index = torch.stack([row, col], dim=0)
        return edge_index

    def disambiguate(self, analyses: List[Dict[str, Any]], context: List[str] = None) -> Dict[str, Any]:
        """
        Given candidate analyses, return the most probable one.
        """
        graph = self.build_graph(analyses, context)
        with torch.no_grad():
            scores = self.model(graph.x, graph.edge_index)
        best_idx = scores.argmax().item()
        return analyses[best_idx]

# Example usage (with dummy tag vocab):
# tag_vocab = {"VERB": 0, "NOUN": 1, "ADJ": 2, "PLUR": 3, ...}
# gnn = GNNDisambiguator(tag_vocab)
# best = gnn.disambiguate(fst_analyses)
