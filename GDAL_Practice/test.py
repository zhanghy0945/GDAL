import torch
import torch.nn as nn
import torch.optim as optim

# 检查torch的版本
print(f"PyTorch 版本: {torch.__version__}")

# 检查是否有可用的GPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"使用设备: {device}")
    print(f"GPU 版本: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")
    print("使用设备: CPU")

# 定义一个简单的神经网络
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 20)
        self.fc3 = nn.Linear(20, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 创建模型并移动到设备
model = SimpleNet().to(device)

# 生成随机输入数据并移动到设备
inputs = torch.randn(64, 10).to(device)
targets = torch.randn(64, 1).to(device)

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 模拟一个训练步骤
model.train()
for epoch in range(5):  # 训练5个epoch
    optimizer.zero_grad()  # 清空梯度
    outputs = model(inputs)  # 前向传播
    loss = criterion(outputs, targets)  # 计算损失
    loss.backward()  # 反向传播
    optimizer.step()  # 更新权重

    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

print("训练完成")
