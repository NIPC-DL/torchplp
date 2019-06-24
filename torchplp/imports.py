# -*- coding: utf-8 -*-
"""
imports.py - Contains common imports

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
#for type annotations
from numbers import Number
from typing import Any, AnyStr, Callable, Collection, Dict, Hashable, Iterator, List, Mapping, NewType, Optional
from typing import Sequence, Tuple, TypeVar, Union
from types import SimpleNamespace
# pytorch
import torch
import torch.nn as nn
# others
import numpy as np
import pandas as pd
import clang.cindex as cc
# torchplp
from torchplp.utils.astree import ASTNode
