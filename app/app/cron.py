from datetime import datetime, timedelta
from core.models import Vote, Coin, User


def calculate_monthly_votes():
    now = datetime.now()
    if now.day != 28:
        return  # Only run on the 1st day of the month

    # Calculate the start and end dates of the current month
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)

    # Get all votes for the current month
    current_month_votes = Vote.objects.filter(created_at__gte=current_month_start, created_at__lt=next_month_start)

    # Calculate percentage change for each coin
    coin_percentages = {}
    for coin in Coin.objects.all():
        try:
            start_vote = current_month_votes.filter(coin=coin).earliest('created_at')
            end_vote = current_month_votes.filter(coin=coin).latest('created_at')
            start_price = start_vote.coin.price
            end_price = end_vote.coin.price
            if start_price and end_price:
                percentage_change = ((end_price - start_price) / start_price) * 100
                coin_percentages[coin] = percentage_change
        except Vote.DoesNotExist:
            continue

    # Find the coin with the highest percentage change
    max_percentage_coin = max(coin_percentages, key=coin_percentages.get)

    # Get users who voted for the coin with the highest percentage change in the current month
    users_with_max_percentage = User.objects.filter(vote__coin=max_percentage_coin, vote__created_at__gte=current_month_start, vote__created_at__lt=next_month_start)

    # Award the gem_finder badge to users
    for user in users_with_max_percentage:
        user.gem_finder = True
        user.save()


def reset_votes_left():
    now = datetime.now()
    if now.day != 1:
        return  # Only run on the 1st day of the month

    users = User.objects.all()

    for user in users:
        user.votes_left = 3
        user.save()
