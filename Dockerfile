FROM continuumio/miniconda3:latest

EXPOSE 8888

RUN /opt/conda/bin/conda install jupyter -y --quiet \
	&& mkdir /opt/notebooks 

RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.1-linux-x86_64.tar.gz \
	&& tar zxvf julia-1.6.1-linux-x86_64.tar.gz

ENV PATH="/julia-1.6.1/bin:${PATH}"

RUN julia -e 'using Pkg; Pkg.add("PyCall"); Pkg.add("IJulia"); Pkg.add("Conda"); ENV["PYTHON"]=""; Pkg.build("PyCall")' \
	&& julia -e 'using Conda; Conda.pip_interop(true); Conda.pip("install", "amazon-braket-sdk")' \
	&& julia -e 'using Pkg; Pkg.add(["LightGraphs", "GraphPlot", "Colors", "Cairo", "Compose", "NLopt", "AWS", "Plots", "PyPlot", "Flux", "MLDatasets", "ProgressMeter"])'

ADD notebooks /opt/notebooks

CMD /opt/conda/bin/jupyter notebook \
	--notebook-dir=/opt/notebooks --ip='*' --port=8888 \
	--no-browser --allow-root
