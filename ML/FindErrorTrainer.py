import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch import device, optim
from transformers import AutoModel, BertTokenizerFast, AdamW
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import AutoModel, BertTokenizerFast, AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
import mlflow


device = 'cuda' if torch.cuda.is_available() else 'cpu'

bert = AutoModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
max_seq_len = 512


class BERT_Arch(nn.Module):
    def __init__(self,bert):
        super(BERT_Arch,self).__init__()
        self.bert = bert
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(768, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 2)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self,sent_id, mask,return_dict):
        _,cls_hs = self.bert(sent_id,attention_mask=mask,return_dict=False)
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.softmax(x)
        return x

model = BERT_Arch(bert).to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-5)
class_wts = compute_class_weight(class_weight='balcnced',classes=np.unique())

