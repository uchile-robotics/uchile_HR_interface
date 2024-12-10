# Uchile Human-Robot Interface

Repo for Speech recognition and text to speech

## Requirements

In order to install the requirements you must install python 3.9 or greater.

### Python 3.9 installation

(FG): Hay que tener ojo, esto solo sirve para el speech to text y el text to speech.
Para instalar ollama, chromadb y todo eso, hay que revisar porque parece que hay que tener una versión más actualizada de python (más que python3.9) (pero no cacho porque solamente alcancé a usar el stt y el tts).


1. Update the packages list and install the prerequisites:

``` bash
sudo apt update
sudo apt install software-properties-common
```

2. Add the deadsnakes PPA to your system’s sources list:

``` bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

3. Once the repository is enabled, you can install Python 3.9 by executing:

``` bash
sudo apt install python3.9
```

4. Verify that the installation was successful by typing:

``` bash
python3.9 --version
```
``` bash
# Output:
Python 3.9.1+
```

#### Virtual Environment creation

To avoid conflicting installations of python packages, 
we recommend that you create a virtual environment 
(you can choose the name of your virtual environment):

```bash
cd ~/
python3.9 -m venv <name-of-environment>
```

Then to activate it, you must run the following command:

```bash
source ~/<name-of-environment>/bin/activate
```

### CUDA clean install

Install CUDA and CUDNN

First you must update your OS
```bash
sudo apt update && sudo apt upgrade
```

Remove all CUDA, CUDNN and Nvidia Drivers:
```bash
sudo apt-get remove --purge -y '*nvidia*' '*cuda*' 'libcudnn*' 'libnccl*' '*cudnn*' '*nccl*'
sudo apt-get autoremove --purge -y
sudo apt-get clean
```
Check if there's any installed packages left:

```bash
dpkg -l | grep -E 'nvidia|cuda|cudnn|nccl'
```
If there is any packages left, you must run:

```bash
packages=('*nvidia*' '*cuda*' 'libcudnn*' 'libnccl*' '*cudnn*' '*nccl*')
for pack in "${packages[@]}"; do
    echo "Removing $pack..."
    sudo apt remove --purge -y "$pack"
done
```
#### Detecting and managing drivers on ubuntu

```bash
ubuntu-drivers devices
```
We will install the NVIDIA driver tagged recommended — 
Which indicates which drivers are recommended for each piece 
of hardware based on compatibility and performance.

```bash
sudo ubuntu-drivers autoinstall
```

##### Install Nvidia Drivers

My recommended version is 555, change “XYZ” in the following command to your recommended driver:

```bash
sudo apt install nvidia-driver-XYZ
```

Reboot the system for these changes to take effect.

```bash
reboot
```
##### Check Installation

After reboot verify that the following command works 
(in order to verify that the nvidia drivers are properly installed)

```bash
nvidia-smi
```

It's recommended that before installing CUDA you check 
[PyTorch's website](https://pytorch.org/get-started/locally/#start-locally)
to install the newest supported version of PyTorch (and its corresponding CUDA version). In that 
website you can find the CUDA versions which are supported by torch. You should 
search the [CUDA versions here](https://developer.nvidia.com/cuda-toolkit-archive).


In our case we'll be installing CUDA 12.4 for Ubuntu 20.04 with architecture x86_64. Before installing, you must check for any `.deb` or `.pin` files in home directory.

```bash
cd ~/
rm cuda*
```
Now we proceed with the installation:

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin

sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600

wget https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda-repo-ubuntu2004-12-4-local_12.4.0-550.54.14-1_amd64.deb

sudo dpkg -i cuda-repo-ubuntu2004-12-4-local_12.4.0-550.54.14-1_amd64.deb

sudo cp /var/cuda-repo-ubuntu2004-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/

sudo apt-get update

sudo apt-get -y install cuda-toolkit-12-4
```

Now we check if CUDA is installed correctly:

```bash
nvcc --version
```
If you are not getting the CUDA version as output, do the following:

Creating a symlink for easier reference
```bash
sudo ln -s /usr/local/cuda-12.4 /usr/local/cuda
```

Add the CUDA paths to your `.bashrc` file to ensure they are set up every time you open a terminal.

```bash
# if you're using bash terminal:
echo 'export PATH=/usr/local/cuda-12.4/bin:$PATH' >> ~/.bashrc
```

```bash
# if you're using zsh terminal:
echo 'export PATH=/usr/local/cuda-12.4/bin:$PATH' >> ~/.zshrc
```

Then close the terminal and open a new one. Then check the installation with the `nvcc --version` command. If that command outputs something similar to :

```bash
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Thu_Mar_28_02:18:24_PDT_2024
Cuda compilation tools, release 12.4, V12.4.131
Build cuda_12.4.r12.4/compiler.34097967_0
```

Then the CUDA installation was succesful.

### Installing CUDNN

Now we'll install CUDNN. To check the compatible CUDNN version with your CUDA installation you must [Check Here](https://docs.nvidia.com/deeplearning/cudnn/latest/reference/support-matrix.html#id17)

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cudnn9-cuda-12 # This command is for our case only, you must check the compatible CUDNN version for your CUDA installation
```

### Installation of Pip packages

Activating the created virtual environment from earlier:

```bash
source ~/<name-of-environment>/bin/activate
pip3 install torch torchvision torchaudio TTS
```

