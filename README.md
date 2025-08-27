# CMPS 455 - Computational Aspects of Game Programming

## Setup

To create an environment for this project via BASH:
```bash
conda env create -f environment.yml
```

To update an existing environment:
```bash
conda env update --file environment.yml
```

Alternatively, to make conda remove packages that are not listed in the `environment.yml` file when updating the environment with required packages:
```bash
conda env update --file environment.yml --prune
```

If it is desired to create a new `environment.yml` file, it should be placed at the root of the project directory. Below lists an example to demonstrate the format of the file:
```yaml
name: my_new_env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy
  - pandas
  - pip
  - pip:
    - scikit-learn
    - notebook
```
