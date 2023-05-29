"""
Common functions used across the project.
"""
import requests

from core.models import Coin


def fetch_coin_data():
    """Fetch coin data from CoinGecko API."""
    response = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets',
        params={'vs_currency': 'usd',
                'sparkline': 'false',
                'price_change_percentage': '30d'}
    )
    data = response.json()

    for coin in data:
        coin_data = {
            'coin_id': coin['id'],
            'name': coin['name'],
            'symbol': coin['symbol'],
            'price': coin['current_price'],
            'price_change_percentage': coin.get(
                'price_change_percentage_30d_in_currency'
            )
        }

        Coin.objects.update_or_create(
            coin_id=coin['id'],
            defaults=coin_data
        )

    queryset = Coin.objects.all().order_by('id')
    return queryset
