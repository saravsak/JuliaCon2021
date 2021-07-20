# JuliaCon2021

## Setup Instructions

### Docker Instructions

Ensure you have docker installed.

```
docker run -p 8888:8888 -it ghcr.io/codewithsk/quantum-computing-with-julia:latest
```

This should start a local jupyter notebook instance with the notebooks required for this tutorial.

### Setting it up from scratch

#### Install Julia

1. Download Julia v1.6.1 for your environment [here](https://julialang.org/downloads/)

```bash
$ wget https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.1-linux-x86_64.tar.gz
```

2. Install Julia for your environment [here](https://julialang.org/downloads/platform/)

```bash
$ wget https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.1-linux-x86_64.tar.gz
$ tar zxvf julia-1.6.1-linux-x86_64.tar.gz
$ echo "PATH=\${PATH}:$(pwd)/julia-1.6.1/bin" >> ~/.bashrc
```

3. Ensure you have Julia Installed
```bash
$ julia -v
julia version 1.6.1
```

4. Install IJulia
```bash
$ julia -e 'using Pkg; Pkg.add("IJulia")'
```

#### Setup Jupyter

1. Install Anaconda from [here](https://www.anaconda.com/products/individual)
```bash
$ sh $(wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh)
```

2. Add conda to your path variable

```bash
$ echo "PATH=\${PATH}:$(pwd)/anaconda3/bin" >> ~/.bashrc
```

3. Ensure that the Julia kernel exists with Jupyter

```bash
$ jupyter kernelspec list
Available kernels:
  julia-1.6    /home/ubuntu/.local/share/jupyter/kernels/julia-1.6
  python3      /home/ubuntu/anaconda3/share/jupyter/kernels/python3
```

#### Setup PyCall

1. Install Conda.jl
```bash
$ julia -e 'using Pkg; Pkg.add("Conda")'
```

2. Install PyCall
```bash
$ julia -e 'using Pkg; Pkg.add("PyCall"); ENV["PYTHON"]=""; Pkg.build("PyCall")'
```

3. Install AWS Braket
```bash
$ julia -e 'using Conda; Conda.pip_interop(true); Conda.pip("install", "amazon-braket-sdk")'
```

4. Verify the right version of Braket has been installed
```bash
$ julia -e 'using PyCall; braket = pyimport("braket._sdk"); println(braket.__version__)'
1.7.2
```
