import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

load_dotenv()

class BaseResearcher:
    def __init__(self):
        tavily_key = os.getenv("TAVILY_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if not tavily_key or not openai_key:
            raise ValueError("Missing API keys")
        
        self.tavily_client = AsyncTavilyClient(api_key=tavily_key)
        self.openai_key = AsyncOpenAI(api_key=openai_key)
        self.analyst_type = "base_researcher"   # Default type
    
    @property
    def analyst_type(self) -> str:
        if not hasattr(self, "_analyst_type"):
            raise ValueError("Analyst type not set by subclass")
        return self._analyst_type
    
    @analyst_type.setter
    def analyst_type(self, value: str):
        self._analyst_type = value

    async def generate_queries(self, state: Dict, prompt: str) -> List[str]:
        company = state.get("company", "Unknown Company")
        industry = state.get("industry", "Unknown Industry")

        try:
            queries = []
            return queries
        except Exception as e:
            print(f"Error generating queries: {e}")
            return []

    def _format_query_prompt(self, prompt, company, hq, year):
        return f"""{prompt}

        Important Guidelines:
        - Focus ONLY on {company}-specific information
        -
        -
        - DO NOT make assumptions about the industry - use only the provided industry infromation"""
    
    def _fallback_queries(self, company, year):
        return [
            f"{company} overview {year}",
            f"{company} recent news {year}",
            f"{company} financial reports {year}",
            f"{company} industry analysis {year}"
        ]
    
    async def search_single_query(self, query: str, websocket_manager=None, job_id=None) -> Dict[str, Any]:
        """Execute a single search query with proper error handling."""
        if not query or len(query.split()) < 3:
            return {}
        
        try:
            docs = {}
            return docs
        except Exception as e:
            return {}
        
    async def search_documents(self, state: ResearchState, queries: List[str]) -> Dict[str, Any]:
        """
        Execute all Tavily searches in parallel at maximum speed
        """
        websocket_manager = state.get('websocket_manager')
        job_id = state.get('job_id')

        if not queries:
            logger.error("No valid queries to search")
            return {}