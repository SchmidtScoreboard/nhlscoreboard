import requests
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
import pytz
from dateutil.parser import *
from common import *

NHL_QUERY = """{
    games {
        common {
            home_team {
                id
                name
                city
                display_name
                abbreviation
                primary_color
                secondary_color
            }
            away_team {
                id
                name
                city
                display_name
                abbreviation
                primary_color
                secondary_color
            }
            away_score
            home_score
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


class NHLGame(Game):
    def __init__(self, timezone, common, away_powerplay, home_powerplay, away_players, home_players):
        Game.__init__(self, timezone, common)
        self.away_powerplay = bool(away_powerplay)
        self.home_powerplay = bool(home_powerplay)
        self.away_skaters = int(away_players)
        self.home_skaters = int(home_players)


class NHL(League):
    def __init__(self, settings, timezone):
        super().__init__(settings, timezone)
        self.renderer = NHLRenderer(64, 32)

    def reset(self):
        super().reset()
        # try:
        response = requests.get(
            url=AWS_URL + "nhl", json={'query': NHL_QUERY}).json()
        data = response['data']
        self.games = [NHLGame(self.timezone, game['common'], game['away_powerplay'], game['home_powerplay'],
                              game['away_players'], game['home_players']) for game in data['games']]
        # except Exception as e:
        #     log.error("Error: " + str(e))
        #     error_title = "Disconnected"
        #     error_message = "Use the Scoreboard app to get reconnected"
        #     self.handle_error(error_title, error_message)

    def get_image(self):
        if self.active_index == -1:
            return self.renderer.draw_info("No games :(")[0]
        elif self.error:
            return self.renderer.draw_error(self.error_title, self.error_message)
        else:
            game = self.games[self.active_index]
            return self.renderer.render(game)


class NHLRenderer(Renderer):
    def __init__(self, width, height):
        Renderer.__init__(self, width, height)

    def render(self, game):

        image, draw = self.draw_big_scoreboard(game)
        team_font = ImageFont.load(big_font)
        # add period
        draw.text((5, 22), game.ordinal, font=team_font, fill=(255, 255, 255))

        # add FINAl
        if game.status == GameStatus.END:
            draw.text((37, 22), "FINAL",
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
