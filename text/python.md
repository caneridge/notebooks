# python.md

Install mc to ~/conda/mc2

conda list -n root --export | grep -v ^conda > ~/conda/mc2/default.list
conda create -n ENV --file ~/conda/mc2/default.list

## install notebook
conda install -n ENV jupyter

cd ipy-location
jupyter notebook

### Generate config file

jupyter notebook --generate-config

Generates
  ~/.jupyter/jupyter_notebook_config.py

## work mac

cd /Users/brian.jones/Desktop/code/ipy
/Users/brian.jones/conda/mc2/envs/py2711/bin/jupyter notebook
