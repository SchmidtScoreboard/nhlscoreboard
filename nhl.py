import requests
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
import pytz
from dateutil.parser import *
from common import * 

API = 'https://statsapi.web.nhl.com'
API_FLAG = '/api/v1/'
LINESCORE = '/linescore'
GAME = '/game/'
SCHEDULE = 'schedule'
FEED = '/feed/live'
TEAMS = "/teams/"

Period = namedtuple('Period', 'away home')

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
class NHLTeam(Team):
    def __init__(self, id, name, display_name, city, abbreviation, primary_color, secondary_color):
        Team.__init__(self, id, name.upper(), display_name.upper(), city.upper(), abbreviation.upper(), primary_color, secondary_color)
        
        

class NHLGame(Game):
    def __init__(self, id, away, home, start_time):
        Game.__init__(self, id, away, home, start_time=start_time)
        time = parse(start_time).astimezone(pytz.timezone("America/Chicago"))
        self.start_hour = time.hour % 12
        if self.start_hour == 0:
            self.start_hour = 12
        self.start_afternoon = "PM" if time.hour >= 12 else "AM"
        self.start_minute = time.minute
        self.refresh()
    def refresh(self):
        game_url = API + API_FLAG + GAME + str(self.id) + LINESCORE
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
        if self.current_period_time == "Final":
            self.status = GameStatus.END
        elif self.current_period_time == "END":
            if self.period >= 3 and self.away_score != self.home_score:
                self.status = GameStatus.END
            else:
                self.status = GameStatus.INTERMISSION
                self.ordinal += " INT"
        else:
            if self.current_period_time != "20:00":
                self.status = GameStatus.ACTIVE
            else:
                self.status = GameStatus.PREGAME
  

short_names = {
    10: "Leafs",
    12: "Canes",
    16: "B Hawks",
    29: "B Jackets",
    54: "Knights"
}
class NHL(League):
  def __init__(self, settings):
    super().__init__(settings)

  def reset(self):
    super().reset()
    schedule_url = API + API_FLAG + SCHEDULE
    team_url = API + API_FLAG + TEAMS
    self.games=[]
    self.teams=[]
    try:
        self.schedule = requests.get(url = schedule_url).json()
        team_response = requests.get(url=team_url).json()
        self.teams = {t["id"]: NHLTeam(t["id"], 
        t["teamName"], 
        t["teamName"] if len(t["teamName"]) < 10 else short_names[t["id"]],
        t["locationName"], 
        t["abbreviation"], 
        primaryColorMap.get(t["id"], Color(0,0,0)),
        secondaryColorMap.get(t["id"], Color(255, 255, 255))) for t in team_response["teams"]}
        if len(self.schedule["dates"]):
            self.games = [NHLGame(
                game["gamePk"],
                self.teams[game["teams"]["away"]["team"]["id"]], 
                self.teams[game["teams"]["home"]["team"]["id"]], 
                start_time=game["gameDate"]) for game in self.schedule["dates"][0]["games"]]
        else:
            self.games = []
        self.refresh()
    except Exception as e:
        print("Error: " + str(e))
        error = "Disconnected"
        self.handle_error(error)

  def get_image(self):
    renderer = NHLRenderer(64, 32)
    if self.error:
      return renderer.draw_error(self.error_message)
    elif self.active_index == -1:
        return renderer.draw_info("No games :(")[0]
    else:
      return renderer.render(self.games[self.active_index])


class NHLRenderer(Renderer):
    def __init__(self, width, height):
        Renderer.__init__(self, width, height)


    def render(self, game):
        
        image, draw = self.draw_big_scoreboard(game)
        team_font = ImageFont.load(big_font)
        #add period
        draw.text((5, 22), game.ordinal, font=team_font, fill=(255, 255, 255))

        #add FINAl
        if game.current_period_time == "Final":
            draw.text((37, 22), game.current_period_time, font=team_font, fill=(255, 255, 0)) 
        else:
            #add powerplay
            message = ""
            powerplay = False
            if game.away_powerplay:
                powerplay = True
                message = game.away.abbreviation
            if game.home_powerplay:
                powerplay = True
                message = game.home.abbreviation
            if 1 < game.away_skaters < 5 and 1 <game.home_skaters < 5:
                powerplay = True
                message = "{}-{}".format(game.away_skaters, game.home_skaters)
            if powerplay:
                w, h = team_font.getsize(message) 
                rightPoint = 63 - w - 3
                draw.rectangle(((rightPoint,21),(rightPoint+w+2,30)), fill=(255,255,0))
                draw.text((rightPoint+2,22), message, font=team_font, fill=(0,0,0))

        return image
