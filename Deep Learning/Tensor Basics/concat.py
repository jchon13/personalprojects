import torch

t1 = torch.tensor([1,1,1])
t2 = torch.tensor([2,2,2])
t3 = torch.tensor([3,3,3])

t4 = torch.cat((t1,t2,t3),dim=0)
t5 = torch.stack((t1,t2,t3),dim=0)
print('concatenation:',t4)
print("stack:",t5)