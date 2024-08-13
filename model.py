import torch
import torch.nn as nn

'''
notes for architecture:

Conv2d
 - use odd kernel sizes
 - each kernel size increase increases padding by 1
  - ex: KS=1 -> padding=0
  - KS=3 -> padding=1
  - KS=5 -> padding=2
 - stride=1

MaxPool2d
 - use even kernel sizes (=2)
 - stride=2
 - each layer will half resolution

ConvLayer
 - Conv + BN + activation

ConvUnit
 - ConvLayers + Maxpool

Input: b x 3 x 224 x 224
Output: b x 7 x 7 x (5+C)
'''

config = [
    {
        'in_channels': 3,
        'out_list': [16,16,16,16],
        'kern_list': [3,3,3,3],
        'maxpool': True
    },
    {
        'in_channels': 16,
        'out_list': [16,16,16],
        'kern_list': [3,3,3],
        'maxpool': True
    },
    {
        'in_channels': 16,
        'out_list': [32,32,32],
        'kern_list': [3,3,3],
        'maxpool': True
    },
    {
        'in_channels': 32,
        'out_list': [64,64,64],
        'kern_list': [3,3,3],
        'maxpool': True
    },
    {
        'in_channels': 64,
        'out_list': [128,128,128],
        'kern_list': [3,3,3],
        'maxpool': True
    },
    {
        'in_channels': 128,
        'out_list': [256,256],
        'kern_list': [3,3],
        'maxpool': False
    }
]

class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kern_size=3, maxpool=False):
        super(ConvLayer, self).__init__()
        #Save userinputs
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kern_size = kern_size
        self.padding = kern_size // 2
        self.mp = maxpool
        
        self.conv = nn.Conv2d(in_channels, out_channels, kern_size, padding=self.padding) #Save Conv2d
        self.bn = nn.BatchNorm2d(out_channels) #Save batchnorm
        if maxpool: #If statement for maxpool line at the end of a layer
            self.maxpool = nn.MaxPool2d((2, 2), 2)

    def forward(self, x): 
        output = nn.functional.relu((self.bn(self.conv(x)))) #Run image(x) through layer
        if self.mp:
            return self.maxpool(output)
        return output
    
class ConvUnit(nn.Module):
    def __init__(self, in_channels, out_list, kern_list, maxpool=True):
        super(ConvUnit, self).__init__()
        #Save userinput
        self.in_channels = in_channels
        self.out_list = out_list
        self.depth = len(out_list)
        self.kern_list = kern_list
        self.mp = maxpool

        self.layers = nn.ModuleList()
        #save layer into layers
        for i in range(self.depth):
            in_channel = in_channels if i == 0 else out_list[i-1] #If statment for first unit
            maxpool = self.mp if i == self.depth - 1 else False# If statment for maxpool
            layer = ConvLayer(in_channel, out_list[i], kern_list[i], maxpool)
            self.layers.append(layer) #Append layer to layers
    
    def forward(self, x):
        for layer in self.layers: #Run image through layers
            x = layer(x)
        return x

class YoYo(nn.Module):
    def __init__(self, num_classes, config=config):
        super(YoYo, self).__init__()
        self.num_classes = num_classes #number of classees
        #dictionary of parameters
        self.config = config
        self.last_layer = nn.Conv2d(config[-1]['out_list'][-1], 5+num_classes, 1) #last conv2d layer

        self.units = nn.ModuleList()
        #save units
        for parameter in config:
            unit = ConvUnit(**parameter)
            self.units.append(unit)

    def forward(self, x):
        #run image through units
        for unit in self.units:
            x = unit(x)
        x = self.last_layer(x).permute(0, 2, 3, 1) # b x 9 x 7 x 7 -> b x 7 x 7 x 9
        #squash
        B_layer = torch.sigmoid(x[..., :5])
        C_layer = torch.softmax(x[..., 5:], -1)
        return torch.cat((B_layer, C_layer), -1)
