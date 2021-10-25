import numpy as np
import pandas as pd
import re
import torch
import random
import torch.nn as nn
import transformers
import matplotlib.pyplot as plt  # specify GPU
device = torch.device('cuda')


df = pd.read_excel('datasets/hello.xlsx')
print(df.head())
