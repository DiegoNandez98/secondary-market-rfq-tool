# Secondary Market RFQ Tool

A small research project exploring how data could support decision-making on a secondary-market structured-products desk.

The project focuses on three questions:

1. Which incoming RFQs should be handled first?
2. Which RFQs are more likely to result in a trade?
3. Which existing client positions are more likely to generate SELL flow in the next 24 hours?

These three components operate at different stages:

- **Before an RFQ arrives** → estimate which existing positions are more likely to generate SELL flow.
- **When an RFQ arrives** → prioritise it based on urgency and market risk.
- **Once an RFQ arrives** → estimate how likely it is to convert into a trade.

All data is synthetic and the assumptions are simplified for research and learning purposes.

## Current Workflow

### 1. RFQ Prioritisation

Incoming RFQs are ranked using a transparent rule-based score based on:

- distance to barrier
- underlying market move
- implied volatility change
- quote staleness, adjusted for recent market activity
- RFQ notional size

The used weights are heuristic assumptions based on the expected relevance of each signal and are not statistically calibrated:

- barrier proximity: 35%
- market move: 20%
- implied volatility change: 15%
- quote staleness: 15%
- RFQ size: 15%

RFQs are classified as HIGH, MEDIUM or LOW priority, with simple reasons explaining the main drivers of the score.

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

### 3. Retail Flow Prediction

Position snapshots and transaction history are used to estimate the probability that an existing client position generates a SELL within the next 24 hours.

The model uses market, product, position and client-behaviour features.

On the chronological test set:

- Sell rate: 4.0%
- ROC-AUC: 0.726
- Top 10% ranked positions: 14.7% sell rate
- Lift: 3.7x

The position-level probabilities can also be aggregated to estimate expected sell activity.


## Project Structure

```text
data/
    synthetic_rfqs.csv
    synthetic_historical_rfqs.csv
    synthetic_position_snapshots.csv
    synthetic_transactions.csv
    synthetic_retail_flow_dataset.csv
    retail_flow_predictions.csv

models/
    retail_flow_model.joblib

notebooks/
    01_rfq_exploration.ipynb
    02_rfq_prioritisation.ipynb
    03_generate_historical_rfqs.ipynb
    04_rfq_conversion_prediction.ipynb
    05_retail_flow_dataset.ipynb
    06_retail_flow_analysis.ipynb
    07_retail_flow_prediction.ipynb
    08_predictive_flow_integration.ipynb

src/
    scoring.py
```

## How to Run

Install the required packages:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter joblib
```
Then run the notebooks in order:

##  Possible Extensions
- integrate sell_probability into RFQ prioritisation
- aggregate position probabilities into expected secondary-market SELL flow
- build a separate BUY-flow model
- include desk risk and hedging information
- calibrate the models on real historical desk data
