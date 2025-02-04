from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict


class NbaAnalyticsInterface(ABC):
    """Abstract interface for NBA analytics operations."""

    # ------------------------------
    # PLAYER METHODS
    # ------------------------------
    @abstractmethod
    async def find_player_info(self, name: str) -> pd.DataFrame:
        """
        Find detailed information about a player by name.

        Args:
            name (str): Full name of the player.

        Returns:
            pd.DataFrame: DataFrame containing player details.
        """
        pass

    @abstractmethod
    async def get_player_career_stats(self, name: str) -> pd.DataFrame:
        """
        Fetch career stats for a player by name.

        Args:
            name (str): Full name of the player.

        Returns:
            pd.DataFrame: DataFrame containing career stats.
        """
        pass

    @abstractmethod
    async def get_player_game_logs(self, name: str, season: str) -> pd.DataFrame:
        """
        Fetch player game logs for a specific season.

        Args:
            name (str): Full name of the player.
            season (str): NBA season (e.g., '2023-24').

        Returns:
            pd.DataFrame: DataFrame containing game logs.
        """
        pass

    # ------------------------------
    # TEAM METHODS
    # ------------------------------
    @abstractmethod
    async def get_teams(self) -> List[Dict]:
        """
        Get a list of all NBA teams.

        Returns:
            List[Dict]: List of team details.
        """
        pass

    @abstractmethod
    async def get_team_game_logs(self, team_name: str, season: str) -> pd.DataFrame:
        """
        Fetch team game logs for a specific season.

        Args:
            team_name (str): Full name of the team (e.g., 'Los Angeles Lakers').
            season (str): NBA season (e.g., '2023-24').

        Returns:
            pd.DataFrame: DataFrame containing team game logs.
        """
        pass

    # ------------------------------
    # PLAY-BY-PLAY METHODS
    # ------------------------------
    @abstractmethod
    async def get_play_by_play(self, game_id: str) -> pd.DataFrame:
        """
        Fetch play-by-play data for a specific game.

        Args:
            game_id (str): NBA game ID.

        Returns:
            pd.DataFrame: DataFrame containing play-by-play data.
        """
        pass

    # ------------------------------
    # LIVE GAME METHODS
    # ------------------------------
    @abstractmethod
    async def get_todays_game_scoreboard(self) -> Dict:
        """
        Get today's game scoreboard.

        Returns:
            Dict: Dictionary containing today's game data.
        """
        pass

    # ------------------------------
    # UTILITY METHODS
    # ------------------------------
    @abstractmethod
    async def save_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        """
        Save data to a CSV file.

        Args:
            data (pd.DataFrame): DataFrame to save.
            filename (str): File path for saving the data.
        """
        pass

    @abstractmethod
    async def load_from_csv(self, filename: str) -> pd.DataFrame:
        """
        Load data from a CSV file.

        Args:
            filename (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded data.
        """
        pass
