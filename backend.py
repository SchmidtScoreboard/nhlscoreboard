import requests
import json
from collections import namedtuple

API = 'https://statsapi.web.nhl.com'
API_FLAG = '/api/v1/'
LINESCORE = '/linescore'
GAME = '/game/'
SCHEDULE = 'schedule'
FEED = '/feed/live'
TEAMS = "/teams/"

Period = namedtuple('Period', 'away home')
Color = namedtuple('Color', 'red green blue')
colorMap = {
    # todo fill in color map 
    1: Color(200, 16, 46),
    2: Color(0, 48, 135),
    3: Color(0, 51, 160),
    4: Color(250, 70, 22),
    5: Color(255, 184, 28),
    6: Color(252, 181, 20),
    7: Color(0, 38, 84),
    8: Color(166, 25, 46),
    9: Color(200, 16, 46),
    10: Color(0, 32, 91),
    12: Color(204, 0, 0),
    13: Color(200, 16, 46),
    14: Color(0, 32, 91),
    15: Color(4, 30, 66),
    16: Color(206, 17, 38),
    17: Color(200, 16, 46),
    18: Color(255, 184, 28),
    19: Color(0, 47, 135),
    20: Color(206, 17, 38),
    21: Color(35, 97, 146),
    22: Color(252, 76, 2),
    23: Color(0, 136, 82),
    24: Color(181, 152, 90),
    25: Color(0, 99, 65),
    26: Color(162, 170, 173),
    28: Color(0, 98, 114),
    29: Color(4, 30, 66),
    30: Color(21, 71, 52),
    52: Color(4, 30, 66),
    53: Color(140, 38, 51),
    54: Color(185, 151, 91) }

class Team:
    def __init__(self, team_id, team_name, team_city, abbreviation, team_color):
        self.team_id = team_id
        self.team_name = team_name
        self.team_city = team_city
        self.abbreviation = abbreviation
        self.team_color = team_color
        
    def text_color(self):
        luminance = ((0.299 * self.team_color.red) 
                         + (0.587 * self.team_color.green) 
                         + (0.114 * self.team_color.blue))
        print(luminance)
        if luminance > 0.5:
            # light background, use a dark font
            return Color(0,0,0)
        else:
            #dark backgorund, use a light font
            return Color(1.0, 1.0, 1.0)
        
    def __repr__(self):
        return "{!r}({!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__,
           self.team_id, self.team_name, 
               self.team_city, self.abbreviation, 
               self.team_color)

class Game:
    def __init__(self, away, home, game_id):
        self.away = away
        self.home = home
        
        self.game_id = game_id
        self.refresh()
    def refresh(self):
        game_url = API + API_FLAG + GAME + str(self.game_id) + LINESCORE
        response = requests.get(url = game_url)
        game_data = response.json()
    
        self.period = game_data["currentPeriod"] - 1 #subtract one for sensible indices
        self.current_period_time = game_data.get("currentPeriodTimeRemaining", "20:00")
        self.periods = [Period(p["away"]["goals"], p["home"]["goals"]) for p in game_data["periods"]]
        teams = game_data["teams"]
        away = teams["away"]
        home = teams["home"]
        self.away_score = away["goals"]
        self.home_score = home["goals"]
    def __repr__(self):
        return "{!r}({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__,
            self.away, self.away_score,
            self.home, self.home_score,
            self.game_id, self.period,
            self.current_period_time, self.periods)
  
class NHL:
  def __init__(self):
    schedule_url = API + API_FLAG + SCHEDULE
    team_url = API + API_FLAG + TEAMS
    self.schedule = requests.get(url = schedule_url).json()
    team_response = requests.get(url=team_url).json()
    self.teams = {t["id"]: Team(t["id"], 
      t["teamName"], 
      t["locationName"], 
      t["abbreviation"], 
      colorMap.get(t["id"], Color(1.0,1.0,1.0))) for t in team_response["teams"]}
    if len(self.schedule["dates"]):
      self.games = [Game(
        self.teams[game["teams"]["away"]["team"]["id"]], 
        self.teams[game["teams"]["home"]["team"]["id"]], 
        game["gamePk"]) for game in self.schedule["dates"][0]["games"]]
    else:
      self.games = []
    self.refresh()

  def refresh(self):
    for game in self.games:
      game.refresh()
      
  def team_playing(schedule, team_id):
    if self.schedule["totalGames"] > 0:
        today = self.schedule["dates"][0]
        games = today["games"]
        for game in games:
            teams = game["teams"]
            if teams["away"]["team"]["id"] == team_id:
                return True
            if teams["home"]["team"]["id"] == team_id:
                return True
    return False
    
