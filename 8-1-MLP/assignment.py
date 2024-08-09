# assignment.py

import numpytorch as npt
from numpytorch import Tensor, nn
from numpytorch import reshape
import numpy as np

class Conv2d(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        # Initialize weights and biases with numpy
        self.weights = npt.tensor(np.random.rand(out_channels, in_channels, kernel_size, kernel_size) * np.sqrt(2. / (in_channels * kernel_size * kernel_size)), requires_grad=True)
        self.bias = npt.tensor(np.zeros(out_channels), requires_grad=True)
    
    def forward(self, x: Tensor) -> Tensor:
        # x: (batch_size, in_channels, height, width)
        batch_size, _, height, width = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        oh, ow = height - kh + 1, width - kw + 1
        
        # Output feature map
        out = np.zeros((batch_size, self.out_channels, oh, ow))
        
        for i in range(oh):
            for j in range(ow):
                # Get the current region
                x_region = x[:, :, i:i+kh, j:j+kw]
                # Perform convolution
                # Ensure tensors are compatible
                out[:, :, i, j] = np.tensordot(x_region.arr, self.weights.arr, axes=([1, 2, 3], [1, 2, 3])) + self.bias.arr
        
        return npt.tensor(out)


class MaxPool2d(nn.Module):
    def __init__(self, kernel_size: int, stride: int) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
    
    def forward(self, x: Tensor) -> Tensor:
        # x: (batch_size, in_channels, height, width)
        batch_size, channels, height, width = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        sh, sw = self.stride, self.stride
        
        oh, ow = (height - kh) // sh + 1, (width - kw) // sw + 1
        out = np.zeros((batch_size, channels, oh, ow))
        
        for i in range(oh):
            for j in range(ow):
                x_region = x[:, :, i*sh:i*sh+kh, j*sw:j*sw+kw]
                out[:, :, i, j] = np.max(x_region.arr, axis=(2, 3))
        
        return npt.tensor(out)


class MNISTClassificationModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = Conv2d(1, 32, kernel_size=3)  # 28x28 -> 26x26
        self.pool1 = MaxPool2d(kernel_size=2, stride=2)  # 26x26 -> 13x13
        self.conv2 = Conv2d(32, 64, kernel_size=3)  # 13x13 -> 11x11
        self.pool2 = MaxPool2d(kernel_size=2, stride=2)  # 11x11 -> 5x5
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10, bias=False)

    def forward(self, x: Tensor) -> Tensor:
        x = self.conv1(x)
        x = npt.relu(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = npt.relu(x)
        x = self.pool2(x)
        x = reshape(x, (x.shape[0], -1))  # Flatten
        x = self.fc1(x)
        x = npt.relu(x)
        logits = self.fc2(x)
        return logits
