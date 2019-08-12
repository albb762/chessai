import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.utils.data import Dataset, DataLoader
import torch



class pgnDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, npz_file):

        train_set = np.load(npz_file)
        self.X = train_set['arr_0']
        y = train_set['arr_1']
        self.Y = y.reshape(-1,1)

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx],self.Y[idx]


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.a1 = nn.Conv2d(5, 16, kernel_size=3, padding=1)
        self.a2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
        self.a3 = nn.Conv2d(16, 32, kernel_size=3, stride=2)

        self.b1 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(32, 64, kernel_size=3, stride=2)

        self.c1 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c2 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c3 = nn.Conv2d(64, 128, kernel_size=2, stride=2)

        self.d1 = nn.Conv2d(128, 128, kernel_size=1)
        self.d2 = nn.Conv2d(128, 128, kernel_size=1)
        self.d3 = nn.Conv2d(128, 128, kernel_size=1)

        self.last = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.a1(x))
        x = F.relu(self.a2(x))
        x = F.relu(self.a3(x))

        # 4x4
        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))

        # 2x2
        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))
        x = F.relu(self.c3(x))

        # 1x128
        x = F.relu(self.d1(x))
        x = F.relu(self.d2(x))
        x = F.relu(self.d3(x))

        x = x.view(-1, 128)
        x = self.last(x)

        # value output
        return torch.tanh(x)

if __name__ == '__main__':
    data = pgnDataset('train_data_10000.npy.npz')
    print(data.__len__())
    trainloader = torch.utils.data.DataLoader(data, batch_size=16,shuffle=True, num_workers=2)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    net = Net().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters())
    net.train()
    for epoch in range(100):  # loop over the dataset multiple times

         running_loss = 0.0
         for i, (inputs,labels) in enumerate(trainloader):
             # get the inputs; data is a list of [inputs, labels]
             inputs,labels= inputs.float().to(device),labels.float().to(device)
       
             # zero the parameter gradients
             optimizer.zero_grad()

             # forward + backward + optimize
             outputs = net(inputs)
             loss = criterion(outputs, labels)
             loss.backward()
             optimizer.step()
             
             
             # print statistics
             running_loss += loss.item()
             if i % 200 == 199:    # print every 2000 mini-batches
                 print('[%d, %5d] loss: %.3f' %
                       (epoch + 1, i + 1, running_loss / 2000))
                 running_loss = 0.0
    torch.save(net.state_dict(),'nets/values.pth') 
    print('Finished Training')


