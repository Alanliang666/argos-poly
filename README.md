<div align="center">

# 👁️ Argos Poly

**A real-time arbitrage scanner for Polymarket prediction markets**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![asyncio](https://img.shields.io/badge/asyncio-powered-00C7B7?style=for-the-badge)](https://docs.python.org/3/library/asyncio.html)
[![WebSocket](https://img.shields.io/badge/WebSocket-live%20stream-brightgreen?style=for-the-badge)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP%20v1.0-orange?style=for-the-badge)]()

> Let the machine find free money while you sleep.

</div>

---

## 🤔 What Does This Actually Do?

In prediction markets, every outcome has an implied probability. In a perfectly efficient market, all outcomes should add up to exactly 100%.

But markets aren't always efficient.

When the sum of implied probabilities across all outcomes drops **below 100%**, there's a window to buy every side simultaneously and **lock in a risk-free profit**. That's textbook arbitrage — and Argos Poly hunts it 24/7.

Here's the core idea:

```
Normal market:    P(Yes) + P(No) = 1.00  →  No opportunity
Mispriced market: P(Yes) + P(No) = 0.96  →  Free $0.04 per dollar
```

**Argos Poly** connects to Polymarket's live order book, continuously computes implied probabilities across thousands of markets, and fires an alert the moment an opportunity appears.

> ⚠️ **V1.0 is Paper Trading only.** No real capital is involved. This phase is for validation and research.

---

## ✨ Features

| | Feature | Details |
|--|---------|---------|
| ⚡ | Async real-time ingestion | `asyncio` + `websockets` — low-latency, non-blocking |
| 📡 | Full CLOB subscription | Subscribes to Level-2 order book across all active markets |
| 🧮 | Fee-adjusted arbitrage engine | Calculates net profit after taker fees (0.2%) and slippage (0.5%) |
| 📋 | Paper trading logger | Simulates trade execution and logs every signal with timestamp |
| 🔄 | Auto-reconnect | WebSocket drops and reconnects automatically — no babysitting needed |
| 🚀 | Concurrent API ingestion | Fetches all market metadata in parallel (up to 50,000 offsets) |

---

## 🖥️ Terminal Preview

```
👁  Argos Poly v1.0 — Polymarket Arbitrage Scanner
─────────────────────────────────────────────────
[INIT]  Fetching active markets from Polymarket REST API...
[OK]    4,823 active markets loaded across 482 pages
[INIT]  Connecting to Polymarket CLOB WebSocket...
[OK]    WebSocket connected → wss://ws-subscriptions-clob.polymarket.com/ws/market
[OK]    Subscribed to 4,823 markets (Level 2, initial dump enabled)
─────────────────────────────────────────────────
[12:00:05] Scanning... Active markets in OrderBook: 312
[12:00:10] Scanning... Active markets in OrderBook: 1,047
[12:00:15] Scanning... Active markets in OrderBook: 2,391

🎯 ARBITRAGE SIGNAL DETECTED
─────────────────────────────────────────────────
[2026-04-09 12:00:15] | Market: 0x7f3a...d92e | Type: Will the Fed cut rates in May 2026? | Cost: $0.97 | Expected Profit: $0.03
[2026-04-09 12:00:15] | Market: 0x4b1c...a83f | Type: BTC above $100K by end of April?   | Cost: $0.96 | Expected Profit: $0.04
```

---

## 🚀 Quick Start

**Requirements:** Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/alanliang666/argos-poly.git
cd argos-poly

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the scanner
python src/main.py
```

---

## 📂 Project Structure

```
argos-poly/
├── src/
│   ├── main.py              # Entry point — wires everything together
│   ├── config.py            # Global constants (URLs, fees, slippage)
│   ├── ingestion/
│   │   ├── api_client.py    # Async REST client — concurrent market metadata fetch
│   │   └── ws_client.py     # WebSocket client — live CLOB stream
│   ├── core/
│   │   └── orderbook_manager.py  # Consumes WS queue, maintains live order book state
│   ├── strategy/
│   │   └── engine.py        # Arbitrage detection + fee/slippage cost estimation
│   └── execution/
│       └── paper_trade.py   # Signal → paper trade logger
├── docs/
│   └── design_docs_v1.md    # System design & architecture notes
├── tests/                   # Unit tests (pytest + asynctest)
├── requirements.txt
└── README.md
```

---

## 🧠 How the Arbitrage Math Works

```python
# For a binary market (Yes / No):
total_cost = best_ask(Yes) + best_ask(No)

# Adjust for trading costs:
slippage = total_cost * 0.005   # 0.5% default
taker_fee = total_cost * 0.002  # 0.2% Polymarket fee
net_cost = total_cost + slippage + taker_fee

# Fire signal only if there's profit left:
if net_cost < 1.00:
    expected_profit = 1.00 - net_cost  # risk-free edge
```

The strategy engine scans every market in the order book on each 5-second polling cycle, computes `net_cost`, and appends profitable opportunities to the signal queue for paper execution.

---

## 🗺️ Roadmap

- [x] **V1.0** — REST + WebSocket ingestion, order book management, arbitrage engine, paper trading
- [ ] **V1.1** — Multi-market parallel scanning, performance benchmarking
- [ ] **V2.0** — Real execution via Polymarket CLOB API (L1 key integration)
- [ ] **V2.1** — SQLite signal history, backtesting module
- [ ] **V3.0** — Web dashboard with live opportunity feed

---

## 🤝 Contributing

All contributions welcome — bug reports, feature ideas, or PRs.

```bash
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
# Then open a Pull Request
```

---

## ⚠️ Disclaimer

This project is for **academic research and educational purposes only**. Prediction markets and crypto carry significant financial risk. The author is not responsible for any real-world financial losses. **Do not deploy real capital without fully understanding the risks and applicable regulations in your jurisdiction.**

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

If this project was useful to you, a ⭐ goes a long way!

**Built by [Alanliang666](https://github.com/Alanliang666)**

</div>
