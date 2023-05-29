"""Tasks to run with celery."""
from operator import itemgetter

from celery import shared_task
from datetime import datetime

from core.models import Vote, Coin, User


@shared_task
def calculate_votes():
    now = datetime.now()
    current_month = now.month

    # Pobierz wszystkie głosy oddane w danym dniu
    votes = Vote.objects.filter(created_at__month=current_month)

    coin_changes = []

    for vote in votes:
        coin_id = vote.coin.coin_id
        coin = Coin.objects.get(coin_id=coin_id)
        price_at_vote = coin.price
        current_price = coin.price
        price_change = ((current_price - price_at_vote) / price_at_vote) * 100

        coin_changes.append((coin_id, price_change))

    if coin_changes:
        coin_with_highest_change = max(coin_changes, key=itemgetter(1))[0]

        User.objects.filter(vote__coin__coin_id=coin_with_highest_change).update(gem_finder=True)


@shared_task
def reset_votes_left():
    """Reset remaining votes."""
    users = User.objects.all()

    for user in users:
        user.votes_left = 3
        user.save()
