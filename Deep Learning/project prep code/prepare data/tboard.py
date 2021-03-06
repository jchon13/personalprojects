from matplotlib.pyplot import grid
from numpy import int32
from sklearn.utils import shuffle
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms

from torch.utils.tensorboard import SummaryWriter


torch.set_printoptions(linewidth=120)

def get_num_correct(predictions,labels):
    return predictions.argmax(dim=1).eq(labels).sum().item()

class Network(nn.Module):
    def __init__(self):
        super(Network,self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1,out_channels=6,kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=6,out_channels=12,kernel_size=5)

        self.fc1 = nn.Linear(in_features=12*4*4, out_features=120) 
        self.fc2 = nn.Linear(in_features=120, out_features=60)
        self.out = nn.Linear(in_features=60, out_features=10)#Fully connected/linear layer


    def forward(self,t):
        #1 input layer
        t=t

        #2 hidden convolutional layer
        t = self.conv1(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2,stride = 2)

        # 3 hidden conv layer 2, comprised of collection of weights and operations
        # Weights are stored in neural network modular layer class instance
        t = self.conv2(t)
        t = F.relu(t) #pure operation, no Weights, activation
        t = F.max_pool2d(t, kernel_size=2,stride = 2) #pure operation, no Weights

        # 4 Linear Layer
        t = t.reshape(-1,12*4*4) #4 by 4 is the height and width 
        t = self.fc1(t)
        t = F.relu(t)

        # 5 Linear layer
        t = self.fc2(t)
        t = F.relu(t)

        # 6 Linear Layer
        t = self.out(t)
        #t = F.softmax(t,dim=1)

        return t

train_set = torchvision.datasets.FashionMNIST(
    root ='./data/FashionMNIST'
    ,train=True
    ,download=True
    ,transform=transforms.Compose([transforms.ToTensor()
    ])
)

network = Network()

train_loader = torch.utils.data.DataLoader(train_set, batch_size=100)
optimizer = optim.Adam(network.parameters(),lr=0.01)





for epoch in range(5):
    all_predictions = torch.tensor([])
    total_loss = 0 
    total_correct = 0

    for batch in train_loader:

        images, labels = batch

        preds = network(images)
        loss= F.cross_entropy(preds,labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        total_correct += get_num_correct(preds,labels)

        all_predictions = torch.cat(
            (all_predictions, preds),dim=0
        )
    

    print("epoch:",epoch +1 ,"total_correct:",total_correct,"total_loss:",total_loss)
    
    





@torch.no_grad()
def get_all_predictions(model,loader):
    all_predictions = torch.tensor([])
    for batch in loader:
        images,labels = batch

        predictions = model(images)
        all_predictions = torch.cat(
            (all_predictions, predictions),dim=0
        )
    return all_predictions


#print(train_predictions.shape)

#with torch.no_grad(): #locally turn off gradient tracking, uses less memory
prediction_loader = torch.utils.data.DataLoader(train_set,batch_size=1000)
#train_predictions = get_all_predictions(network,prediction_loader)

#Building confusion matrix
stacked = torch.stack(
    (
        train_set.targets
        ,all_predictions.argmax(dim=1) 
        #built into training loop, the all_predictions var
    )
    ,dim=1
)

cmt = torch.zeros(10,10,dtype=torch.int32)

for p in stacked:
    j, k = p.tolist()
    cmt[j,k]=cmt[j,k]+1

print(cmt)