import random
import json
from Game import Game
from Team import Team
from Sport import Sport
from Athlete import Athlete

class Tournament:
    """Tournament class represents a tournament. It has a name, a list of games, and list of teams."""
    def __init__(self,name):
        """Custom constructor for Tournament class"""
        self.name = name
        self.games = []
        self.teams = []
    def add_teams (self, team):
        """Add a team to the tournament """
        if isinstance (team, Team):
            self.games.append(team)
        else:
            raise ValueError ( "Only Team object can be added as a team. ")
        
    def add_teams (self, game):
        """Add a team to the tournament """
        if isinstance (game, Game):
            self.games.append(game)
        else:
            raise ValueError ( "Only game object can be added as a team. ")

    def _str_ (self):
        """String representation of the Tournament class."""
        return f"Tournament(name={self.name}, Teams: {len(self.teams)}, Games: {len(self.games)}"
    
    def _repr_(self):
        """String representation of the Tournament class."""
        return f"Tournament(name={self.name}, Teams={len(self.teams)}, Games: {len(self.games)}"
    def to_json(self):
        return {
            "name": self.name,
            "teams":[team.to_json() for team in self.teams],
            "games":[game.to_json() for game in self.games]
        }
    def load_json(self,filename):
        with open(filename, 'r', encoding = 'utf-8') as f:data  = json.load(f)
        data = json.load(f)
        json_data = json.loads(data)
        print(f"ITEMS IN DATA LIST: {len(data)}")
        print(f"Data:{data[0]}")
        for team_data in data["teams"]:
            team = Team(team_data["name"],team_data["sport"])
            Sport_name = team_data["Sport"]["Name"]
            Sport_league = team_data["Sport"]["league"]
            sport_num_players = team_data["sport"]["num_players"]
            sport = Sport(Sport_name, sport_num_players, Sport_league)
            team = Team(team_name, sport)
            players = team_data["athletes"]
            for player in players:
                 team.add_athlete(Athlete(player))
            self.add_team(team)

        
if __name__ == "__main__":
    tournament = Tournament("FIFA WORLD CUP")
    tournament.load_json("tournament.json")
    print(tournament)
