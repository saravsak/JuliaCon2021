FROM continuumio/miniconda3:latest

EXPOSE 8888

RUN /opt/conda/bin/conda install jupyter -y --quiet\
	&& mkdir /opt/notebooks 

CMD /opt/conda/bin/jupyter notebook \
	--notebook-dir=/opt/notebooks --ip='*' --port=8888 \
	--no-browser --allow-root
