# 👁️ Argos Poly: Polymarket Risk-Free Arbitrage Scanner

Argos Poly is a real-time arbitrage monitoring system built with Python `asyncio` and websockets. It is designed to continuously scan the Central Limit Order Book (CLOB) of Polymarket prediction markets, hunting for risk-free arbitrage opportunities where the sum of implied probabilities falls below 100%.

**Current Version:** V1.0 (MVP)
This phase focuses exclusively on Paper Trading and data monitoring. No real capital execution is involved.

## 🛠️ Getting Started

Please follow the steps below to set up your local development environment:

### 1. Clone the Repository

```bash
git clone https://github.com/alanliang666/argos-poly.git
cd argos-poly
```

### 2. Create and Activate Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate
# Activate the virtual environment (Windows)
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📂 Project Architecture

- `docs/`: System design documents and testing strategies.
- `src/ingestion/`: Polymarket WebSocket data stream ingestion.
- `src/strategy/`: Core mathematical engine for arbitrage calculations.
- `src/execution/`: Paper trading execution and log formatting.

## ⚠️ Disclaimer

This project is for academic research and programming learning purposes only. Cryptocurrency and prediction markets carry extremely high risks. The author assumes no responsibility for any real financial losses.