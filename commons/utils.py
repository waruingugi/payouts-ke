from datetime import datetime, timedelta

from django.core.cache import cache
from django.utils.timezone import localtime
from django_stubs_ext.aliases import ValuesQuerySet

from commons.constants import GraphDurationFilter, ProbabilityPayoutFilter
from commons.models import Payouts
from commons.raw_logger import logger


def get_minute_intervals(interval: int, minutes: int) -> list[datetime]:
    """Get a list of time intervals: [13:30pm, 13:25pm, ...]
    Args interval: An int value of the interval in minutes. Example interval=5
    Args minutes: An int value of how many minutes to date back the time."""
    now = localtime()

    # Round down to nearest interval
    rounded_minute = (now.minute // interval) * interval

    # Create the stop time which is ahead of local time
    stop_time = now.replace(minute=rounded_minute, second=0, microsecond=0)

    # Create the start time which is behind current localtime
    start_time = stop_time - timedelta(minutes=minutes)

    time_intervals = [start_time]
    current_time = start_time

    while current_time < stop_time:
        current_time = current_time + timedelta(minutes=interval)
        time_intervals.append(current_time)

    return time_intervals


def calculate_intervals(
    payouts: ValuesQuerySet, filter: ProbabilityPayoutFilter
) -> list:
    """Find indices of payouts where payout > filter.value"""
    high_payout_indices = [
        i for i, payout in enumerate(payouts) if payout > filter.value
    ]

    # Calculate intervals
    intervals = []
    for i in range(len(high_payout_indices) - 1):
        # The interval is the difference in indices - 1 (to count the payouts in between)
        interval = high_payout_indices[i + 1] - high_payout_indices[i] - 1
        intervals.append(interval)

    return intervals


def get_payout_intervals(filter: ProbabilityPayoutFilter, app_name: str):
    """Get payout intervals for a filter"""
    # logger.info(f"Calculating payouts over {filter.value}x for {app_name}")

    app_payouts = f"{app_name}_payouts"
    payouts = cache.get(app_payouts, {})

    if not payouts:
        payouts = Payouts.objects.filter(app=app_name).values_list("payout", flat=True)

        # Save to cache as the computation is slow and expensive
        cache.set(app_payouts, payouts, timeout=60)

    # Find indices of payouts where payout > filter.value
    intervals = calculate_intervals(payouts, filter)

    return intervals


def get_probability(intervals: list, distance: int) -> float:
    """Calculate probability of payout x happening at interval y"""
    # Count the number of payouts that occurred at or before the current interval
    payouts_at_or_before = sum(1 for interval in intervals if interval <= distance)

    # Total number of payouts observed
    total_payouts = len(intervals)

    if total_payouts > 0:
        # The empirical probability of a payout occurring by, say, the 44th interval
        probability = (payouts_at_or_before / total_payouts) * 100
        return probability
    return 0.0


def get_count_since_last_high_payout(payout: float, app_name: str) -> int:
    """Get count since the last high payout"""
    last_high_payout = Payouts.objects.filter(app=app_name, payout__gt=payout).first()

    if last_high_payout:
        return Payouts.objects.filter(
            app=app_name, created_at__gt=last_high_payout.created_at
        ).count()
    else:
        return Payouts.objects.filter(app=app_name).count()


def payouts_filter_probabilities(app_name: str) -> dict[str, str]:
    """Calculate probabilities of all payouts in the ProbabilityPayoutFilter"""
    app_prob = f"{app_name}_probabilities"

    probabilities = cache.get(app_prob, {})

    if not probabilities:
        # Calculate the probabilities
        # logger.info(f"Calculate probabilities of all payouts in {app_name}")

        for filter in ProbabilityPayoutFilter:
            intervals = get_payout_intervals(filter, app_name)

            payout_count = get_count_since_last_high_payout(filter.value, app_name)

            # The probability of the payout x happening right now
            over_x_prob_now = get_probability(intervals, payout_count)

            # The probability of the payout x happening in the next 15 mins.
            # If a payout takes roughly 26 seconds, then 15 mins is roughly 35 payouts in the future
            over_x_prob_soon = get_probability(intervals, payout_count + 35)

            # The average of the payout x happening in the above two time frames
            over_x_prob = (over_x_prob_now + over_x_prob_soon) / 2

            # Get time now and time in 15 minutes
            time_now = localtime()
            time_soon = time_now + timedelta(minutes=15)

            over_x_time_now = time_now.strftime("%I:%M%p").lower()
            over_x_time_soon = time_soon.strftime("%I:%M%p").lower()

            probabilities[f"Over {filter.value}x"] = {
                "probability": over_x_prob,
                "event_start": over_x_time_now,
                "event_end": over_x_time_soon,
            }

        # Save to cache as the computation is slow and expensive
        cache.set(app_prob, probabilities, timeout=15)

    return probabilities


def payouts_query(
    app_name,
    *,
    selected_page_size: int,
    selected_duration: int,
    selected_min_value: float,
) -> ValuesQuerySet:
    "Populate payouts based on the filters provided"
    logger.info(f"Populate payouts for {app_name}")
    start_time = localtime() - timedelta(seconds=selected_duration)
    payouts_query = Payouts.objects.filter(
        app=app_name,
        created_at__gt=start_time,
        payout__gte=selected_min_value,
    ).values("payout", "created_at")[:selected_page_size]

    return payouts_query


def get_graph_values(
    app_name, *, selected_graph_duration: int, data_points: int = 12
) -> tuple:
    "Create the graph's x labels and y values"
    # logger.info(f"Plot payouts trend graph for {app_name}")
    minute_duration = selected_graph_duration // 60
    interval = minute_duration // data_points

    # A list of datetime objecsts. Example: [<datetime>, ..., <datetime>]
    time_intervals: list = get_minute_intervals(
        interval=interval, minutes=minute_duration
    )

    # The largest duration in the Graph filter is 24 hours
    x_hours_ago = localtime() - timedelta(
        hours=GraphDurationFilter.TWENTY_FOUR_HOURS.value
    )

    # Get data of the last 24 hours only as this greatly reduces the query time
    app_graph_payouts = f"{app_name}_get_graph_payouts_filter"

    payouts = cache.get(app_graph_payouts, {})

    if not payouts:
        payouts = Payouts.objects.filter(
            app=app_name, created_at__gt=x_hours_ago
        ).values("created_at", "payout")
        cache.set(app_graph_payouts, payouts, timeout=60)

    """
    This code block calculates the average payouts at intervals
    (e.g 5 minute intervals) while still only hiting the database only once.
    """
    y_values: list[str] = []
    for time_ in time_intervals:
        start_time = time_
        end_time = time_ + timedelta(minutes=interval)

        payouts_list = []
        for obj in payouts:
            if start_time <= obj["created_at"] <= end_time:
                payouts_list.append(obj["payout"])

        if payouts_list:
            payouts_avg = round(  # Calculate the average
                (sum(payouts_list) / len(payouts_list)), 2
            )
        else:
            payouts_avg = 0.0

        y_values.append(str(payouts_avg))

    # Append one more label for visual 'continuity', this value label will be empty
    empty_label = time_intervals[-1] + timedelta(minutes=interval)
    time_intervals.append(empty_label)

    x_labels = [time_.strftime("%I:%M%p").lower() for time_ in time_intervals]

    return x_labels, y_values
