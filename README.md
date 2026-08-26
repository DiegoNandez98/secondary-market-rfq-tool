# Secondary Market RFQ Prioritisation Tool

A small Python prototype for prioritising incoming RFQs on a structured-products secondary market desk.

The goal is to help a trader identify which requests may require attention first when multiple RFQs arrive simultaneously.

## Current MVP

The project currently:

- generates a synthetic RFQ dataset
- explores the main RFQ and market-risk variables
- assigns a priority score to each RFQ
- ranks RFQs from highest to lowest priority
- classifies requests into HIGH, MEDIUM and LOW priority

The score currently considers factors such as:

- underlying market move
- implied volatility change
- time since the last quote / price staleness
- RFQ size
- proximity to a product barrier

The initial scoring weights and thresholds are heuristic and would ideally be calibrated using historical desk data.

## Project structure

```text
secondary-market-rfq-tool/
├── data/
│   └── synthetic_rfqs.csv
├── notebooks/
│   ├── 01_rfq_exploration.ipynb
│   └── 02_rfq_prioritisation.ipynb
├── src/
│   └── scoring.py
└── README.md
```

## Next steps

The next iteration will focus on making the ranking more interpretable by explaining why each RFQ receives its priority level.

Possible later extensions include product-specific risk logic, dynamic scoring weights and integration with live market data.

## Disclaimer

This project uses synthetic data and is intended as a prototype for research and learning purposes.
