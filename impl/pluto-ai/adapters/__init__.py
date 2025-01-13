from .vegas_odds import VegasOddsInterface, VegasOddsPipeline
from .nba_stats import NbaAnalyticsPipeline, NbaAnalyticsInterface


class Adapters:
    vegas_odds: VegasOddsInterface
    nba_analytics: NbaAnalyticsInterface

    def __init__(self):
        self.vegas_odds = VegasOddsPipeline()
        self.nba_analytics = NbaAnalyticsPipeline()
