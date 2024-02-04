import tabula

EMPTY_DICT = {}

FOLIO_NO = 'FOLIONO'
ISIN = 'ISIN'
SCHEME_NAME = 'SCHEME_NAME'
COST_VALUE = 'COST_VALUE'
UNIT_BALANCE = 'UNIT_BALANCE'
NAV_DATE = 'NAV_DATE'
NAV = 'NAV'
MARKET_VALUE = 'MARKET_VALUE'
REGISTRAR = 'REGISTRAR'

def within_index(table, row):
    N_ROWS = len(table)
    if row >= N_ROWS:
        print('Index out of range for table')
        return False
    return True

def get_record(table, row):
    if not within_index(table, row):
        return EMPTY_DICT

    record = table.iloc[row]

    folio_no = record[0]
    isin = ''

    if type(folio_no) == str:
        parts = folio_no.split('IN')
        folio_no = parts[0]
        isin = 'IN' + parts[1]
    
    scheme_name = record[2]
    cost_value = record[3]
    unit_balance = record[4]
    nav_date = record[5]
    nav = record[6]
    market_value = record[7]
    registrar = record[8]
    
    return {
        FOLIO_NO: folio_no,
        ISIN: isin,
        SCHEME_NAME: scheme_name,
        COST_VALUE: cost_value,
        UNIT_BALANCE: unit_balance,
        NAV_DATE: nav_date,
        NAV: nav,
        MARKET_VALUE: market_value,
        REGISTRAR: registrar
    }


def __parse(table):
    data = []

    for row in range(1, len(table)):
        record = get_record(table, row)

        if type(record[FOLIO_NO]) == float: #math.isnan(record[FOLIO_NO]):
            last_record = data[-1]
            last_record[SCHEME_NAME] += ' ' + record[SCHEME_NAME]
        else:
            data.append(record)    
    return data


def parse(file, password):
    try:
        pdfData = tabula.read_pdf(file, pages='1', password = password, silent = True)
        table = pdfData[0]
        return __parse(table)
    except:
        print('Exception')
        pass
    return 'An Error occurred'

