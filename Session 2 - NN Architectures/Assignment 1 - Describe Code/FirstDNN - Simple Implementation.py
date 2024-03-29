#%%
# STATUS: 1st Block Complete 

#Setup Block

import torch

import torch.nn as nn 
import torch.nn.functional as F
import torch.optim as optim 
from torchvision import datasets, transforms
#!pip install torchsummary
from torchinfo import summary
from tqdm import tqdm

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
#%%
# 1: Data Loader Block
batch_size = 128

train_loader = torch.utils.data.DataLoader( 
    datasets.MNIST('../data', 
        train=True, download=True, 
        transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])),
    batch_size=batch_size, shuffle=True) # torch.utils.data.DataLoader does batching...
train_loader = tqdm(train_loader)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=False, transform=transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
                    ])),
    batch_size=batch_size, shuffle=True)

# Testing
device = torch.device("cuda") # cuda, cpu, tpu
channels_in, neurons = 1, 1
singleImage = torch.randn(channels_in,28,28)

basicModel = nn.Sequential(
    nn.Conv2d(channels_in,neurons,3)
    )
basicModel(singleImage)

#%%
# Neural Network Block
# RF Formulae: https://share.cleanshot.com/Xw5YtDb7 & https://docs.google.com/spreadsheets/d/1GoGSYCGxL0AUagRUIVULokRRnrvmuQaCBZW-kZEbX8w/edit#gid=0

class FirstDNN(nn.Module): 
    def __init__(self):
        super(FirstDNN, self).__init__()
        self.conv1 = nn.Conv2d(  1,   32, 3, padding= "same") 
        self.conv2 = nn.Conv2d( 32,   64, 3, padding= "same") # 64 different features with (32 Channels for each feature)
        
        self.conv3 = nn.Conv2d( 64,  128, 3, padding= "same")
        self.conv4 = nn.Conv2d(128,  256, 3, padding= "same")
        
        self.conv5 = nn.Conv2d(256,  512, 3)
        self.conv6 = nn.Conv2d(512, 1024, 3)
        self.conv7 = nn.Conv2d(1024,  10, 3)

        self.pool1 = nn.MaxPool2d(2, 2)
        self.pool2 = nn.MaxPool2d(2, 2)

    def forward(self, x): # 4 blocks of transformation. 2 Big & 2 (Much Denser & Smaller Data) processing Blocks
        x = self.pool1(F.relu(self.conv2(F.relu(self.conv1(x)))))  # Effectively Convolution Block. How many convs, how many features & channels?
        x = self.pool2(F.relu(self.conv4(F.relu(self.conv3(x)))))

        x = F.relu(self.conv6(F.relu(self.conv5(x)))) # Final Decision Maker
        # x = F.relu(self.conv7(x))   # Final Decision Maker. ( RELU is making an decision)
        x = self.conv7(x)
        x = x.view(-1, 10) 
        x = F.log_softmax(x) # final activation/ decision maker
        return x
    
model = FirstDNN() 
model.to(device)
print(model)
print(summary(model, input_size=(1, 28, 28), 
        verbose=2,
        col_names=["input_size","kernel_size", "output_size", "num_params", "params_percent"],col_width=20))
#%%

for batch_idx, (data, y_actual) in enumerate(train_loader): 
    y_predicted = model(data)
    # Error Function & Optimizer
    error_function = nn.functional.nll_loss(y_actual,y_predicted)
    error_function.backward() # Error Gradient Calculated
    # Print gradients & weights & weight change
    
    optimizer = optim.SGD(model.parameters())   # Optimize what?
    optimizer.step()
    break


#%%
"TODO: Training & Testing Loop"
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

for epoch in range(1, 2):
    train(model, device, train_loader, optimizer)
    test(model, device, test_loader)