"""
Global configuration and constants for the Polymarket Arbitrage Bot.
"""
import logging

# ==========================================
# 1. API & WebSocket URLs 
# ==========================================
POLYMARKET_REST_URL = "https://gamma-api.polymarket.com/events"
POLYMARKET_WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

# ==========================================
# 2. Ingestion Settings 
# ==========================================
# API Client 
API_MAX_OFFSET = 50000
API_PAGINATION_LIMIT = 100

# WebSocket Client
WS_PING_INTERVAL = 10
WS_PING_TIMEOUT = 10

# ==========================================
# 3. Strategy Parameters 
# ==========================================
DEFAULT_SLIPPAGE = 0.005
TAKER_FEE = 0.002

# ==========================================
# 4. Logger Settings 
# ==========================================
LOG_LEVEL = logging.INFO
