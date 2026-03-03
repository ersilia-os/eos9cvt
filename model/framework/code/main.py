import os
import sys
import csv

import torch
import numpy as np
from chemprop import data, featurizers, models, nn

# Parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Paths
root = os.path.dirname(os.path.abspath(__file__))
checkpoints_dir = os.path.join(root, "..", "..", "checkpoints")
model_path = os.path.join(checkpoints_dir, "model.pt")

# Load checkpoint and reconstruct model
ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
state_dict = ckpt["state_dict"]

mean = state_dict["predictor.output_transform.mean"].squeeze()
scale = state_dict["predictor.output_transform.scale"].squeeze()

mp = nn.BondMessagePassing(d_h=300, depth=3)
agg = nn.MeanAggregation()
output_transform = nn.UnscaleTransform(mean=mean, scale=scale)
ffn = nn.RegressionFFN(
    input_dim=300,
    hidden_dim=300,
    n_layers=1,
    n_tasks=4,
    output_transform=output_transform,
)
model = models.MPNN(mp, agg, ffn)
model.load_state_dict(state_dict)
model.eval()

# Read input
with open(input_file, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    smiles = [r[0] for r in reader]

# Run predictions
test_data = [data.MoleculeDatapoint.from_smi(s) for s in smiles]
feat = featurizers.SimpleMoleculeMolGraphFeaturizer()
test_dset = data.MoleculeDataset(test_data, feat)
test_loader = data.build_dataloader(test_dset, shuffle=False)
all_preds = []
with torch.inference_mode():
    for batch in test_loader:
        bmg = batch.bmg
        preds = model(bmg)
        all_preds.append(preds.numpy())
        print(preds.numpy())

all_preds = np.concatenate(all_preds, axis=0)

# Write output
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["caco2_er", "caco2_papp", "mdck_er", "nih_mdck_er"])
    for row in all_preds:
        writer.writerow([round(float(v), 6) for v in row])