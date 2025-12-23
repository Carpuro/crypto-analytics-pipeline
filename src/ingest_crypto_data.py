import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import os

def get_db_connection():
    """Create database connection"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'crypto_db')
    db_user = os.getenv('DB_USER', 'crypto_user')
    db_password = os.getenv('DB_PASSWORD', 'crypto_pass')
    
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)

def fetch_crypto_data():
    """Fetch cryptocurrency data from CoinGecko API"""
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    params = {
        'vs_currency': 'usd',
        'ids': 'bitcoin,ethereum,cardano,solana,polkadot,dogecoin,ripple,litecoin,chainlink,polygon',
        'order': 'market_cap_desc',
        'sparkline': 'false'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        processed_data = []
        for coin in data:
            processed_data.append({
                'timestamp': datetime.now(),
                'coin_id': coin['id'],
                'symbol': coin['symbol'],
                'name': coin['name'],
                'current_price': coin['current_price'],
                'market_cap': coin['market_cap'],
                'total_volume': coin['total_volume'],
                'price_change_24h': coin['price_change_24h'],
                'price_change_percentage_24h': coin['price_change_percentage_24h']
            })
        
        df = pd.DataFrame(processed_data)
        
        # Save to CSV
        filename = f"data/crypto_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        
        # Save to PostgreSQL
        engine = get_db_connection()
        df.to_sql('crypto_prices', engine, if_exists='append', index=False)
        print(f"Data inserted into database: {len(df)} records")
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    df = fetch_crypto_data()
    if df is not None:
        print(df)