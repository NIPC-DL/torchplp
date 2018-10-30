# Covec
Covec is the collections of popular datasets and process methods for program analysis liks torchvision for visions.  
This is a very early vision, just use it carefully.   

# Install
From source:
```bash
python setup.py install
```

# Dependence
- Python ≥ 3.6
- clang ≥ 6.0

# Datasets
- [SySeVR](https://github.com/SySeVR/SySeVR)
- **TODO** [Juliet Test Suite](https://samate.nist.gov/SRD/testsuite.php)

# Processor
- Text Model: NLP like process methods, based on [arXiv:1807.06756](https://arxiv.org/abs/1807.06756)
- **TODO** Tree Model: AST based process methods

# Usage
```python
from covec.datasets import SySeVR
from covec.processor import TextModel, Word2Vec
from torch.utils.data import DataLoader

# create a words embedding model for processor
embedder = Word2Vec(size=20, min_count=1, workers=12) 
# create a processor object to transform data in vector representation
processor = TextModel(embedder) 
# create dataset and only use API Function Call data
dataset = SySeVR('~/WorkSpace/Test/', processor, category=['AF'])
# get train and valid datasets for 10 folds validation
train, valid = dataset.torchset(10)
# create dataloader for training
train_loader = DataLoader(train, batch_size=50)
valid_loader = DataLoader(valid, batch_size=50)
```