"""
scripts/grid_search_gnn.py

Automated grid search for GNN hyperparameter tuning.
"""
import itertools
import subprocess
import json
import os
import logging

def run_train(params: dict, data: str, tag_vocab: str, out_dir: str) -> str:
    """
    Run training subprocess with specified parameters. Logs command and errors.
    """
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
    logging.info(f'Running: {" ".join(cmd)}')
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        logging.info(f"stdout: {result.stdout}")
        if result.stderr:
            logging.warning(f"stderr: {result.stderr}")
    except Exception as e:
        logging.error(f"Failed to run training subprocess: {e}")
    return out_path

def main():
    """
    Perform grid search over GNN hyperparameters. Logs progress and errors.
    """
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
    for params in itertools.product(*param_grid.values()):
        param_dict = dict(zip(param_grid.keys(), params))
        logging.info(f"Testing params: {param_dict}")
        run_train(param_dict, data, tag_vocab, out_dir)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
