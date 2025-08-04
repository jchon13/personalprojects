import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms

#torch.set_grad_enabled(True)

torch.set_printoptions(linewidth=120)

#Gets number of correct predictions
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

train_loader = torch.utils.data.DataLoader(train_set,batch_size=100)
batch = next(iter(train_loader))
images, labels = batch

#Calculating Loss
preds = network(images)
loss = F.cross_entropy(preds,labels) #calculates loss
print('initial loss:',loss.item())

#Calculating gradient
#print(network.conv1.weight.grad)
loss.backward()
#print(network.conv1.weight.grad)

#Updating Weights
optimizer = optim.Adam(network.parameters(),lr=0.01) #can use optim.SGD
print(get_num_correct(preds,labels))
optimizer.step() #Updating weights
preds = network(images)
loss = F.cross_entropy(preds,labels)
print(loss.item())
print(get_num_correct(preds,labels))


#Essentially 

'''#
network = Network()

train_loader = torch.utils.data.DataLoader(train_set,batch_size=100)
optimizer = optim.Adam(network.parameters(),lr=0.01)

batch = next(iter(train_loader)) # Get Batch
images, labels = batch

preds = network(images) #Pass Batch
loss = F.cross_entropy(preds,labels) #calculates loss

loss.backward() #Calculating gradient
optimizer.step() #Updating weights
#'''