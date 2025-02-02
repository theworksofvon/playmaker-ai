import asyncio

# from agents import aggregator, twitter_poster
# from agency.agency import Agency
from adapters import Adapters
from utils import save_to_csv


async def main():

    # agency = Agency([aggregator, twitter_poster])

    # resp = await agency.run(
    #     starting_prompt="What are all of the actions you can currently do ?"
    # )

    # print(f"Response from Agency: {resp}")
    adapters = Adapters()

    resp = adapters.nba_analytics.get_team_game_logs("Los Angeles Lakers", "2024-25")

    print(f"career stats: {resp}")
    


if __name__ == "__main__":
    asyncio.run(main())
