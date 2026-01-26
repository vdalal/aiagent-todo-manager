"""Week boundary calculation utilities using Monday-Sunday weeks."""

from datetime import date, timedelta


def get_week_start(target_date=None):
    """Get the Monday of the week for the given date.

    Weeks run Monday (weekday 0) through Sunday (weekday 6).

    Args:
        target_date: datetime.date object (defaults to today)

    Returns:
        str: ISO date string (YYYY-MM-DD) for Monday of the week
    """
    if target_date is None:
        target_date = date.today()

    # Calculate days to subtract to get to Monday
    days_since_monday = target_date.weekday()
    monday = target_date - timedelta(days=days_since_monday)

    return monday.isoformat()


def get_week_end(target_date=None):
    """Get the Sunday of the week for the given date.

    Weeks run Monday (weekday 0) through Sunday (weekday 6).

    Args:
        target_date: datetime.date object (defaults to today)

    Returns:
        str: ISO date string (YYYY-MM-DD) for Sunday of the week
    """
    if target_date is None:
        target_date = date.today()

    # Get Monday, then add 6 days to get Sunday
    days_since_monday = target_date.weekday()
    monday = target_date - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)

    return sunday.isoformat()
