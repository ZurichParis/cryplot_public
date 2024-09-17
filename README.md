### Introduction
This project is a web application built using Dash by Plotly that allows users to visualize bitcoin price historical data and query for future price predictions.
Link to the web app: https://crypto-price-predictor-399l.onrender.com


### How to run
1. Clone the repository and cd into it
2. set virtual environment and run the app:

(Opion 1) venv:
```bash
python3 -m venv cryplot_1
source cryplot_1/bin/activate
pip install -r requirements.txt
```
```bash
python app.py
```

(Option 2) conda:
```bash
conda env create -f environment.yml
conda activate cryplot_1
```

```bash
python app.py
```

(Option 3) Docker:
```bash
docker build -t crypto-price-predictor .
docker run -p 8050:8050 crypto-price-predictor
```


