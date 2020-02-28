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
    def __init__(self, timezone, common, outs, balls, strikes, inning, is_inning_top):
        Game.__init__(self, timezone, common)
        self.outs = int(outs)
        self.balls = int(balls)
        self.strikes = int(strikes)
        self.inning = int(inning)
        self.is_inning_top = bool(is_inning_top)


class MLB(League):
    def __init__(self, settings, api_key, timezone):
        super().__init__(settings, api_key, timezone)
        self.renderer = MLBRenderer(64, 32)

    def reset(self):
        super().reset()
        self.games = []
        data = self.get_games("mlb", MLB_QUERY)
        if data is not None:
            self.games = [MLBGame(self.timezone, game['common'], game['outs'], game['balls'], game['strikes'],
                                  game['inning'], game['is_inning_top']) for game in data['games']]

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
