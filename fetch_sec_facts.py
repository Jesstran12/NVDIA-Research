"""Extract the SEC XBRL company facts used by Project 1 into one small CSV.

Standard library only. Reads data.sec.gov's companyfacts API for NVIDIA, AMD and
Broadcom, keeps only the tags and periods the model uses, and writes
src/sec_xbrl/companyfacts_extract.csv with the accession number, form and filing
date of every value so each number can be traced to its filing.

Usage:  python3 fetch_sec_facts.py              # fetch (needs network) and extract
        python3 fetch_sec_facts.py --offline    # re-extract from the cached raw JSON

The raw JSON responses are cached in src/sec_xbrl/raw/ (ignored by git because they are
2-4 MB each); the extract CSV is committed. The SEC asks for a descriptive User-Agent.
"""
import csv
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, 'src', 'sec_xbrl', 'raw')
OUT = os.path.join(HERE, 'src', 'sec_xbrl', 'companyfacts_extract.csv')
USER_AGENT = 'FIN43900 student research (Purdue) contact via course'

COMPANIES = {'NVDA': '0001045810', 'AMD': '0000002488', 'AVGO': '0001730168'}

# Tags kept, by taxonomy. Durational tags keep rows ending in or after 2025; instants too.
TAGS = {
    'us-gaap': [
        'Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'CostOfRevenue',
        'GrossProfit', 'OperatingExpenses', 'ResearchAndDevelopmentExpense',
        'SellingGeneralAndAdministrativeExpense', 'OperatingIncomeLoss', 'NetIncomeLoss',
        'ProfitLoss', 'IncomeTaxExpenseBenefit',
        'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
        'EarningsPerShareDiluted', 'EarningsPerShareBasic',
        'WeightedAverageNumberOfDilutedSharesOutstanding',
        'WeightedAverageNumberOfSharesOutstandingBasic',
        'CashAndCashEquivalentsAtCarryingValue', 'MarketableSecuritiesCurrent',
        'DebtSecuritiesCurrent', 'ShortTermInvestments', 'AvailableForSaleSecuritiesDebtSecurities',
        'EquitySecuritiesFvNi', 'EquitySecuritiesWithoutReadilyDeterminableFairValueAmount',
        'AccountsReceivableNetCurrent', 'InventoryNet', 'AccountsPayableCurrent',
        'AccruedLiabilitiesCurrent', 'PropertyPlantAndEquipmentNet',
        'IntangibleAssetsNetExcludingGoodwill', 'Goodwill',
        'LongTermDebt', 'LongTermDebtCurrent', 'LongTermDebtNoncurrent', 'DebtCurrent',
        'LongTermDebtFairValue', 'CommercialPaper', 'OperatingLeaseLiabilityCurrent',
        'OperatingLeaseLiabilityNoncurrent', 'StockholdersEquity', 'Assets', 'Liabilities',
        'DepreciationDepletionAndAmortization', 'AmortizationOfIntangibleAssets',
        'ShareBasedCompensation', 'PaymentsToAcquireProductiveAssets',
        'NetCashProvidedByUsedInOperatingActivities', 'PaymentsForRepurchaseOfCommonStock',
        'PaymentsOfDividends', 'InvestmentIncomeInterest', 'InterestExpense',
        'NonoperatingIncomeExpense', 'OtherNonoperatingIncomeExpense',
    ],
    'dei': ['EntityCommonStockSharesOutstanding'],
}
MIN_END = '2024-01-01'


def fetch(cik, offline):
    os.makedirs(RAW_DIR, exist_ok=True)
    path = os.path.join(RAW_DIR, f'CIK{cik}.json')
    if offline or os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    req = urllib.request.Request(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
                                 headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.load(resp)
    with open(path, 'w') as fh:
        json.dump(payload, fh)
    return payload


def extract(ticker, payload):
    rows = []
    for taxonomy, tags in TAGS.items():
        facts = payload['facts'].get(taxonomy, {})
        for tag in tags:
            if tag not in facts:
                continue
            for unit, values in facts[tag]['units'].items():
                for v in values:
                    if v.get('form') not in ('10-K', '10-Q', '10-K/A') or v['end'] < MIN_END:
                        continue
                    rows.append(dict(ticker=ticker, taxonomy=taxonomy, tag=tag, unit=unit,
                                     start=v.get('start', ''), end=v['end'], value=v['val'],
                                     form=v['form'], fiscal_year=v.get('fy'), fiscal_period=v.get('fp'),
                                     accession=v.get('accn'), filed=v.get('filed'), frame=v.get('frame', '')))
    return rows


def main():
    offline = '--offline' in sys.argv
    rows = []
    for ticker, cik in COMPANIES.items():
        rows.extend(extract(ticker, fetch(cik, offline)))
    rows.sort(key=lambda r: (r['ticker'], r['tag'], r['end'], r['start'], r['filed'] or ''))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} rows -> {os.path.relpath(OUT, HERE)}')


if __name__ == '__main__':
    main()
