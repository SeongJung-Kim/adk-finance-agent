import pandas as pd
from dotenv import load_dotenv

class PortfolioManager:
    def __init__(self):
        load_dotenv()
    
    def manage_portfolio(self, finance_api, database):
        date = finance_api.today.strftime('%Y-%m-%d')

        