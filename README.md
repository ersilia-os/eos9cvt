# Permeability and Efflux Prediction (GNN-MTL)

Predicts cell membrane permeability and efflux transport using a multitask   graph neural network. The model simultaneously predicts four endpoints:   Caco-2 efflux ratio (ER), Caco-2 apparent permeability (P\_app), MDCK ER, and NIH-MDCK ER. Built with Chemprop v2.1 using a message-passing neural   network (MPNN) trained on a harmonized single-laboratory dataset of over   10, 000 compounds from Caco-2 and MDCK cell-line assays.

This model was incorporated on 2026-02-23.Last packaged on 2026-03-03.

## Information
### Identifiers
- **Ersilia Identifier:** `eos9cvt`
- **Slug:** `permeability-efflux-mtl`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Property calculation or prediction`
- **Biomedical Area:** `ADMET`
- **Target Organism:** `Homo sapiens`
- **Tags:** `ADME`, `Permeability`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `4`
- **Output Consistency:** `Fixed`
- **Interpretation:** The output of this template model should be interpreted like this.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| caco2_er | float | high | Predicted log10 Caco-2 efflux ratio. Values >log10(2)=0.30 suggest active efflux |
| caco2_papp | float | high | Predicted log10 Caco-2 apparent permeability (x10^-6 cm/s). Higher means more permeable |
| mdck_er | float | high | Predicted log10 MDCK efflux ratio. Values >log10(2)=0.30 suggest active efflux |
| nih_mdck_er | float | high | Predicted log10 NIH-MDCK efflux ratio. Values >log10(2)=0.30 suggest active efflux |


### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos9cvt](https://hub.docker.com/r/ersiliaos/eos9cvt)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos9cvt.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos9cvt.zip)

### Resource Consumption
- **Model Size (Mb):** `3`
- **Environment Size (Mb):** `7878`
- **Image Size (Mb):** `7757.89`

**Computational Performance (seconds):**
- 10 inputs: `40.62`
- 100 inputs: `28.23`
- 10000 inputs: `290.58`

### References
- **Source Code**: [https://github.com/chemprop/chemprop](https://github.com/chemprop/chemprop)
- **Publication**: [https://doi.org/10.1021/acsomega.5c04861](https://doi.org/10.1021/acsomega.5c04861)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2025`
- **Ersilia Contributor:** [Marina18](https://github.com/Marina18)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [Apache-2.0](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos9cvt
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos9cvt
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
