"""
Polymarket API Client.
This module provides an asynchronous HTTP client to concurrently fetch
and parse market information from the Polymarket API.
"""
from src.config import API_MAX_OFFSET, API_PAGINATION_LIMIT
import aiohttp
import asyncio
import json
import certifi
import ssl

class ApiClient:
    OFFSET = API_MAX_OFFSET
    LIMIT = API_PAGINATION_LIMIT
    
    def __init__(self, url):
        """
        Initialize the api client and prepare the storage for market information.
        @param url: str, the url of the Polymarket API
        """
        self.url = url
        self.market_info = {} # mapping: clob_token_id -> [market_id, question, outcome]
        
    
    async def get_market_info(self):
        """
        Concurrently fetch market info from the api across multiple pages.
        Uses asynchronous requests to avoid blocking and retrieve all data chunk.
        """
        ssl_context = ssl.create_default_context(cafile=certifi.where()) # SSL context using certifi CA certificates
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for offset in range(0, self.OFFSET, self.LIMIT):  # pre-generate offsets up to 50,000 to cover all possible pages
                tasks.append(self.fetch_single_market_info(session, offset)) # add fetch task to the batch
            await asyncio.gather(*tasks) 


    async def fetch_single_market_info(self, session, offset, limit=100):
        """
        Fetch a single chunk of market info from the API based on the offset.
        @param session: aiohttp.ClientSession, the active async connection session
        @param offset: int, the starting point (offset) for the data chunk
        @param limit: int, the maximum number of items to retrieve per request
        """
        params={"offset": offset, "limit":limit, "active":"true", "closed":"false"}
        async with session.get(self.url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                self.extract_market_info(data)
            else:
                print(f"Error: {response.status}")
                return None 

    
    def extract_market_info(self, data):
        """
        Extract market details from raw event data.
        The extracted pairings will be mapped and stored inside self.market_info.
        @param data: list, the raw event list fetched from the API
        """
        for event in data:
            if "markets" in event:
                for market in event["markets"]:
                    if market.get("closed") is False:
                        question = market.get("question")
                        market_id = market.get("id")

                        # parse JSON string into Python list
                        try:
                            outcome = json.loads(market.get("outcomes", "[]"))
                            clob_token_id = json.loads(market.get("clobTokenIds", "[]"))

                            if len(clob_token_id) == len(outcome):  # ensure arrays have matching lengths before pairing
                                for i in range(len(outcome)):  # pair each token ID with its corresponding outcome
                                    self.market_info[clob_token_id[i]] = [market_id, question, outcome[i]]
                        
                        except json.JSONDecodeError:
                            print(f"Skipping Market {market.get('id')} due to JSON decode error.")
                            continue
                        
                        except Exception as e:
                            pass
