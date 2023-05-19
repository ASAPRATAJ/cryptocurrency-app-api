from coin.views import CoinViewSet
from coin.serializers import CoinSerializer
from celery import shared_task

from core.models import Coin


@shared_task
def fetch_coin_data_every_five_minutes():
    coin_view_set = CoinViewSet()
    request = None  # Mock the request object as it's not needed for the list method
    coin_view_set.request = request
    coin_view_set.format_kwarg = None
    coin_view_set.kwargs = {}
    coin_view_set.action = 'list'

    # Execute the list method to fetch coin data
    response = coin_view_set.list(request)

    # Process the response and update the database
    if response.status_code == 200:
        return 'Jest 200 jest super'

    return 'Coin data fetched successfully.'
