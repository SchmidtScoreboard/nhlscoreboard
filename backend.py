import requests
import json
from collections import namedtuple
import pytz
from dateutil.parser import *

API = 'https://statsapi.web.nhl.com'
API_FLAG = '/api/v1/'
LINESCORE = '/linescore'
GAME = '/game/'
SCHEDULE = 'schedule'
FEED = '/feed/live'
TEAMS = "/teams/"

Period = namedtuple('Period', 'away home')
Color = namedtuple('Color', 'red green blue')
primaryColorMap = {
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

secondaryColorMap = {
    # todo fill in color map 
    1: Color(0, 0, 0),
    2: Color(252, 76, 2),
    3: Color(200, 16, 46),
    4: Color(0, 0, 0),
    5: Color(0, 0, 0),
    6: Color(0, 0, 0),
    7: Color(252, 181, 20),
    8: Color(0, 30, 98),
    9: Color(198, 146, 20),
    10: Color(255, 255, 255),
    12: Color(162, 169, 175),
    13: Color(185, 151, 91),
    14: Color(255, 255, 255),
    15: Color(200, 16, 46),
    16: Color(204, 138, 0),
    17: Color(255, 255, 255),
    18: Color(4, 30, 66),
    19: Color(255, 184, 28),
    20: Color(243, 188, 82),
    21: Color(111, 38, 61),
    22: Color(4, 30, 66),
    23: Color(0, 32, 91),
    24: Color(249, 86, 2),
    25: Color(162, 170, 173),
    26: Color(0, 0, 0),
    28: Color(229, 114, 0),
    29: Color(200, 16, 46),
    30: Color(166, 25, 46),
    52: Color(162, 170, 173),
    53: Color(226, 214, 181),
    54: Color(0, 0, 0) }
class Team:
    def __init__(self, team_id, team_name, team_city, abbreviation, team_color, secondary_color):
        self.team_id = team_id
        self.team_name = team_name.upper()
        self.team_city = team_city.upper()
        self.abbreviation = abbreviation
        self.team_color = team_color
        self.team_secondary_color = secondary_color
        
    def text_color(self):
        luminance = ((0.299 * self.team_color.red) 
                         + (0.587 * self.team_color.green) 
                         + (0.114 * self.team_color.blue))
        if luminance > 0.5:
            # light background, use a dark font
            return Color(0,0,0)
        else:
            #dark backgorund, use a light font
            return Color(255.0, 255.0, 255.0)
        
    def __repr__(self):
        return "{!r}({!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__,
           self.team_id, self.team_name, 
               self.team_city, self.abbreviation, 
               self.team_color, self.team_secondary_color)

class Game:
    def __init__(self, away, home, game_id, start_time):
        self.away = away
        self.home = home
        
        self.game_id = game_id
        time = parse(start_time).astimezone(pytz.timezone("America/Chicago"))
        self.start_hour = time.hour % 12
        self.start_afternoon = "PM" if time.hour > 12 else "AM"
        self.start_minute = time.minute
        self.refresh()
    def refresh(self):
        game_url = API + API_FLAG + GAME + str(self.game_id) + LINESCORE
        response = requests.get(url = game_url)
        game_data = response.json()
        self.period = game_data["currentPeriod"]
        self.ordinal = game_data["currentPeriodOrdinal"] if self.period >= 1 else "{}:{:02d} {}".format(self.start_hour, self.start_minute, self.start_afternoon)
        self.current_period_time = game_data.get("currentPeriodTimeRemaining", "20:00")
        self.periods = [Period(p["away"]["goals"], p["home"]["goals"]) for p in game_data["periods"]]
        teams = game_data["teams"]
        away = teams["away"]
        home = teams["home"]
        self.away_score = away["goals"]
        self.home_score = home["goals"]
        self.away_powerplay = away["powerPlay"]
        self.home_powerplay = home["powerPlay"]
        self.home_skaters = home["numSkaters"]
        self.away_skaters = away["numSkaters"]
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
      primaryColorMap.get(t["id"], Color(0,0,0)),
      secondaryColorMap.get(t["id"], Color(255, 255, 255))) for t in team_response["teams"]}
    if len(self.schedule["dates"]):
      self.games = [Game(
        self.teams[game["teams"]["away"]["team"]["id"]], 
        self.teams[game["teams"]["home"]["team"]["id"]], 
        game["gamePk"],
        game["gameDate"]) for game in self.schedule["dates"][0]["games"]]
    else:
      self.games = []
    self.refresh()

  def refresh(self):
    for game in self.games:
      game.refresh()
      
  def team_playing(self, team_id):
    for game in self.games:
        if game.home.team_id == team_id or game.away.team_id == team_id:
            if game.current_period_time != "Final" and game.period != 0:
                return self.games.index(game)
    return None
    
