## For user
Thanks for cloning my project. This is a small python based multiple processor framework for python user, you can define your own processor function and, of course deploy it into the multiprocessor manager. Then it can automatically distribute and allocate the nodes, to execute among clusters of machine or only one machine for more than one processes.

## Main Features
 - user-friendly multiple processor API, all you need to do is define a rollup function to execute all the task in one thread. The multiprocessor manager will automatically exert this function on multiple processors.
 - user-friendly distributed processing API. All you need to do is the totally the same to the above, with the manager helping you set the distributed configuration.

## Install Toturial
### Basic requirements
 - Python : >=3.8
### Installation
1. Download this repositry using git:
```bash
git clone https://github.com/BugBubbles/Multiprocessor
# OR git clone git@github.com:BugBubbles/Multiprocessor.git
```
2. (Optional) Install the requisite software (if you want to use the distributed processing programme), you can find the official guide in [HERE](https://www.mpich.org/static/downloads/4.1.2/mpich-4.1.2-installguide.pdf).
3. Install the basic third package in your virtual environment:
```bash
cd ./Multiprocessor
conda create -n multiprocessor python==3.8.5
conda activate multiprocessor
conda install --file requirements.txt
```
If you are using the python basic `venv`, you can type these command in your bash shell:
```bash
python3 -m venv multiprocessor
activate /path/to/your/env/multiprocessor/bin/activate
pip install -r requirements.txt
```
4. Install the virtual environment:
```bash
pip install .
```
After finish all above, the Multiprocessor is successfully installed in your machine!

## Other Things