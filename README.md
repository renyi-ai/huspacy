
[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/spacy-hu/spacy-hungarian-models)
[![spacy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/huspacy)
[![PyPI version](https://badge.fury.io/py/huspacy.svg)](https://pypi.org/project/huspacy/)
[![license](https://img.shields.io/github/license/spacy-hu/spacy-hungarian-models)](https://github.com/spacy-hu/spacy-hungarian-models/blob/master/LICENSE)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fspacy-hu%2Fspacy-hungarian-models&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true)](https://hits.seeyoufarm.com)
[![pip downloads](https://img.shields.io/pypi/dm/huspacy.svg)](https://pypi.org/project/huspacy/)
[![Demo](https://img.shields.io/badge/Try%20the-Demo-important)](https://huggingface.co/spaces/huspacy/demo)
[![stars](https://img.shields.io/github/stars/spacy-hu/spacy-hungarian-models?style=social)](https://github.com/spacy-hu/spacy-hungarian-models)


# HuSpaCy: Industrial-strength Hungarian NLP

HuSpaCy is a [spaCy](https://spacy.io) model and library providing industrial-strength Hungarian language processing facilities. A live demo is available [here](https://huggingface.co/spaces/huspacy/demo). This repository contain material to build the models for HuSpaCy.

## Installation

To get started using the latest Hungarian model, you can fetch the model by installing `huspacy` from PyPI:

```bash
pip install huspacy
```

This should be followed by the model download:

```python
import huspacy

huspacy.download()
```

Alternatively, one can install the latest models directly from Hugging Face Hub:

```bash
pip install https://huggingface.co/huspacy/hu_core_news_lg/resolve/main/hu_core_news_lg-any-py3-none-any.whl
```


To speed up inference, you might want to run the models on GPU for which you need to add CUDA support for spacy as described in [here](https://spacy.io/usage).

## Usage

```python
# Load the model through huspacy
import huspacy
huspacy.load()

# Load the mode using spacy.load().
import spacy
nlp = spacy.load("hu_core_news_lg")

# Or load the model directly as a module.
import hu_core_news_lg
nlp = hu_core_news_lg.load()

# Either way you get the same model and can start processing your texts.
doc = nlp('Csiribiri csiribiri zabszalma - négy csillag közt alszom ma.')
```

For a detailed guide on usage, check [spaCy's documentation](https://spacy.io/usage/linguistic-features).

## Available Models 

Currently, we only support a single large model which has a good balance between accuracy and speed. You can play around with the tool capabilities in this [interactive demo](https://huggingface.co/spaces/huspacy/demo).

[`hu_core_news_lg`](https://huggingface.co/huspacy/hu_core_news_lg) provides tokenization, sentence splitting, part-of-speech tagging (UD labels w/ detailed morphosyntactic features), lemmatization, dependency parsing and named entity recognition and ships with pretrained word vectors.

Models' changes are recorded in the [changelog](https://github.com/spacy-hu/spacy-hungarian-models/blob/master/CHANGELOG.md).

## Development
 
### Installing requirements

- `poetry install` will install all the dependencies
- For better performance you might need to [reinstall spacy with GPU support](https://spacy.io/usage), e.g. `poetry add spacy[cuda92]` will add support for CUDA 9.2 

### Repository structure

```
├── .github            -- Github configuration files
├── data               -- Data files
│   ├── external       -- External models required to train models (e.g. word vectors)
│   ├── processed      -- Processed data ready to feed spacy
│   └── raw            -- Raw data, mostly corpora as they are obtained from the web
├── hu_core_news_lg    -- Spacy 3.x project files for building a model for news texts
│   ├── configs        -- Spacy pipeline configuration files
│   ├── project.lock               -- Auto-generated project script
│   ├── project.yml                -- Spacy3 Project file describing steps needed to build the model
│   └── README.md                  -- Instructions on building a model from scratch
├── huspacy            -- subproject for the PyPI distributable package
├── tools              -- Source package for tools
│   └── cli            -- Command line scripts (Python)
├── models             -- Trained models and their metadata
├── resources          -- Resource files
├── scripts            -- Bash scripts
├── tests              -- Test files 
├── CHANGELOG.md       -- Keeps the changelog
├── LICENSE            -- License file
├── poetry.lock        -- Locked poetry dependencies files
├── poetry.toml        -- Poetry configurations
├── pyproject.toml     -- Python project configutation, including dependencies managed with Poetry 
└── README.md          -- This file
```

## Citing

If you use the models or this library in your research please cite this [paper]().</br>
Additionally, please indicate the version of the model you used so that your research can be reproduced.

<!--
```bibtex
@misc{HuSpaCy:2021,
  title = {{HuSpaCy: industrial strength Hungarian natural language processing}},
  booktitle = {{XVIII. Magyar Sz\'{a}m\'{\i}t\'{o}g\'{e}pes Nyelv\'{e}szeti Konferencia}},
  author = {Orosz, Gy\"{o}rgy and Sz\'{a}nt\'{o}, Zsolt and Berkecz, Péter and Szabó, Gergő and Tóth, Bálint and Farkas, Rich\'{a}rd}, 
  year = {forthcoming 2021},
}
```
-->

## License

This library is released under the Apache 2.0 License. See the [`LICENSE`](https://github.com/spacy-hu/spacy-hungarian-models/blob/master/LICENSE) file for more details.

The trained models have their own license as described on the [models hub](https://huggingface.co/spacy-hu/hu_core_news_lg).

## Contact
For feature request issues and bugs please use the [GitHub Issue Tracker](https://github.com/spacy-hu/spacy-hungarian-models/issues). Otherwise, please use the [Discussion Forums](https://github.com/spacy-hu/spacy-hungarian-models/discussions).

## Acknowledgments

The project was supported by the Ministry of Innovation and Technology NRDI Office within the framework of the Artificial Intelligence National Laboratory Program.
