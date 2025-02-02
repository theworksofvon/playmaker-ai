from config import config
from .interface import VegasOddsInterface, VegasOddsResponse
from typing import List, Literal, Optional, Union
from aiohttp import ClientSession
from datetime import datetime, timezone


class VegasOddsPipeline(VegasOddsInterface):
    def __init__(self) -> None:
        self.api_key = config.ODDS_API_KEY
        self.base_url = "https://api.the-odds-api.com/v4/"
        self.base_params = {"api_key": self.api_key}

    async def get_sports(self) -> VegasOddsResponse:
        url = f"{self.base_url}/sports"
        sports = await self._fetch(url=url)
        return sports

    async def get_current_odds(
        self,
        sport: str | None = "basketball_nba",
        regions: List[str] | str | None = "us",
        markets: List[str] | str | None = "h2h",
    ) -> VegasOddsResponse:
        url = f"{self.base_url}/sports/{sport}/odds"
        if isinstance(markets, list):
            markets = ",".join(markets)
        if isinstance(regions, list):
            regions = ",".join(regions)
        params = {"regions": regions, markets: markets}
        current_odds = await self._fetch(url=url, params=params)
        return current_odds

    async def get_historical_odds(
        self,
        date: int,  # timestamp in milliseconds
        sport: str | None = " basketball_nba",
        regions: Optional[Union[List[str] | str]] = "us",
        markets: Optional[Union[List[str] | str]] = "h2h",
    ) -> VegasOddsResponse:
        url = f"{self.base_url}/historical/sports/{sport}"
        date = datetime.fromtimestamp(date, tz=timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        if isinstance(markets, list):
            markets = ",".join(markets)
        if isinstance(regions, list):
            regions = ",".join(regions)
        params = {"date": date, "regions": regions, "markets": markets}
        historical_odds = await self._fetch(url=url, params=params)
        return historical_odds

    async def _fetch(
        self,
        url: str,
        method: Literal["GET", "POST"] = "GET",
        json: dict | list = None,
        params: dict = None,
    ) -> VegasOddsResponse:
        try:
            params = {**self.base_params, **params} if params else {**self.base_params}
            async with ClientSession() as session:
                async with session.request(
                    method=method, url=url, json=json, params=params
                ) as response:
                    if response.status == 200:
                        return VegasOddsResponse(
                            response=await response.json(), status_code=200
                        )
        except Exception as error:
            return VegasOddsResponse(
                response={"status": "error", "error": error}, status_code=500
            )
