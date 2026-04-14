import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms

# 加载MNIST（公开数据集，1行加载✅）
train_dataset = datasets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=True)

# 构建2层网络（输入784 → 隐藏128 → 输出10）
#用单层的话如“3”和“8”局部特征相似，单层无法准确识别俩层加Relu可以拟合曲线边界
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)#第一层layer层 
        self.fc2 = nn.Linear(128, 10)#第二层layer层
        self.relu = nn.ReLU()  #选用 ReLU 三重理由：
# 1️⃣ 梯度恒为1（x>0）→ 避免浅层网络梯度衰减（对比Sigmoid饱和区梯度≈0，梯度消失！！！） 链式法则连乘导致，
# 2️⃣ 仅需比较运算 → 训练速度比Sigmoid快1.2倍+（企业看重迭代效率）
# 3️⃣ 负输入归零 → 引入稀疏性，隐含正则效果（减少过拟合风险）


    def forward(self, x):
        x = x.view(-1, 784)  # 展平28x28图像
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNet()
# 后续训练逻辑略（周三任务会补全）
