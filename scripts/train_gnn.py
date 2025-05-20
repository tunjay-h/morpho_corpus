"""
scripts/train_gnn.py

Example script for training the MorphoGNN disambiguator on annotated FST candidate data.
"""
import torch
from torch_geometric.data import Data, DataLoader
from core.gnn_disambiguator import MorphoGNN
import json, os
from typing import List, Dict

def load_tag_vocab(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_examples(data_path: str, tag_vocab: Dict[str, int]):
    """
    Load training examples from JSONL. Each line: {"analyses": [...], "gold_idx": int}
    Returns list of (graph, gold_idx).
    """
    from core.gnn_disambiguator import GNNDisambiguator
    examples = []
    with open(data_path, encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            gnn = GNNDisambiguator(tag_vocab)
            graph = gnn.build_graph(item['analyses'])
            graph.y = torch.tensor([item['gold_idx']], dtype=torch.long)
            examples.append(graph)
    return examples

def train(model, train_loader, val_loader=None, epochs=10, lr=1e-3):
    """Train the MorphoGNN model with logging."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            out = model(batch.x, batch.edge_index)
            loss = loss_fn(out.unsqueeze(0), batch.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        logging.info(f"Epoch {epoch+1}: Train Loss {total_loss/len(train_loader):.4f}")
        if val_loader:
            model.eval()
            correct = 0
            total = 0
            with torch.no_grad():
                for batch in val_loader:
                    out = model(batch.x, batch.edge_index)
                    pred = out.argmax().item()
                    if pred == batch.y.item():
                        correct += 1
                    total += 1
            logging.info(f"  Validation Accuracy: {100.0 * correct / max(1,total):.2f}%")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Path to training data (JSONL)')
    parser.add_argument('--tag_vocab', required=True, help='Path to tag vocab JSON')
    parser.add_argument('--out', required=True, help='Path to save model')
    parser.add_argument('--hidden_dim', type=int, default=64, help='Hidden dimension of the model')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--batch_size', type=int, default=1, help='Batch size')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs')
    parser.add_argument('--val_split', type=float, default=0.2, help='Validation split proportion')
    args = parser.parse_args()

    tag_vocab = load_tag_vocab(args.tag_vocab)
    examples = load_examples(args.data, tag_vocab)
    # Split into train/val
    from torch.utils.data import random_split
    n_total = len(examples)
    n_val = int(n_total * args.val_split)
    n_train = n_total - n_val
    train_set, val_set = random_split(examples, [n_train, n_val])
    from torch_geometric.data import DataLoader
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=1, shuffle=False) if n_val > 0 else None
    model = MorphoGNN(num_morph_tags=len(tag_vocab), hidden_dim=args.hidden_dim)
    train(model, train_loader, val_loader=val_loader, epochs=args.epochs, lr=args.lr)
    torch.save(model.state_dict(), args.out)
