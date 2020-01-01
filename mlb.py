import requests
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from dateutil.parser import *
from common import *

MLB_QUERY = """{
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
      inning
    is_inning_top
    balls
    outs
    strikes
    }
}"""


class MLBGame(Game):
    def __init__(self, common, outs, balls, strikes, inning, is_inning_top):
        Game.__init__(self, common)
        self.outs = outs
        self.balls = balls
        self.strikes = strikes
        self.inning = inning
        self.is_inning_top = is_inning_top


class MLB(League):
    def __init__(self, settings):
        super().__init__(settings)
        self.renderer = MLBRenderer(64, 32)

    def reset(self):
        super().reset()
        self.games = []
        try:
            response = requests.get(
                url=AWS_URL + "mlb", json={'query': MLB_QUERY}).json()
            data = response['data']
            self.games = [MLBGame(game['common'], game['outs'], game['balls'], game['strikes'],
                                  game['inning'], game['is_inning_top']) for game in data['games']]
        except Exception as e:
            log.error("Error: " + str(e))
            error_title = "Disconnected"
            error_message = "Use the Scoreboard app to get reconnected"
            self.handle_error(error_title, error_message)
            return

    def get_image(self):
        if self.error:
            return self.renderer.draw_error(self.error_title, self.error_message)
        elif self.active_index == -1:
            return self.renderer.draw_info("No games :(")[0]
        else:
            return self.renderer.render(self.games[self.active_index])


class MLBRenderer(Renderer):
    def __init__(self, width, height):
        Renderer.__init__(self, width, height)

    def render(self, game):

        image, draw = self.draw_small_scoreboard(game)
        team_font = ImageFont.load(big_font)

        # draw the inning or game start time
        w, h = team_font.getsize(game.ordinal)
        draw.text((5, 19), game.ordinal, font=team_font, fill=(255, 255, 255))

        if game.status == GameStatus.ACTIVE:
            if game.is_inning_top:
                draw.point(self.draw_pixels(small_up_arrow_pixels, 6+w, 20))
            else:
                draw.point(self.draw_pixels(small_down_arrow_pixels, 6+w, 23))

            # draw balls/outs/strikes

            balls_strikes = "{}-{}".format(game.balls, game.strikes)
            small = ImageFont.load(small_font)
            w, h = small.getsize(balls_strikes)
            draw.text((61-w, 18), balls_strikes,
                      font=small, fill=(255, 255, 255))

            for i in range(0, 3):
                x = 61 - w + i * 4
                y = 19 + h + 3
                if game.outs > i:
                    draw.point(self.draw_pixels(square_3x3_filled, x, y))
                else:
                    draw.point(self.draw_pixels(square_3x3_open, x, y))

        return image
