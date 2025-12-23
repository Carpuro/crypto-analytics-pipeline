import os
from sqlalchemy import create_engine, text
import pandas as pd

def get_db_connection():
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'crypto_db')
    db_user = os.getenv('DB_USER', 'crypto_user')
    db_password = os.getenv('DB_PASSWORD', 'crypto_pass')
    
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)

def query_latest_prices():
    engine = get_db_connection()
    query = "SELECT * FROM latest_crypto_prices ORDER BY market_cap DESC"
    df = pd.read_sql(query, engine)
    print("\n=== Latest Crypto Prices ===")
    print(df)
    return df

def query_all_records():
    engine = get_db_connection()
    query = "SELECT COUNT(*) as total FROM crypto_prices"
    df = pd.read_sql(query, engine)
    print(f"\nTotal records in database: {df['total'][0]}")

if __name__ == "__main__":
    query_all_records()
    query_latest_prices()