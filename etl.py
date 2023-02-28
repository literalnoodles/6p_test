import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import time

conn = psycopg2.connect(
    host="db",
    database="etldb",
    user="postgres",
    password="postgres"
)

fields = [
    'indexId',
    'chartOpen',
    'chartClose',
    'chartLow',
    'chartHigh',
    'totalQtty',
    'totalValue',
    'dateTime'
]

chunk_size = 10000

def save_data(chunk):
    records = [tuple(x) for x in chunk[fields].to_numpy()]
    with conn.cursor() as cursor:
        cols = ','.join(fields)
        query = f"INSERT INTO StockPrice ({cols}) VALUES %s"
        execute_values(cursor, query, records)
        conn.commit()

def extract(src_file):
    print('Start reading excel file ...')
    df = pd.read_excel(src_file, sheet_name=0)
    print('Finish loading dataframe')
    return df

def load(df):
    chunks = [df[i:i+chunk_size] for i in range(0, df.shape[0], chunk_size)]
    for chunk in chunks:
        save_data(chunk)

def convert_hour_data():
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO stockpricehour (indexId, chartOpen, chartClose, chartLow,
                chartHigh, totalQtty, totalValue, dateTime)
            SELECT distinct on (indexid, dt)
                indexId, 
                first_value(chartOpen) OVER w AS chartopen,
                last_value(chartClose) OVER w AS chartclose,
                min(chartLow) OVER w AS chartlow, 
                max(chartHigh) OVER w AS charthigh,
                sum(totalQtty) OVER w AS totalqtty, 
                sum(totalValue) OVER w AS totalvalue, 
                date_trunc('hour', dateTime) AS dt
            FROM stockprice
            WINDOW w AS (PARTITION BY indexid, date_trunc('hour', datetime)
                ORDER BY datetime ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
            """)
        conn.commit()

def main():
    df = extract('./db/data.xlsx')
    load(df)
    convert_hour_data()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
