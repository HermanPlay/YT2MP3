FROM continuumio/miniconda3

COPY requirements.txt .
COPY bot.py .
COPY downloader.py .

RUN conda config --add channels conda-forge

RUN conda env create --name virtual-env --file requirements.txt python=3.9.16


ENTRYPOINT [ "conda", "run", "-n", "virtual-env", "bot.py"]