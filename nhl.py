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


NHL_QUERY = """{
    games {
        common {
            home_team {
                id
                name
                display_name
                abbreviation
                primary_color
                secondary_color
            }
            away_team {
                id
                name
                display_name
                abbreviation
                primary_color
                secondary_color
            }
            status
            ordinal
            start_time
            id
        }
        away_powerplay
        home_powerplay
        away_players
        home_players
    }
}"""


class NHLTeam(Team):
    def __init__(self, team_json):
        self = Team.build(team_json)


class NHLGame(Game):
    def __init__(self, common, away_powerplay, home_powerplay, away_players, home_players):
        self = Game.build(common)
        self.away_powerplay = away_powerplay
        self.home_powerplay = home_powerplay
        self.away_skaters = away_players
        self.home_skaters = home_players


class NHL(League):
    def __init__(self, settings):
        super().__init__(settings)
        self.renderer = NHLRenderer(64, 32)

    def reset(self):
        super().reset()
        self.games = []
        try:

            response = requests.get(url=AWS_URL + "nhl", json: NHL_QUERY).json()
            data = response['data']
            self.games = [NHLGame(game['common'], game['away_powerplay'], game['home_powerplay'],
                                  game['away_skaters'], game['home_skaters']) for game in data['games']]
        except Exception as e:
            print("Error: " + str(e))
            error_title = "Disconnected"
            error_message = "Use the Scoreboard app to get reconnected"
            self.handle_error(error_title, error_message)

    def get_image(self):
        if self.error:
            return self.renderer.draw_error(self.error_title, self.error_message)
        elif self.active_index == -1:
            return self.renderer.draw_info("No games :(")[0]
        else:
            return self.renderer.render(self.games[self.active_index])


class NHLRenderer(Renderer):
    def __init__(self, width, height):
        Renderer.__init__(self, width, height)

    def render(self, game):

        image, draw = self.draw_big_scoreboard(game)
        team_font = ImageFont.load(big_font)
        # add period
        draw.text((5, 22), game.ordinal, font=team_font, fill=(255, 255, 255))

        # add FINAl
        if game.current_period_time == "Final":
            draw.text((37, 22), game.current_period_time,
                      font=team_font, fill=(255, 255, 0))
        else:
            # add powerplay
            message = ""
            powerplay = False
            if game.away_powerplay:
                powerplay = True
                message = game.away.abbreviation
            if game.home_powerplay:
                powerplay = True
                message = game.home.abbreviation
            if 1 < game.away_skaters < 5 and 1 < game.home_skaters < 5:
                powerplay = True
                message = "{}-{}".format(game.away_skaters, game.home_skaters)
            if powerplay:
                w, h = team_font.getsize(message)
                rightPoint = 63 - w - 3
                draw.rectangle(
                    ((rightPoint, 21), (rightPoint+w+2, 30)), fill=(255, 255, 0))
                draw.text((rightPoint+2, 22), message,
                          font=team_font, fill=(0, 0, 0))

        return image
