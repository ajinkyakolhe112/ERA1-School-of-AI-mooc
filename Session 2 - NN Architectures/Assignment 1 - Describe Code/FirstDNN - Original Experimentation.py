import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
# !pip install torchsummary
from torchsummary import summary

# !pip install torchinfo # has more advanced functionality
from torchinfo import summary as summaryNew

summaryNew(model,input_size=(1,28,28),verbose=2,
    col_names=["input_size","kernel_size", "output_size", "num_params", "params_percent"],col_width=20
);

"""### Device Setup"""

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
device

"""### Data Loader Setup"""

batch_size = 128

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=True, download=True,
                    transform=transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
                    ])),
    batch_size=batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=False, transform=transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
                    ])),
    batch_size=batch_size, shuffle=True)

"""# Some Notes on our naive model

We are going to write a network based on what we have learnt so far. 

The size of the input image is 28x28x1. We are going to add as many layers as required to reach RF = 32 "atleast".

## Sequential & 2Dto1D Reshape/Flatten
"""

# Simple Sequential Stack of Simple Layers
# Simple Layers individually do one step of transformation. Nesting of layers makes powerful networks
model = nn.Sequential(
    nn.Conv2d(1,1,3), # Layer, Activation or Block of Layers. 

)
# Image to Linear conversion is a bit complex. Need to understand this interaction deeply.
# Flatten Layer -> Maintains number of Channels. Converts 2d Image to a vector.


nn.Conv2d(inputImage)
# calls forward on this layer with input. 
# Error is same at each layer. Contribution to error is the parameter of connection
# Weights at this layer are layer.weight & layer.bias
# Receptive field at each layer & output dimentions

Session2Model = torch.nn.Sequential(
    torch.nn.Conv2d(1,32,3,padding=1),
    nn.Conv2d(32,64,3,padding=1),
    nn.MaxPool2d(2,2),
    nn.Conv2d(64,128,3,padding=1),
    nn.Conv2d(128,256,3,padding=1),
    nn.MaxPool2d(2,2),
    nn.Conv2d(256,512,3),
    nn.Conv2d(512,1024,3),
    nn.Conv2d(1024,10,3),
    CustomReshape(10),
    nn.Softmax()
)

class CustomReshape(nn.Module): # NO RESHAPE IN PYTORCH
    def __init__(self,newShape): #
        super().__init__()
        self.shape = newShape
    
    def forward(self,x):
        try:
            return x.view(-1,self.shape) # view function in Tensor module not in torch.nn.functional module
        except ReshapeNotPossibleError:
            pass
        # return x.view(*self.shape)

# Making it work All Again
# Flatten Image to 1D. Transition layer. Flatten with multi channel -> Conv1d, combined channel


channels,width,height = 3,28,28
testImage = torch.randn(channels,width,height)
flattenTest = nn.Sequential(
    nn.Conv2d(3,128,21), # 128 * 8 * 8
    nn.ReLU(),
    nn.Conv2d(128,128,3), # Output Shape: Single Example of 5*5 with out_channels. In_channels of Data, those many channels of kernels. 
    nn.ReLU(),
    nn.Flatten(), # Single Example 5*5 flatten. 128 Channels with 5*5...   
    nn.Conv1d(128,1,1), # Convert prev_channels Channels into 1 channel. 1 Channel * 5*5 Pixels in straight line
    nn.Linear(width*height,1) # 5*5 pixels, 
)

output = model(singleImage)
summary(model)

"""## Sequential to Functional

"""

# You can't do any branching at all. And branching is very powerful. So we use alternative.

"""
Model Architecture & Parameters
Data fed Batch by Batch

1. initialization of layers & parameters
1. FOR Data fed batch by batch
2. FOR forward pass layer by layer
3. error calculation at last layer. (Activation Function Choosen)
4. FOR Error back propogation reverse layer by layer
5. Weight Update accordingly
"""

"""
A Single Neuron we put. It's a building block of learning. Each Single Neuron is just X_batch \odot W_neuronNo
Every Single Neuron, according to Error Value, corrects its individual weights, according to each's contribution to Error
W = horizontal array of weights. 
"""

import torch
import torch.nn as nn
import torch.nn.functional as F # functional module is all the Classes in nn module but in format of functions. Simple functions. F.relu F.selu() F.conv2d
import torch.nn.functional as functions

## Layers in pytorch, actually are nothing but functions from functional module being called with inputX * Weight + Bias. 
## Layer is a class instantiated with its internal variables or parameters being updated for all batches of data. 

class FirstDNN(nn.Module):
    def __init__(self): # Initialization for layers to be used
        super(FirstDNN,self).__init__()
        nn.Conv2d() # Processing & Parameters... Parameters initialize. 
        nn.ReLU() # Don't need to create. Non parameter layer. Just processing layer. 
        nn.Conv2d()
        CustomReshapeImageto1D() # For Vision. Somewhere from Image * Channel view, we will go into vector space of integers for further processing Generally final block of 4 block structure NN

    # extending method 
    def forward(self,inputData): # \latex single Example.. one by one x_1, x_2 or array of batch of datapoints # this will have hooks
        firstTransformedData = Conv2d(inputData)
        secondTransformedData = Conv2d(firstTransformedData)

    def backward(ErrorFunction): # will probably have hooks
        pass
        # According to dynamic operation in above forward, we have library which can calculate this. why do we have that library, because we have fast computers which can calculate this. 

class CustomReshape(nn.Module):
    def __init__(self,newShape):
        self.newShape = newShape

    def forward(self,inputData):
        torch.nn.functional.view
# customNeural Network + CustomLayer in that network + Functional Pytorch for forward. extending forward pass for each.

