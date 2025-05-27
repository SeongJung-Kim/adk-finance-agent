import os
import yaml
from dotenv import load_dotenv
import configparser
from helper.helper import HelperService


config = configparser.ConfigParser()
config.read('config.ini')

helper: HelperService = HelperService(config)

"""
StockAnalyst 클래스는 다음을 목표로 합니다. (Gemini Code Assist 제공)

1. 여러 주식에 대한 재무 데이터 및 뉴스를 가져옵니다.
2. 가져온 데이터에 산업 평균 비교 정보를 추가하여 풍부하게 만듭니다.
3. AI 모델(HelperService를 통해)을 활용하여 주식을 분석하고, 순위를 매기고, 투자 결정을 제공합니다.
4. 분석 결과를 데이터베이스에 저장합니다.
"""

class StockAnalyst:
    def __init__(self):
        load_dotenv()
        with open('schema/prompts.yaml', 'r') as file:
            self.prompts = yaml.safe_load(file)

    def stock_analysis(self, finance_api, database):
        """
        
        """
        # Access and set the Google API key
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        if os.getenv("COMPARE_SYMBOLS_WITHOUT_INDUSTRY"):
            self._compare_stocks_with_retry(finance_api.symbols, 'NO_INDUSTRY', finance_api, database)
        else:
            for industry, stocks in finance_api.industries.items():
                self._compare_stocks_with_retry(stocks, industry, finance_api, database)


    @helper.retry(retries=3, delay=60 * 5)
    def _compare_stocks_with_retry(self, stocks, industry, finance_api, database):
        self._compare_stocks(stocks, industry, finance_api, database)

    def _compare_stocks(self, stocks, industry, finance_api, database):
        data_per_symbol = []
        for symbol in stocks:
            data, ticker = finance_api.get_history(symbol['symbol'])
            self._add_industry_average_to_ticker(ticker, symbol['symbol'], finance_api)
            ticker.info['name'] = symbol['name']
            input_text = self.prompts['agent_web_search_stock_analysis']['prompt'].replace("<stock_name>", symbol['name'])
            ticker.info['StockNews'] = helper.invoke_agent(input_text)
            data_per_symbol.append(self_remove_unused_data_for_ai(ticker.info))

        stocks_to_send = self._get_ranking(data_per_symbol, industry, finance_api)
        for st in stocks_to_send:
            st['industry'] = industry
            st['date'] = str(finance_api.today.strftime('%Y-%m-%d'))
        database.save_stock_analytics(stocks_to_send)

    
    def _get_ranking(self, data, industry, finance_api):
        content = self.prompts['stock_analytics_user']['prompt'].replace("<data>", str(data))
        system_prompt = self.prompts['stock_analytics_system']['prompt'].replace("<data>", 
                                                                                 str(finance_api.today.strftime('%Y-%m-%d'))) \
                                                                        .replace('<industry>', industry)
        
        response = helper.invoke_model([{"role": "user", "content": content}], system_prompt)
        stock_indicators = data
        for ai_ranking in response:
            for stock_indicator in stock_indicators:
                if 'symbol' in ai_ranking and stock_indicator['symbol'] == ai_ranking['symbol']:
                    rank = ai_ranking.get('rank', 99)
                    explanation = ai_ranking.get('explanations', '')
                    investment_decision = ai_ranking.get('investment_decision', '')
                    if rank == 'null' or rank is None or rank == 'None' or rank == 'N/A':
                        rank = 99
                    stock_indicator['rank'] = rank
                    stock_indicator['explanation'] = explanation
                    stock_indicator['investment_decision'] = investment_decision
        
        try:
            stock_indicators_sorted = sorted(stock_indicators, key=lambda x: x.get('rank', 99))
        except Exception as e:
            stock_indicators_sorted = stock_indicators
        return stock_indicators_sorted

    def _remove_unused_data_for_ai(self, data):
        parameters = ['address1', 'address2', 'city', 'state', 'zip', 'country', 'phone', 'phone', 'fax', 'website', 'industry', 'industryKey', 'industryKey', 'industryDisp', 'sector', 'sectorKey', 'sectorDisp', 'longBusinessSummary', 'fullTimeEmployees', 'companyOfficers']
        return {key: value for key, value in data.items() if key not in parameters}
    
    def _add_industry_average_to_ticker(self, ticker, symbol, finance_api):
        # 티커에 대한 산업 평균 추가(?)
        """Add industry average to ticker information."""
        parameters = ["trailingPE", "forwardPE", "averageVolume", "trailingAnnualDividendRate", "profitMargin", "shortRatio", "shortPercentOfFloat", "bookValue", "trailingEps", "forwardEps", "ebitda", "totalDebt", "totalRevenue", "debtToEquity", "freeCashflow", "earningsGrowth", "revenueGrowth", "operatingMargins", "pegRatio", "grossMargins", "ebitdaMargins"]
        for parameter in parameters:
            industry_avg = finance_api.get_industry_or_sector_data(symbol,
                                                                   name="industry",
                                                                   parameter=parameter)
            ticker.info[f"industryAverage{parameter[0].upper()}{parameter[1:]}"] = industry_avg
            symbol_val = finance_api.get_info(ticker, parameter=parameter)
            ticker.info[parameter] = symbol_val