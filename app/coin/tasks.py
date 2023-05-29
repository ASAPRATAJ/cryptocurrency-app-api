from celery import shared_task

from coin.views import CoinView


@shared_task
def fetch_coin_data_every_five_minutes():
    coin_view = CoinView()

    # Execute the list method to fetch coin data
    response = coin_view.get()

    # Process the response and update the database
    if response.status_code == 200:
        return 'Coin data fetched successfully.'

    return 'Failed to fetch coin data.'
