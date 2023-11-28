#!/bin/sh


sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y git-lfs
git config --global credential.helper store
git lfs pull
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.6
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
sudo update-alternatives --config pytho
sudo apt install python3.6-distutils
sudo apt-get install python3-distutils
sudo apt-get install python3-apt
# Choose 3.6 version
sudo apt -y install python3-pip
pip3 install --upgrade pip
python -m pip install numpy
python -m pip install pandas
python -m pip install matplotlib
python -m pip install https://files.pythonhosted.org/packages/86/9f/be0165c6eefd841e6928e54d3d083fa174f92d640fdc52f73a33dc9c54d1/tensorflow-1.4.0-cp36-cp36m-manylinux1_x86_64.whl
python -m pip install sugartensor==1.0.0.2
python -m pip install sklearn
python -m pip install future
python -m pip install torch
python -m pip install scipy
python -m pip install toml
python -m pip install matplotlib
python -m pip install torch
python -m pip install torchvision
python -m pip install wfdb
python -m pip install lshashpy3
# python -m pip  install opencv-python 
# Run: time python main_tsgen.py
