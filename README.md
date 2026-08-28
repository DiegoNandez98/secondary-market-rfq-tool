# Secondary Market RFQ Tool

A small research project exploring how data could support decision-making on a secondary-market structured-products desk.

The project currently focuses on two questions:

1. Which incoming RFQs should be handled first?
2. Which RFQs are more likely to result in a trade?

All data is synthetic and the assumptions are simplified for research and learning purposes.

## Current Workflow

### 1. RFQ Prioritisation

Incoming RFQs are ranked using factors such as:

- notional size
- market moves
- implied volatility changes
- distance to barrier
- quote staleness
- bid-ask spread

The output is a priority score with simple reasons explaining the ranking.

### 2. RFQ Conversion Prediction

A synthetic historical RFQ dataset is used to estimate the probability that an incoming RFQ results in a trade.

The baseline model is an interpretable logistic regression using client, product and market information.

On the test set:

- ROC-AUC: 0.666
- Overall trade rate: 42.7%
- Top 30% ranked RFQs: 61.3% trade rate
- Top 20%: 68.0%
- Top 10%: 75.0%

The model is therefore mainly used as a ranking tool rather than as a binary trade/no-trade classifier.

## Project Structure

```text
data/
    synthetic_rfqs.csv
    synthetic_historical_rfqs.csv

notebooks/
    01_rfq_exploration.ipynb
    02_rfq_prioritisation.ipynb
    03_generate_historical_rfqs.ipynb
    04_rfq_conversion_prediction.ipynb

src/
    scoring.py
```

## How to Run

Install the required packages:

```bash
pip install pandas numpy scikit-learn jupyter
```
Then run the notebooks in order:

01 → explore the RFQ data
02 → build the RFQ priority ranking
03 → generate synthetic historical RFQs
04 → train and evaluate the RFQ conversion model

##  Possible Extensions
- forecast which clients, products and BUY/SELL flows may emerge from market moves
- include desk risk and hedging information
- combine RFQ urgency with execution probability
- calibrate the models on real historical desk data
