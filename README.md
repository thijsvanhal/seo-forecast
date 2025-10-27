<div align="center">

![Streamlit Prophet](streamlit_prophet/references/logo.png)

[![CI status](https://github.com/artefactory-global/streamlit_prophet/actions/workflows/ci.yml/badge.svg?branch%3Amain&event%3Apush)](https://github.com/artefactory-global/streamlit_prophet/actions/workflows/ci.yml?query=branch%3Amain)
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](#supported-python-versions)
[![Dependencies Status](https://img.shields.io/badge/dependabots-active-informational.svg)](https://github.com/artefactory-global/streamlit_prophet/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://prophet.streamlit.app)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-informational.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory-global/streamlit_prophet/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/artefactory-global/streamlit_prophet/releases)
[![License](https://img.shields.io/badge/License-MIT-informational.svg)](https://github.com/artefactory-global/streamlit_prophet/blob/main/LICENSE)

Deploy a [Streamlit](https://streamlit.io/) app to train, evaluate and optimize a [Prophet](https://facebook.github.io/prophet/) forecasting model visually

## ⭐  Quick Start  ⭐

[Test the app online](https://prophet.streamlit.app) with shared computing resources & [read introductory article](https://medium.com/artefact-engineering-and-data-science/visual-time-series-forecasting-with-streamlit-prophet-71d86a769928?source=friends_link&sk=590cca0d24f53f73a9fdb0490a9a47a7)

If you plan to use the app regularly, you should install the package and run it locally:
```bash
pip install -U streamlit_prophet
streamlit_prophet deploy dashboard
```

</div>

https://user-images.githubusercontent.com/56996548/126762714-f2d3f3a1-7098-4a86-8c60-0a69d0f913a7.mp4

## 💻 Requirements

### Python version
* Main supported version : <strong>3.7</strong> <br>
* Other supported versions : <strong>3.8</strong> & <strong>3.9</strong>

Please make sure you have one of these versions installed to be able to run the app on your machine.

### Operating System
Windows users have to install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/) to download the package. 
This is due to an incompatibility between Windows and Prophet's main dependency (pystan). 
Other operating systems should work fine.

## ⚙️ Installation


### Create a virtual environment (optional)
We strongly advise to create and activate a new virtual environment, to avoid any dependency issue.

For example with conda:
```bash
pip install conda; conda create -n streamlit_prophet python=3.7; conda activate streamlit_prophet
```

Or with virtualenv:
```bash
pip install virtualenv; python3.7 -m virtualenv streamlit_prophet --python=python3.7; source streamlit_prophet/bin/activate
```


### Install package
Install the package from PyPi (it should take a few minutes):
```bash
pip install -U streamlit_prophet
```

Or from the main branch of this repository:
```bash
pip install git+https://github.com/artefactory-global/streamlit_prophet.git@main
```


## 📈 Usage

Once installed, run the following command from CLI to open the app in your default web browser:

```bash
streamlit_prophet deploy dashboard
```

Now you can train, evaluate and optimize forecasting models in a few clicks.
All you have to do is to upload a time series dataset. 
This dataset should be a csv file that contains a date column, a target column and optionally some features, like on the example below:

![](streamlit_prophet/references/input_format.png)

Then, follow the guidelines in the sidebar to:

* <strong>Prepare data</strong>: Filter, aggregate, resample and/or clean your dataset.
* <strong>Choose model parameters</strong>: Default parameters are available but you can tune them.
Look at the tooltips to understand how each parameter is impacting forecasts.
* <strong>Select evaluation method</strong>: Define the evaluation process, the metrics and the granularity to
assess your model performance.
* <strong>Make a forecast</strong>: Make a forecast on future dates that are not included in your dataset,
with the model previously trained.
* <strong>📊 NEW: Investment Scenario Simulation</strong>: Compare different investment strategies (e.g., SEO budgets, content production) and their projected impact on your metrics. Perfect for sales presentations and ROI demonstrations!

Once you are satisfied, click on "save experiment" to download all plots and data locally.

## 🎯 NEW: Investment Scenario Simulation

This tool now includes powerful scenario simulation capabilities, perfect for SEO and marketing forecasting:

- **🔮 What-If Analysis**: Compare different investment levels side-by-side
- **⏱️ Lag Effects**: Model delayed impact (e.g., SEO investments taking 3-6 months to show results)
- **💰 ROI Analysis**: Calculate and visualize return on investment for different strategies
- **📈 Sales Presentations**: Demonstrate potential outcomes to clients and stakeholders

**Use Cases:**
- Pitch SEO services by showing projected impact of different investment levels
- Plan budgets by comparing ROI across scenarios
- Justify marketing spend with data-driven projections

👉 **See [SCENARIO_SIMULATION.md](SCENARIO_SIMULATION.md) for detailed usage guide and examples**

👉 **Try it with the example dataset: [example_seo_data.csv](example_seo_data.csv)**


## 🛠️ How to contribute ?

All contributions, ideas and bug reports are welcome! 
We encourage you to open an [issue](https://github.com/artefactory-global/streamlit_prophet/issues) for any change you would like to make on this project.


For more information, see [`CONTRIBUTING`](https://github.com/artefactory-global/streamlit_prophet/blob/main/CONTRIBUTING.md) instructions.
If you wish to containerize the app, see [`DOCKER`](https://github.com/artefactory-global/streamlit_prophet/blob/main/DOCKER.md) instructions.
