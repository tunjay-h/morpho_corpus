"""
scripts/grid_search_gnn.py

Automated grid search for GNN hyperparameter tuning.
"""
import itertools
import subprocess
import json
import os

def run_train(params, data, tag_vocab, out_dir):
    out_path = os.path.join(out_dir, f"model_hd{params['hidden_dim']}_lr{params['lr']}_bs{params['batch_size']}.pt")
    cmd = [
        'python', 'scripts/train_gnn.py',
        '--data', data,
        '--tag_vocab', tag_vocab,
        '--out', out_path,
        '--hidden_dim', str(params['hidden_dim']),
        '--lr', str(params['lr']),
        '--batch_size', str(params['batch_size']),
        '--epochs', str(params['epochs']),
        '--val_split', str(params['val_split'])
    ]
    print('Running:', ' '.join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return out_path

def main():
    param_grid = {
        'hidden_dim': [32, 64],
        'lr': [1e-2, 1e-3],
        'batch_size': [1, 4],
        'epochs': [10],
        'val_split': [0.2]
    }
    data = 'data/gnn_train.jsonl'
    tag_vocab = 'data/tag_vocab.json'
    out_dir = 'models/'
    os.makedirs(out_dir, exist_ok=True)
    for combo in itertools.product(*param_grid.values()):
        params = dict(zip(param_grid.keys(), combo))
        run_train(params, data, tag_vocab, out_dir)

if __name__ == "__main__":
    main()
