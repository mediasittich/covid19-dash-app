# 2019 Novel Coronavirus (COVID-19) Dashboard Monitor and Data Repository

[![license](https://img.shields.io/github/license/Perishleaf/data-visualisation-scripts)](https://github.com/Perishleaf/data-visualisation-scripts/blob/master/LICENSE)

This public repository is created as part of a practice project at LMU Statistics.

Dashboard is deployed on Heroku and can be accessed from [https://dash-coronavirus-2020.herokuapp.com/](https://covid-19-stats-project.herokuapp.com)

The corresponding Jupyter Notebooks can be viewed [here](https://mybinder.org/v2/gh/mediasittich/covid19-dash-app/5ed7346e4e585b0a40116eed3090ec4b093fd3a8)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mediasittich/covid19-dash-app/master)



The data used in this project is sourced from 

- Ramil Kiprin
- UN Population Prospects
- World Bank Data
- Oxford Government Response Tracker

## Project Organization

------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │          
    │   └── make_dataset.py     <- Scripts to download or generate data
    │   │
    │   └── build_features.py   <- Scripts to turn raw data into features for modeling
    │   │ 
    │   └── visualize.py        <- Scripts to create exploratory and results oriented visualizations

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
