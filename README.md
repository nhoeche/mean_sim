# mean_sim
MeanSim: Understanding Standard Error

This is a python Dash app that simulates drawing $N$ random variables of $n$ samples each from a normal distribution of mean $µ$ and standard deviation $\sigma$. The mean of each $N$ is plotted on the normal distribution.
This simulation demonstrates how the standard error of th mean gets smaller with increasing $n$ and decreasing $\sigma$.

## How to run

You will need python to run the app.

### Install the dependencies

Using pip:

```sh
pip install dash numpy pandas scipy plotly dash-bootstrap-components
```

Using conda: 

```sh
conda install dash numpy pandas scipy dash-bootstrap-components
conda install -c plotly plotly
```

Using conda with virtual environment:

```sh
conda create -n meansim dash numpy pandas scipy dash-bootstrap-components
conda activate meansim
conda install -c plotly plotly
```

### Run the app

Run the app with python

```sh
python main.py
```

The app should open in your browser. If not, visit `http://127.0.0.1:8050/`in your browser.

