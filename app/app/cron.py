"""Tasks to run with crontab."""
import datetime

import requests
from rest_framework.response import Response

from coin import serializers
from core.models import Vote, Coin, User
from coin.views import CoinViewSet


# def fetch_coin_data():
#     """Get coin data from CoinGecko API."""
#     response = requests.get(
#         'https://api.coingecko.com/api/v3/coins/markets',
#         params={'vs_currency': 'usd',
#                 'sparkline': 'false',
#                 'price_change_percentage': '30d'}
#     )
#     data = response.json()
#
#     for coin in data:
#         coin_data = {
#             'coin_id': coin['id'],
#             'name': coin['name'],
#             'symbol': coin['symbol'],
#             'price': coin['current_price'],
#             'price_change_percentage': coin.get(
#                 'price_change_percentage_30d_in_currency'
#             )
#         }
#
#         Coin.objects.update_or_create(
#             coin_id=coin['id'],
#             defaults=coin_data
#         )
#
#     queryset = Coin.objects.all().order_by('id')
#     serializer = serializers.CoinSerializer(queryset, many=True)
#     return Response(serializer.data)
#

def calculate_monthly_votes():
    """Calculate monthly votes and reward gem_finders with badge."""
    today = datetime.date.today()
    first_day_of_month = datetime.date(today.year, today.month, 1)

    next_month = first_day_of_month.replace(day=28) \
                 + datetime.timedelta(days=4)

    last_day_of_month = next_month - datetime.timedelta(
        days=next_month.day
    )
    votes = Vote.objects.filter(
        created_at__gte=first_day_of_month,
        created_at__lte=last_day_of_month
    )

    coins = Coin.objects.all()
    coin_prices = {coin.coin_id: coin.price for coin in coins}

    # Calculate percentage change for each coin
    largest_changes = {}

    for vote in votes:
        coin = vote.coin
        vote_price = vote.price

        if coin.coin_id in coin_prices:
            current_price = coin_prices[coin.coin_id]
            percentage_change = \
                ((current_price - vote_price) / vote_price) * 100

            if coin.coin_id not in largest_changes \
                    or percentage_change > largest_changes[coin.coin_id]:
                largest_changes[coin.coin_id] = percentage_change

    if largest_changes:
        max_percentage_change = max(largest_changes.values())

        coins_with_max_change = \
            [coin_id for coin_id, percentage_change in largest_changes.items()
             if percentage_change == max_percentage_change]

        users_with_votes = Vote.objects.filter(
            coin__coin_id__in=coins_with_max_change,
            created_at__gte=first_day_of_month,
            created_at__lte=last_day_of_month
        ).values_list('user', flat=True).distinct()

        users = User.objects.filter(id__in=users_with_votes)
        for user in users:
            user.gem_finder = True
            user.save()


def reset_votes_left():
    """Reset remaining votes."""
    now = datetime.now()
    if now.day != 1:
        return  # Only run on the 1st day of the month

    users = User.objects.all()

    for user in users:
        user.votes_left = 3
        user.save()
