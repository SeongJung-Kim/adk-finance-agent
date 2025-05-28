import OpenDartReader

"""
https://github.com/FinanceData/OpenDartReader
https://opendart.fss.or.kr/guide/detail.do
"""

DART_API_KEY = "fd664865257f1a3073b654f9185de11a708f726c"
dart = OpenDartReader(DART_API_KEY)

# Example: Get financial statements
# You need to find the corp_code for the company.

corp_code = '00126380'  # 삼성전자

try:
    # Get annual single-company financial statements for 2024
    # 11011 for Annual Report
    # 11013 for 재무제표
    fs_single = dart.finstate_all(corp_code, bsns_year=2024, reprt_code='11011')

    if fs_single is not None and not fs_single.empty:
        # Extract relevant data (e.g., 자산총계 - Total Assets, 부채총계 - Total Liabilities), 자본총계 - Total Equity,
        # 매출액 - Revenue, 영업이익 - Operating Income, 당기순이익 - Net Income)
        # You'll need to know the Korean account names (sj_nm) or codes (account_id)
        # Example (this will vary based on DART's output format and what you need):
        total_assets = fs_single[fs_single['account_nm'] == '자산총계']['thstrm_amount'].iloc[0]
        total_liabilities = fs_single[fs_single['account_nm'] == '부채총계']['thstrm_amount'].iloc[0]
        total_equity = fs_single[fs_single['account_nm'] == '자본총계']['thstrm_amount'].iloc[0]

        revenue = fs_single[fs_single['account_nm'] == '매출액']['thstrm_amount'].iloc[0]
        net_income = fs_single[fs_single['account_nm'] == '당기순이익']['thstrm_amount'].iloc[0]    # or 포괄손익계산서상의 당기순이익'

        print(f"\n--- Samsung Electronics (DART Data for 2024) ---")
        print(f"Total Assets: {float(total_assets):,.0f} KRW")
        print(f"Total Liabilities: {float(total_liabilities):,.0f} KRW")
        print(f"Total Equity: {float(total_equity):,.0f} KRW")
        print(f"Revenue: {float(revenue):,.0f} KRW")
        print(f"Net Income: {float(net_income):,.0f} KRW")

        if total_equity and float(total_equity) != 0:
            debt_to_equity_dart = float(total_liabilities) / float(total_equity)
            print(f"Debt to Equity (DART): {debt_to_equity_dart:.2f}")
        if revenue and float(revenue) != 0:
            net_profit_margin_dart = float(net_income) / float(revenue)
            print(f"Net Profit Margin (DART): {net_profit_margin_dart:.2f}")

    else:
        print("Could not retrieve financial statements from DART or data is empty.")

except Exception as e:
    print(f"Error fetching data from DART: {e}")


def calculate_stability_ratios(data):
    """안정성 지표 계산"""
    ratios = {}
    if data.get('유동부채') != 0:   # 0 으로 나누는 것 방지
        ratios['유동비율(%)'] = (data.get('유동자산', 0) / data['유동부채']) * 100
        ratios['당좌비율(%)'] = ((data.get('유동자산', 0) - data.get('재고자산', 0)) / data['유동부채']) * 100
    if data.get('총자본') != 0:
        ratios['부채비율(%)'] = (data.get('총부채', 0) / data['총자본']) * 100
    if data.get('이자비용') != 0:
        ratios['이자보상배율(배)'] = (data.get('영업이익', 0) / data['이자비용']) * 100
    return ratios

def calculate_profitability_ratios(data):
    """수익성 지표 계산"""
    ratios = {}
    if data.get('매출액') != 0:   # 0 으로 나누는 것 방지
        ratios['매출총이익률(%)'] = (data.get('매출총이익', 0) / data['매출액']) * 100
        ratios['영업이익률(%)'] = (data.get('영엽이익', 0) / data['매출액']) * 100
        ratios['순이익률(%)'] = (data.get('당기순이익', 0) / data['매출액']) * 100
    if data.get('평균자기자본') != 0:
        ratios['ROE(%)'] = (data.get('당기순이익', 0) / data['평균자기자본']) * 100
    if data.get('평균총자산') != 0:
        ratios['ROA(%)'] = (data.get('당기순이익', 0) / data['평균총자산']) * 100
    return ratios


print(fs_single)
print(fs_single.columns)

"""
['rcept_no', 'reprt_code', 'bsns_year', 'corp_code', 'sj_div', 'sj_nm',
       'account_id', 'account_nm', 'account_detail', 'thstrm_nm',
       'thstrm_amount', 'frmtrm_nm', 'frmtrm_amount', 'bfefrmtrm_nm',
       'bfefrmtrm_amount', 'ord', 'currency', 'thstrm_add_amount']

rcept_no: 접수번호 (보고서 제출 시 부여되는 고유번호)
reprt_code: 보고서코드 (예: 11011-사업보고서, 11012-반기보고서, 11013-분기보고서)
bsns_year: 사업연도 (회계 기준 연도)
corp_code: 고유번호 (공시시스템에서 사용하는 기업별 고유번호) 또는 법인등록번호
sj_div: 재무제표구분 (예: BS-재무상태표, IS-손익계산서, CIS-포괄손익계산서, CF-현금흐름표, SCE-자본변동표)
sj_nm: 재무제표명 (예: 재무상태표, 손익계산서)
account_id: 계정ID (회계 계정과목의 고유 코드)
account_nm: 계정명 (예: 유동자산, 매출액, 당기순이익)
account_detail: 계정상세 (계정과목의 상세 분류 또는 주석 구분)

thstrm_nm: 당기명 (보고서의 현재 기간 명칭, 예: 제 X 기)
thstrm_amount: 당기금액 (현재 기간의 계정 금액)
thstrm_add_amount: 당기누적금액 (분/반기 보고서의 경우 해당 회계연도 누적 금액) 또는 당기증감액 (문맥에 따라 변동액을 의미할 수도 있음. 일반적으로는 누적금액을 의미할 가능성이 높음)

frmtrm_nm: 전기명 (직전 기간 명칭, 예: 제 X-1 기)
frmtrm_amount: 전기금액 (직전 기간의 계정 금액)

bfefrmtrm_nm: 전전기명 (직전 기간의 이전 기간 명칭, 예: 제 X-2 기)
bfefrmtrm_amount: 전전기금액 (직전 기간의 이전 기간의 계정 금액)

ord: 계정과목 정렬순서 (재무제표 내 계정과목 표시 순서)
currency: 통화 단위 (금액의 통화 단위, 예: KRW, USD)

정기보고서 재무정보 > 단일회사 전체 재무제표
https://opendart.fss.or.kr/guide/detail.do?apiCrpCd=DS003&apiId=2019020
정기보고서 재무정보 > 단일회사 주요계정
https://opendart.fss.or.kr/guide/detail.do?apiCrpCd=DS003&apiId=2019016
"""

"""
# fs_single -> financial_data 으로 전환 필요
financial_data = {
    "유동자산": ,
    "재고자산": ,
    "유동부채": ,
    "총부채": ,
    "총자본": ,
    "영엽이익": ,
    "이자비용": ,
    "매출액": ,
    "매출총이익": ,
    "당기순이익": ,
    "평균자기자본": ,
    "평균총자산": ,
}
"""

fs_single = dart.finstate_all(corp_code, bsns_year=2024, reprt_code='11013')
print(fs_single)
print(fs_single.columns)

fs_single = dart.finstate_all(corp_code, bsns_year=2024)
print(fs_single)
print(fs_single.columns)

financial_data = {}

# 지표 계산 실행
stability = calculate_stability_ratios(financial_data)
profitability = calculate_profitability_ratios(financial_data)
#stability = calculate_stability_ratios(fs_single)
#profitability = calculate_profitability_ratios(fs_single)

print("--- 안정성 지표 ---")
for key, value in stability.items():
    print(f"{key}: {value:.2f}")

print("\n--- 수익성 지표 ---")
for key, value in profitability.items():
    print(f"{key}: {value:.2f}")