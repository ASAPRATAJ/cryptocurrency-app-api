from _decimal import Decimal

from django.db.models import Sum, F

from datetime import datetime, timedelta
from core.models import Vote, Coin, User


def calculate_monthly_votes():
    now = datetime.now()
    if now.day != 6:
        return  # Only run on the 6th day of the month

    # Get all votes for the current month
    current_month_votes = Vote.objects.all()

    # Calculate percentage change for each coin
    coin_percentages = {}
    for coin in Coin.objects.all():
        try:
            start_vote = current_month_votes.filter(coin=coin).earliest('id')
            end_vote = current_month_votes.filter(coin=coin).latest('id')
            start_price = start_vote.coin.price
            end_price = end_vote.coin.price
            if start_price and end_price:
                percentage_change = ((end_price - start_price) / start_price) * 100
                coin_percentages[coin] = percentage_change
        except Vote.DoesNotExist:
            continue

    # Find the users with the highest percentage change and award the gem finder badge
    user_percentages = {}
    for coin, percentage in coin_percentages.items():
        user_vote = current_month_votes.filter(coin=coin).latest('id')
        user = user_vote.user
        if user not in user_percentages:
            user_percentages[user] = percentage
        else:
            user_percentages[user] += percentage

    # Find the two users with the highest overall percentage change and award the gem finder badge
    sorted_users = sorted(user_percentages, key=user_percentages.get, reverse=True)
    max_users = sorted_users[:2]  # Get the top two users with the highest percentage change

    for user in max_users:
        user.gem_finder = True
        user.save()
