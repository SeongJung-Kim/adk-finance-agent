import os
from dotenv import load_dotenv
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from pynamodb.models import Model

load_dotenv()

REGION = os.getenv("REGION", "us-central1")
TABLE_NAME_STOCK_ANALYTICS = os.getenv("TABLE_NAME_STOCK_ANALYTICS", "StockAnalytics")
TABLE_NAME_PORTFOLIO = os.getenv("TABLE_NAME_PORTFOLIO", "portfolio")

class StockAnalysis(Model):
    class Meta:
        table_name = TABLE_NAME_STOCK_ANALYTICS
        region = REGION
    
    stock = UnicodeAttribute(hash_key=True)
    date = UnicodeAttribute(range_key=True)
    close = NumberAttribute()
    name = UnicodeAttribute(null=True)
    rank = NumberAttribute(null=True)
    stock_news = UnicodeAttribute(null=True)
    investment_decision = UnicodeAttribute(null=True)
    explanation = UnicodeAttribute(null=True)
    industry = UnicodeAttribute(null=True)

class Protfolio(Model):
    class Meta:
        table_name = TABLE_NAME_PORTFOLIO
        region = REGION


