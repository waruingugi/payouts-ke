from enum import Enum


class BettingApps(str, Enum):
    """Bettings sites supported on the server"""

    BETIKA = "BETIKA"
    BETGR8 = "BETGR8"
    ODIBETS = "ODIBETS"
    WINPESA = "WINPESA"

    @classmethod
    def list_(cls) -> list:
        statuses = {status.value for status in cls}
        return list(statuses)


# APP choices is a list of choices generated from BettingApps
APP_CHOICES = [
    (BettingApps.BETIKA.name, BettingApps.BETIKA.value),
    (BettingApps.BETGR8.name, BettingApps.BETGR8.value),
    (BettingApps.ODIBETS.name, BettingApps.ODIBETS.value),
    (BettingApps.WINPESA.name, BettingApps.WINPESA.value),
]


class ProbabilityPayoutFilter(Enum):
    """Filters values for which we use to calculate probabilities"""

    OVER_TWENTY_FIVE_FILTER = 25.0
    OVER_FIFTY_FILTER = 50.0
    OVER_ONE_HUNDRED = 100.0


class PageSizeFilter(Enum):
    """Number of payouts to show per page"""

    THREE_HUNDRED = 300
    FIVE_HUNDRED = 500

    @classmethod
    def labels(cls) -> dict:
        return {
            "300": cls.THREE_HUNDRED.value,
            "500": cls.FIVE_HUNDRED.value,
        }


class DurationFilter(Enum):
    """Show payouts in this duration.
    Example: show payouts in the past TWO_HOURS"""

    TWO_HOURS = 60 * 60 * 2
    FOUR_HOURS = 60 * 60 * 4
    EIGHT_HOURS = 60 * 60 * 8

    @classmethod
    def labels(cls) -> dict:
        return {
            "Last 2 hours": cls.TWO_HOURS.value,
            "Last 4 hours": cls.FOUR_HOURS.value,
            "Last 8 hours": cls.EIGHT_HOURS.value,
        }


class MinValueFilter(Enum):
    """Filter to show minimum value payouts"""

    OVER_ONE = 1.0
    OVER_FIVE = 5.0
    OVER_TEN = 10.0
    OVER_FIFTY = 50.0
    OVER_HUNDRED = 100.0

    @classmethod
    def labels(cls) -> dict:
        return {
            "Over 1.0x": cls.OVER_ONE.value,
            "Over 5.0x": cls.OVER_FIVE.value,
            "Over 10.0x": cls.OVER_TEN.value,
            "Over 50.0x": cls.OVER_FIFTY.value,
            "Over 100.0x": cls.OVER_HUNDRED.value,
        }


class GraphDurationFilter(Enum):
    """Filter for graphs"""

    ONE_HOUR = 60 * 60 * 1
    THREE_HOURS = 60 * 60 * 3
    TWENTY_FOUR_HOURS = 60 * 60 * 24

    @classmethod
    def labels(cls) -> dict:
        return {
            "Last 1 hour": cls.ONE_HOUR.value,
            "Last 3 hours": cls.THREE_HOURS.value,
            "Last 24 hours": cls.TWENTY_FOUR_HOURS.value,
        }
