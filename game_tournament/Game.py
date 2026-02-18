"""
Docstring for game_tournament.Game
Game class represents a game in the tournament. It has a name, a sport, and a list of teams.
"""
import random
import json
from Team import Team
from Sport import Sport
from Athlete import Athlete

class Game:
    """ Game class represents a game in the tournament. It has two teams and a score"""
    def __init__(self, A:Team, B:Team):
        """ Custom constructor for Game class. """
        self.set_team(A, "local")
        self.set_team(B,"visitor")
        self.score = {
            A.name: 0, B.name: 0
            }
    def set_team(self, team, role):
        """ Set a team for the game. """
        if isinstance(team, Team):
            if role == "local":
                self.team_a = team
            elif role == "visitor":
                self.team_b = team
            else:
                raise ValueError("Role must be 'local' or 'visitor'.")
        else:
            raise ValueError("Only Team objects can be set as a team.")
    def play(self):
        """ Simulate playing the game by randomly assigning scores to each team. """
        self.score[self.team_a.name] = random.randint(0, Sport.max_score[self.team_a.sport.name])
        self.score[self.team_b.name] = random.randint(0, Sport.max_score[self.team_b.sport.name])
    def __str__(self):
        """ String representation of the Game class. """
        return f"{self.team_a.name} vs {self.team_b.name} - Score: {self.score[self.team_a.name]}:{self.score[self.team_b.name]}"
    def __repr__(self):
        """ String representation of the Game class. """
        return f"Game(team_a={repr(self.team_a)}, team_b={repr(self.team_b)}, score={self.score})"
    def to_json(self):
        """ Convert the Game object to a JSON string. """
        return {
            "team_a": self.team_a.to_json(),
            "team_b": self.team_b.to_json(),
            "score": self.score
        }

def a_game():
    """ Example usage of the Game class. """
    players_mex = ['Chicharito','Piojo','Guardado','Hector Moreno','Rafa Marquez','Salcido','Vela','Dos Santos','Herrera','Layun','Corona']
    players_arg = ['Messi','Di Maria','Aguero','Higuain','Mascherano','Biglia','Dybala','Paredes','Tagliafico','Otamendi','Zabaleta']

    sport = Sport("Futbol", 11, "FIFA")
    team_mex = Team("Mexico", sport)
    team_arg = Team("Argentina", sport)
    for player in players_mex:
        team_mex.add_athlete(Athlete(player))
    for player in players_arg:
        team_arg.add_athlete(Athlete(player))
    game = Game(team_mex, team_arg)
    game_string = game.to_json()
    return game_string

def save_game_to_json(game_data, filename):
    """ Save the game object to a JSON file. """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(game_data, f, indent=4)

def a_tournament():
    """ Example usage of the Game class. """
    players_mex = ['Chicharito','Piojo','Guardado','Hector Moreno','Rafa Marquez','Salcido','Vela','Dos Santos','Herrera','Layun','Corona']
    players_arg = ['Messi','Di Maria','Aguero','Higuain','Mascherano','Biglia','Dybala','Paredes','Tagliafico','Otamendi','Zabaleta']
    players_peru= ['Farfan','Guerrero','Carrizo','Andre','Tapia','Aquino','advincula','carlos zambrano','miguel araujo','aldo corzo','pedro gallese']
    players_chile=['Vargas','Alexis Sanchez','Puch','Vidal','Aranguiz','Medel','beausejour','jara','Roco','Mena','Bravo']
    players_brasil=['Ronaldinho','Ronaldo','Rivaldo','Silva','Emerson','kleberson','cafu','roberto carlos','lucio','dida']
    players_france=['mbappe','giroud','griezmann','dembele','kante','rabiot','varane','umtiti','hernandez','pavard','lloris']
    players_alemania=['Klose','Ozil','Schurrle','khedira','kroos','krammer','muller','howedes','hummels','boateng','lahm','neuer']
    players_españa=['iniesta','pedro','villa','xavi','busquets','alonso','capdevilla','pique','puyol','ramos','casillas']




    sport = Sport("Futbol", 11, "FIFA")
    team_mex = Team("Mexico", sport)
    team_arg = Team("Argentina", sport)
    team_peru = Team("Peru",sport)
    team_chile = Team("Chile",sport)
    team_brasil = Team("brasil",sport)
    team_france = Team("Francia",sport)
    team_alemania = Team("Francia",sport)
    team_españa = Team("España",sport)

    for player in players_mex:
        team_mex.add_athlete(Athlete(player))
    for player in players_arg:
        team_arg.add_athlete(Athlete(player))
    for player in players_peru:
        team_peru.add_athlete(Athlete(player))
    for player in players_chile:
        team_chile.add_athlete(Athlete(player))
    for player in players_brasil:
        team_brasil.add_athlete(Athlete(player))
    for player in players_france:
        team_france.add_athlete(Athlete(player))
    for player in players_alemania:
        team_alemania.add_athlete(Athlete(player))
    for player in players_españa
        team_españa.add_athlete(Athlete(player))


       


    game = Game(team_mex, team_arg)
    game_string = game.to_json()
    return game_string



if __name__ == "__main__":
    string_game = a_game()
    save_game_to_json(string_game, "game.json")
    print(string_game)