## Tennis Match prediction with betting strategy based on the Sharpe Ratio

blogpost here: https://medium.com/@tomko5peter/betting-on-grand-slam-aa35d6a9da71

### Project Overview:

The goal of the project is to analyze betting strategy in tennis Grand Slams. Using machine learning model, the underlying probability model of match result is being investigated. Based on the prediction model, we apply optimization technique for optimal allocation of bet stakes. Betting strategy is evaluated in the Jupyter notebook `Beating the bookmakers on tennis matches.ipynb`.

### Project Statement:

Is there any source of predictability in betting industry? Is there a way to create an edge over bookmakers in long-run? Is there a subset of tennis betting industry that might create a profitable opportunities? The project aims to apply machine learning approach with combination of optimization model in order to evaluate possible long-run profitability in tennis betting.

### Input Data:

Within the project we use the data freely available on the website - **http://www.tennis-data.co.uk/alldata.php**. We use men and women results in Grand Slams in period from 2000.

### Betting Strategy Evaluation/Metrics:

The betting strategy is evaluated in period from 1/1/2019 up to the most recently available results in the year 2020. The optimization uses daily matches - the decision about optimal stakes is delivered using the Sharpe ratio maximization (technique heavily used in the field of financial markets). The metric used for betting strategy evaluation is a **net cumulative profit**. Furthermore, within the project we use also cumulative accuracy - i.e. daily precision of the betting rolling daily from the beginning of the year 2019.

### Modules Used:

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

Downloaded data are archived in the folder `Downloaded Data` - there are 2 archives (`men`, and `women`).

* `Data Exploration and Visualization.ipynb` (Data Exploration and Visualization)

* `create_modellingdata.py` (in the "Generated Data" folder the modelling data are stored)

* `create_features.py` (this creates the features for each player and match, the code should run using parallelization, cca. 45min)

If the archive Generated Data.7z is unzipped into the project directory, there is no need to run previous sequence of codes.

* `model_estimation.py` (xgboost model estimation)

* `Beating the bookmakers on tennis matches.ipynb` (this summarizes the result of the project)
