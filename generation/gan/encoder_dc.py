"""
Source of the code: https://github.com/dbiir/TS-Benchmark.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.utils import save_image
import os
from PIL import Image
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
from glob import glob
import wfdb
import numpy as np
from tqdm import tqdm
import torch.nn.functional as F
import os
import argparse

import toml
config = toml.load('../config.toml')

n_iterations = int(config['generation']['n_iterations'])


class D_Net(nn.Module):
    def __init__(self,bais=False):
        super(D_Net,self).__init__()
        self.dnet1 = nn.Sequential(
            nn.Conv2d(3,128,5,3,3,bias=bais),
            # nn.BatchNorm2d(64),不要把batchnormlize部署在判别网络输入端和生成网络的输出端
            nn.LeakyReLU(0.2,True),#12

            nn.Conv2d(128,256, 4, 2,3,bias=bais),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2,True),#8

            nn.Conv2d(256,512,4, 2,3,bias=bais),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2,True),)#6
        self.dnet2=nn.Sequential(
            nn.Conv2d(512,1024, 4,2,2,bias=bais),
            nn.BatchNorm2d(1024),
            nn.LeakyReLU(0.2,True),#4
            nn.Conv2d(1024,1,4, 1,bias=bais),
            )

    def forward(self, x):
        y =self.dnet1(x)
        out=self.dnet2(y)
        return y,out

class G_Net(nn.Module):
    def __init__(self):
        super(G_Net, self).__init__()
        # layer1输入的是128,128,1,1的随机噪声,输出尺寸(64*8)x4x4
        self.layer1 = nn.Sequential(
            nn.ConvTranspose2d(128, 1024, 4, 1, 0, bias=False),
            nn.BatchNorm2d(1024),
            nn.ReLU(inplace=True)
        )
        # layer2输出尺寸(64*4)x8x8
        self.layer2 = nn.Sequential(
            nn.ConvTranspose2d(1024, 512, 4, 2, 2, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True)
        )
        # layer3输出尺寸(64*2)x16x16
        self.layer3 = nn.Sequential(
            nn.ConvTranspose2d(512, 256, 4, 2, 3, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )
        # layer4输出尺寸(64)x32x32
        self.layer4 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 4, 2, 3, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        # layer5输出尺寸 3x96x96
        self.layer5 = nn.Sequential(
            nn.ConvTranspose2d(128, 3, 5, 3, 3, bias=False),
            nn.Tanh()
        )
    # 定义G_Net的前向传播
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        return out
class encoder(nn.Module):
    def __init__(self,bais=False):
        super(encoder,self).__init__()
        self.en = nn.Sequential(
            nn.Conv2d(3,32,3,1,bias=bais),
            nn.BatchNorm2d(32),#不要把batchnormlize部署在判别网络输入端和生成网络的输出端
            nn.PReLU(),#30

            nn.Conv2d(32,64, 3,2,1,bias=bais),
            nn.BatchNorm2d(64),
            nn.PReLU(),#15

            nn.Conv2d(64,128,3,1,bias=bais),
            nn.BatchNorm2d(128),
            nn.PReLU(),#13
            #
            nn.Conv2d(128,256, 3,2,1,bias=bais),
            nn.BatchNorm2d(256),
            nn.PReLU(),#7

            nn.Conv2d(256,256,3, 1,bias=bais),
            nn.BatchNorm2d(256),
            nn.PReLU(),#5
            nn.Conv2d(256,512,3, 1,bias=bais),
            nn.BatchNorm2d(512),
            nn.PReLU(),#3
            nn.Conv2d(512, 128, 3, 1, bias=bais),
            nn.BatchNorm2d(128),#1
)

    def forward(self, x):
        y =self.en(x)
        return y

if __name__ == '__main__':
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    d_net = D_Net().to(device)
    g_net = G_Net().to(device)
    encoder_=encoder().to(device)
    d_net.eval()
    g_net.eval()
    encoder_.train()
    loss_fu=nn.MSELoss()
    optimizer = torch.optim.Adam(
        encoder_.parameters(), lr=0.0001)
    batch_size=128
    # def to_img(x):
    #     out = 0.5 * (x + 1)#[(-1,1)+1=(0,2),(0,2)*0.5=(0,1)],
    #     out = out.clamp(0, 1)#Clamp函数可以将随机变化的数值
    #     # 限制在一个给定的区间[min, max]内,[0,1]
    #     return out
    #
    #
    parser = argparse.ArgumentParser(description="A script that takes two integer values as input and calls a function with them.")
    parser.add_argument("--seed", type=str, default='conductivity', help="Link to original dataset")
    args = parser.parse_args()
    date=np.loadtxt('../data/' + args.seed + '/segments_orig.txt',delimiter=',')
    
    # date=np.loadtxt('../data/column_23_3072_3072.txt',delimiter=',')
    lis = []
    for i in range(3072):
        lis.append(date[i].reshape((3, 32, 32))/10)

    print(len(lis))

    dataloader = DataLoader(lis, batch_size=batch_size,
                            shuffle=True, num_workers=2, drop_last=True)

    d_net.load_state_dict(
                torch.load(r"./gand_path"))
    g_net.load_state_dict(
                torch.load(r"./gang_path"))
    try:
        encoder_.load_state_dict(torch.load('./ganen_path'))
        print('success')
    except:
        print('falied')

    for epoch in range(n_iterations):
            for i, img in enumerate(dataloader):
                for p in d_net.parameters(): p.data.clamp_(-0.01, 0.01)
                # img = img / 10
                real_img = img.float().to(device)
                z=encoder_(real_img)
                real_out = g_net(z)
                out1,_=d_net(real_img)
                out2,_=d_net(real_out)
                loss1=loss_fu(out2,out1)
                loss2=loss_fu(real_out,real_img)
                loss=loss1+loss2

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                # pbbox.append(loss.cpu().detach().numpy())
                # sub_axix = filter(lambda x: x % 200 == 0, pbbox)
                # plt.plot(pbbox, color='green')
                # # plt.legend()
                # plt.title('en_loss')
                # plt.ylabel('en_loss')
                # plt.pause(0.001)
                if i%10 == 0:
                    print(loss.item())
                    torch.save(encoder_.state_dict(), r"./ganen_path")
