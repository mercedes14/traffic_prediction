
import torch
from dataset import prepare_data
from lstm_model import LSTM
import torch.nn as nn
import torch.optim as optim

def run_epoch(model, optimiser, criterion,  dataloader):
    model.train()
    epoch_loss = 0
    for idx, (x, y) in enumerate(dataloader):
        batchsize = x.shape[0]
        optimiser.zero_grad()
        out = model(x)
        loss = criterion(out.contiguous(), y.contiguous())
        loss.backward()
        optimiser.step()
        epoch_loss += (loss.detach().item() / batchsize)
    return epoch_loss

def eval_model(model, criterion,  dataloader):
    model.eval()
    epoch_loss = 0
    for idx, (x, y) in enumerate(dataloader):
        batchsize = x.shape[0]
        out = model(x)
        loss = criterion(out.contiguous(), y.contiguous())
        epoch_loss += (loss.detach().item() / batchsize)
    return epoch_loss

def main():
    train_data, test_data = prepare_data('rnn_dataset.txt')
    model = LSTM(input_dim=1,hidden_dim=4,num_layers=32,output_dim=1)
    loss = nn.MSELoss()
    optimiser = optim.Adam(model.parameters(), lr=0.008 , betas=(0.9, 0.98), eps=1e-9)
    scheduler = optim.lr_scheduler.StepLR(optimiser, step_size=35, gamma=0.1)
    for i in range(100):
        train_loss = run_epoch(model,optimiser,loss,train_data)
        print(f"Training Loss for epoch {i+1} : {train_loss}")
        test_loss = eval_model(model,loss,test_data)
        if i%20 == 0:
            print(f"Eval Loss for epoch {i+1} : {test_loss}")
        scheduler.step()
    torch.save(model.state_dict(), "rnn_model.pth")
main()
