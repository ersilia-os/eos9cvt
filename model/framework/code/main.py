import os
import sys
import csv

import numpy as np
import torch
from rdkit import Chem
from chemprop import data, featurizers, models, nn

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# load checkpoint and reconstruct model
checkpoints_dir = os.path.join(root, "..", "..", "checkpoints")
model_path = os.path.join(checkpoints_dir, "model.pt")

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
_model = models.MPNN(mp, agg, ffn)
_model.load_state_dict(state_dict)
_model.eval()

N_TASKS = 4


# my model: takes a list of SMILES and returns predictions for 4 endpoints
# invalid SMILES produce a row of NaN
def my_model(smiles_list):
    results = np.full((len(smiles_list), N_TASKS), float("nan"))

    valid_indices, valid_smiles = [], []
    for i, smi in enumerate(smiles_list):
        if Chem.MolFromSmiles(smi) is not None:
            valid_indices.append(i)
            valid_smiles.append(smi)

    if not valid_smiles:
        return results.tolist()

    test_data = [data.MoleculeDatapoint.from_smi(s) for s in valid_smiles]
    feat = featurizers.SimpleMoleculeMolGraphFeaturizer()
    test_dset = data.MoleculeDataset(test_data, feat)
    test_loader = data.build_dataloader(test_dset, shuffle=False, drop_last=False)

    preds_list = []
    with torch.inference_mode():
        for batch in test_loader:
            preds_list.append(_model(batch.bmg).numpy())

    valid_preds = np.concatenate(preds_list, axis=0)
    for i, idx in enumerate(valid_indices):
        results[idx] = valid_preds[i]

    return results.tolist()


# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    smiles_list = [r[0] for r in reader]

# run model
outputs = my_model(smiles_list)

# check input and output have the same length
input_len = len(smiles_list)
output_len = len(outputs)
assert input_len == output_len

# write output in a .csv file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["caco2_er", "caco2_papp", "mdck_er", "nih_mdck_er"])
    for row in outputs:
        writer.writerow(["" if np.isnan(float(v)) else round(float(v), 6) for v in row])
