## Tennis Match prediction with betting strategy based on the Sharpe Ratio

### Description:

The goal of the project is using machine learning techniques predict the result of tennis matches. Furthermore, the prediction are then used for the optimization model that provides the optimal betting stakes for four major Grandslams - French Open, Wimbledon, Australian Open and US Open.

### Data:

Within the project we use the data freely available on the website - http://www.tennis-data.co.uk/alldata.php.

### Modules used:

`from urllib.request import urlopen`

`from bs4 import BeautifulSoup`

`from zipfile import ZipFile`

`from io import BytesIO`

`import os`

`import pandas as pd`

`import numpy as np`

`import multiprocessing`

`from datetime import datetime`

`from datetime import timedelta`

`import glob`

`from datetime import datetime`

`from xgboost import XGBClassifier`

`from sklearn.model_selection import cross_val_score`

### Code Evaluation:

Sequence of codes that needs to be run

* `data_download.py` (this downloads the data for project, this code should create a folder "Downloaded Data" in which the files are stored)

* `create_modelling_data.py` (in the "Generated Data" flder the modelling data are stored)

* `create_features.py` (this creates the features for each player and match, the code should run using parallelization)

* `model_estimation.py` (xgboost model estimation)

* `Beating the bookmakers on tennis matches.ipynb` (this summarizes the result of the project)
