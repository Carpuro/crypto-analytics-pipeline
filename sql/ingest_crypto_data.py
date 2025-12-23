import requests
import pandas as pd
from datetime import datetime
import time

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
        
        # Extract relevant fields
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
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    df = fetch_crypto_data()
    if df is not None:
        print(df)