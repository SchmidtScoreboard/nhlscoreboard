import requests
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
import pytz
from dateutil.parser import *
from common import * 

API = 'http://statsapi.mlb.com'
API_FLAG = '/api/v1/'
LINESCORE = '/linescore'
GAME = '/game/'
SCHEDULE = 'schedule?sportId=1'
FEED = '/feed/live'
TEAMS = "/teams?sportId=1"

primaryColorMap = {
    108: Color(186, 0, 33),
    109: Color(167, 25, 48),
    110: Color(223, 70, 1),
    111: Color(198, 1, 31),
    112: Color(14, 51, 134),
    113: Color(198, 1, 31),
    114: Color(227, 25, 55),
    115: Color(51, 0, 111),
    116: Color(12, 35, 64),
    117: Color(0, 45, 98),
    118: Color(0, 70, 135),
    119: Color(0, 90, 156),
    120: Color(171, 0, 3),
    121: Color(0, 45, 114),
    133: Color(0, 56, 49),
    134: Color(253, 184, 39),
    135: Color(0, 45, 98),
    136: Color(0, 92, 92),
    137: Color(39, 37, 31),
    138: Color(196, 30, 58),
    139: Color(214, 90, 36),
    140: Color(0, 50, 120),
    141: Color(19, 74, 142),
    142: Color(0, 43, 92),
    143: Color(232, 24, 40),
    144: Color(19, 39, 79),
    145: Color(39, 37, 31),
    146: Color(0, 0, 0),
    147: Color(12, 35, 64),
    158: Color(19, 41, 75)
}


secondaryColorMap = {
    108: Color(196, 206, 212),
    109: Color(227, 212, 173),
    110: Color(39, 37, 31),
    111: Color(255, 255, 255),
    112: Color(204, 52, 51),
    113: Color(0, 0, 0),
    114: Color(12, 35, 64),
    115: Color(196, 206, 212),
    116: Color(250, 70, 22),
    117: Color(244, 145, 30),
    118: Color(189, 155, 96),
    119: Color(239, 62, 66),
    120: Color(20, 34, 90),
    121: Color(252, 89, 16),
    133: Color(239, 178, 30),
    134: Color(39, 37, 31),
    135: Color(162, 170, 173),
    136: Color(196, 206, 212),
    137: Color(253, 90, 30),
    138: Color(12, 35, 64),
    139: Color(255, 255, 255),
    140: Color(192, 17, 31),
    141: Color(177, 179, 179),
    142: Color(211, 17, 69),
    143: Color(0, 45, 114),
    144: Color(206, 17, 65),
    145: Color(196, 206, 212),
    146: Color(0, 163, 224),
    147: Color(255, 255, 255),
    158: Color(182, 146, 46)
}
class MLBTeam(Team):
    def __init__(self, id, name, display_name, city, abbreviation, primary_color, secondary_color):
        Team.__init__(self, id, name.upper(), display_name.upper(), city.upper(), abbreviation.upper(), primary_color, secondary_color)
        
    
class MLBGame(Game):
    def __init__(self, id, away, home, start_time):
        Game.__init__(self, id, away, home, start_time=start_time)
        time = parse(start_time).astimezone(pytz.timezone("America/Chicago"))
        self.start_hour = time.hour % 12
        self.start_afternoon = "PM" if time.hour > 12 else "AM"
        self.start_minute = time.minute
        self.refresh()
    def refresh(self):
        game_url = API + API_FLAG + GAME + str(self.id) + LINESCORE
        response = requests.get(url = game_url)
        game_data = response.json()
        self.inning = game_data.get("currentInning", 0)
        self.is_inning_top = game_data.get("isTopInning", False)
        self.ordinal = game_data.get("currentInningOrdinal", "") if self.inning >= 1 else "{}:{:02d} {}".format(self.start_hour, self.start_minute, self.start_afternoon)
        teams = game_data["teams"]
        away = teams["away"]
        home = teams["home"]
        self.away_score = away.get("runs", 0)
        self.home_score = home.get("runs", 0)
        if self.inning <= 0:
            self.status = GameStatus.PREGAME
        elif self.inning >0:
            self.status = GameStatus.ACTIVE
  

short_names = {
}
class MLB(League):
  def __init__(self):
    super().__init__()
  
  def reset(self):
    super().reset()
    schedule_url = API + API_FLAG + SCHEDULE
    team_url = API + API_FLAG + TEAMS
    self.teams = []
    self.games = []
    try:
      self.schedule = requests.get(url = schedule_url).json()
      team_response = requests.get(url = team_url).json()
      self.teams = {t["id"]: MLBTeam(t["id"], 
        t["teamName"], 
        t["teamName"] if len(t["teamName"]) < 10 else short_names[t["id"]],
        t["locationName"], 
        t["abbreviation"], 
        primaryColorMap.get(t["id"], Color(0,0,0)),
        secondaryColorMap.get(t["id"], Color(255, 255, 255))) for t in team_response["teams"]}
      if len(self.schedule["dates"]):
        self.games = [MLBGame(
          game["gamePk"],
          self.teams[game["teams"]["away"]["team"]["id"]], 
          self.teams[game["teams"]["home"]["team"]["id"]], 
          start_time=game["gameDate"]) for game in self.schedule["dates"][0]["games"]]
      else:
        self.games = []
      self.refresh()
    except:
      error = "blah"
      self.handle_error(error)

  def get_image(self):
    renderer = MLBRenderer(64, 32)
    if self.error:
      return renderer.draw_error(self.error_message)
    elif self.active_index == -1:
      return renderer.render_no_games()
    else:
      return renderer.render(self.games[self.active_index])

class MLBRenderer(Renderer):
    def __init__(self, width, height):
        Renderer.__init__(self, width, height)


    def render(self, game):
        
        image, draw = self.draw_small_scoreboard(game)
        team_font = ImageFont.load(big_font)

        return image
