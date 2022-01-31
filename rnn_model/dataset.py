import numpy as np
from torch.utils.data import Dataset, DataLoader
import random
from copy import deepcopy

random.seed(5)

class TimeSeriesDataset(Dataset):
    def __init__(self, x, y):
        x = np.expand_dims(x, 2)
        self.x = x.astype(np.float32)
        self.y = y.astype(np.float32)
        
    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return (self.x[idx], self.y[idx])


def prepare_data(data_file):
    with open(data_file) as fh:
        lines = fh.readlines()
        lines = [l.strip().split("\t") for l in lines]
    random.shuffle(lines)
    y = [float(z[-1]) for z in lines]
    x = []
    for z in lines:
        z_float = [float(num) for num in z[1:-1]]
        x.append(z_float)
    train_x = np.asarray(x[:135])
    test_x = np.asarray(x[:135])
    train_y = np.asarray(y[-135:])
    test_y = np.asarray(y[-135:])

    train_dataset = TimeSeriesDataset(train_x,train_y)
    test_dataset = TimeSeriesDataset(test_x,test_y)

    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    return train_dataloader, test_dataloader

    


