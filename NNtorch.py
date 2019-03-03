import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch import optim
import os


class ChessValueDataset(Dataset):
    def __init__(self, path):

        data = np.load(path)
        self.inputs = data['arr_0']
        self.targets = data['arr_1']

        print("loaded ", self.inputs.shape, self.targets.shape)

    def __len__(self):
        return self.inputs.shape[0]

    def __getitem__(self, item):
        return self.inputs[item], self.targets[item]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.input_layer = nn.Conv2d(20, 128, kernel_size=3, stride=1, padding=1)
        self.hidden_layer1 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1)
        self.hidden_layer2 = nn.Conv2d(128, 64, kernel_size=3, stride=2, padding=1)

        self.hidden_layer3 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.hidden_layer4 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.hidden_layer5 = nn.Conv2d(64, 32, kernel_size=3, stride=2)

        self.hidden_layer6 = nn.Conv2d(32, 32, kernel_size=2, padding=1)
        self.hidden_layer7 = nn.Conv2d(32, 32, kernel_size=2, padding=1)
        self.hidden_layer8 = nn.Conv2d(32, 16, kernel_size=2, stride=2)

        self.hidden_layer9 = nn.Conv2d(16, 16, kernel_size=1)
        self.hidden_layer10 = nn.Conv2d(16, 16, kernel_size=1)
        self.hidden_layer11 = nn.Conv2d(16, 16, kernel_size=1)

        self.output_layer = nn.Linear(16, 1)

    def forward(self, input):
        input = F.relu(self.input_layer(input))
        input = F.relu(self.hidden_layer1(input))
        input = F.relu(self.hidden_layer2(input))
        input = F.relu(self.hidden_layer3(input))
        input = F.relu(self.hidden_layer4(input))
        input = F.relu(self.hidden_layer5(input))
        input = F.relu(self.hidden_layer6(input))
        input = F.relu(self.hidden_layer7(input))
        input = F.relu(self.hidden_layer8(input))
        input = F.relu(self.hidden_layer9(input))
        input = F.relu(self.hidden_layer10(input))
        input = F.relu(self.hidden_layer11(input))
        input = input.view(-1, 16)
        input = self.output_layer(input)

        return torch.tanh(input)


if __name__ == '__main__':
    device = "cuda"

    model = Net()
    optimizer = optim.Adam(model.parameters())
    floss = nn.MSELoss()

    if device == 'cuda':
        model.cuda()

    model.train()

    chess_data = ChessValueDataset("train/train_1.npz")
    train_loader = torch.utils.data.DataLoader(chess_data, batch_size=250, shuffle=True)
    for epoch in range(100):
        for fn in os.listdir("train"):
            path = os.path.join("train", fn)
            chess_data = ChessValueDataset(path)
            all_loss = 0
            num_loss = 0
            for batch_idx, (data, target) in enumerate(train_loader):
                target = target.unsqueeze(-1)
                data, target = data.to(device), target.to(device)
                data = data.float()
                target = target.float()

                optimizer.zero_grad()
                output = model(data)

                loss = floss(output, target)
                loss.backward()
                optimizer.step()
                all_loss += loss.item()
                num_loss += 1
            torch.save(model.state_dict(), "model/model"+str(all_loss/num_loss)+".pth")
            print(epoch, ', ', all_loss/num_loss)
