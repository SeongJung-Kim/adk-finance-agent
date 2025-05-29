from typing import Any, Dict

from langchain_core.messages import AIMessage

from ...classes import ResearchState
from .base import BaseResearcher

class CompanyAnalyzer(BaseResearcher):
    def __init__(self) -> None:
        super().__init__()
        self.analyst_type = "company_analyzer"
    
    async def analyze(self, state: ResearchState) -> Dict[str, Any]:
        return {

        }
    
    async def run(self, state: ResearchState) -> Dict[str, Any]:
        return await self.analyze(state)