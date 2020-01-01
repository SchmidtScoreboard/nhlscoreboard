from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from enum import Enum
from files import *
import logging
import json
import time
import config
import socket
import version
import signal
import pytz
from dateutil.parser import *
log = logging.getLogger(__name__)
Color = namedtuple('Color', 'red green blue')

ACTIVE_SCREEN_KEY = "active_screen"
SETUP_STATE_KEY = "setup_state"
SCREENS_KEY = "screens"
MATRIX_KEY = "matrix"
SCREEN_ON_KEY = "screen_on"
VERSION_KEY = "version"

AWS_URL = 'https://opbhrfuhq5.execute-api.us-east-2.amazonaws.com/Beta/'
# AWS_URL = 'http://127.0.0.1:1337/'


small_down_arrow_pixels = [(0, 0), (1, 0), (2, 0),
                           (3, 0), (4, 0), (1, -1), (2, -1), (3, -1), (2, -2)]
small_up_arrow_pixels = [(2, 0), (1, -1), (2, -1),
                         (3, -1), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2)]
square_3x3_open = [(0, 0), (0, 1), (0, 2), (1, 0),
                   (1, 2), (2, 0), (2, 1), (2, 2)]
square_3x3_filled = square_3x3_open + [(1, 1)]
wifi = [(0, -6), (1, -5), (2, -4), (2, -7), (3, -4), (3, -6), (4, -3), (4, -6), (4, -8), (5, -3), (5, -5), (5, -7), (6, -3), (6, -5),
        (6, -7), (6, -9), (7, -3), (7, -5), (7, -7), (8, -3), (8, -6), (8, -8), (9, -4), (9, -6), (10, -4), (10, -7), (11, -5), (12, -6)]


def restart_scoreboard():
    if config.testing:
        log.info("About to reboot, test mode")
        os.kill(os.getppid(), signal.SIGINT)
    else:
        log.info("About to reboot, production mode")
        os.system('sudo shutdown -r now')


def get_settings():
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except:
        with open(settings_template_path) as f:
            settings = json.load(f)
            write_settings(settings)
    return settings


def write_settings(new_settings):
    with open(settings_path, "w+") as f:
        new_settings["version"] = version.version
        json.dump(new_settings, f)


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # attempt to connect, and then get hostname
        return s.getsockname()[0]
    except:
        return ""


class ActiveScreen(Enum):
    NHL = 0
    MLB = 1
    CLOCK = 50
    REBOOT = 99
    REFRESH = 100
    HOTSPOT = 101
    WIFI_DETAILS = 102
    SYNC = 103
    ERROR = 999


def hexToRGB(hex):
    red = hex[0:2]
    green = hex[2:4]
    blue = hex[4:6]
    return Color(int(red, 16), int(green, 16), int(blue, 16))


class Team:
    def __init__(self, common):
        self.id = common['id']
        self.name = common['name']
        self.display_name = common['display_name'].upper()
        self.city = common['city']
        self.abbreviation = common['abbreviation']
        self.primary_color = hexToRGB(common['primary_color'])
        self.secondary_color = hexToRGB(common['secondary_color'])

    def __repr__(self):
        return "{!r}({!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__,
                                                                 self.id, self.name,
                                                                 self.city, self.abbreviation,
                                                                 self.primary_color, self.secondary_color)


class GameStatus(Enum):
    INVALID = 0
    PREGAME = 1
    ACTIVE = 2
    INTERMISSION = 3
    END = 4

    @staticmethod
    def stringToValue(string):
        if string == "PREGAME":
            return GameStatus.PREGAME
        elif string == "ACTIVE":
            return GameStatus.ACTIVE
        elif string == "INTERMISSION":
            return GameStatus.INTERMISSION
        elif string == "END":
            return GameStatus.END
        else:
            return GameStatus.INVALID


class Game:
    def __init__(self, common):
        self.id = common['id']
        self.away = Team(common['away_team'])
        self.home = Team(common['home_team'])
        self.away_score = common['away_score']
        self.home_score = common['home_score']
        self.status = common['status']
        self.start_time = common['start_time']
        self.ordinal = common['ordinal']
        time = parse(self.start_time).astimezone(
            pytz.timezone("America/Chicago"))
        self.start_hour = time.hour % 12
        if self.start_hour == 0:
            self.start_hour = 12
        self.start_afternoon = "PM" if time.hour >= 12 else "AM"
        self.start_minute = time.minute


class Screen:
    def __init__(self):
        self.error = False
        self.error_title = ""
        self.error_message = ""
        pass

    def reset(self):
        pass

    def get_image(self):
        pass

    def refresh(self):
        pass

    def get_sleep_time(self):
        return 10

    def get_refresh_time(self):
        return 60


class League(Screen):
    def __init__(self, settings):
        super().__init__()
        self.last_full_refresh_time = 0
        self.active_index = 0
        self.last_reset = 0
        self.rotation_time = settings.get("rotation_time", 10)
        self.focus_teams = settings.get("focus_teams", [])
        self.games = []

    def reset(self):
        pass

    def refresh(self):
        if (time.time() - self.last_reset) > self.get_refresh_time():
            # if it's been more than X seconds since the last refresh, refresh all games
            log.info("Performing refresh")
            self.last_reset = time.time()
            self.reset()

        # Regardless, move the active game up one, unless a favorite team is playing
        if len(self.games) == 0:
            self.active_index = -1
        elif self.favorite_teams_playing() is not None:
            self.active_index = self.favorite_teams_playing()
        else:
            self.active_index = (self.active_index + 1) % len(self.games)

    def get_sleep_time(self):
        if self.error:
            return 0.05
        else:
            return self.rotation_time

    def get_image(self):
        pass

    def get_refresh_time(self):
        if len(self.games) == 0:
            return 120
        else:
            return 60

    def team_playing(self, team_id):
        for game in self.games:
            if game.home.id == team_id or game.away.id == team_id:
                if game.status == GameStatus.ACTIVE or game.status == GameStatus.INTERMISSION:
                    return self.games.index(game)
        return None

    def favorite_teams_playing(self):
        for team_id in self.focus_teams:
            game = self.team_playing(team_id)
            if game is not None:
                return game
        return None

    def handle_error(self, error_title, error_message):
        self.error = True
        self.last_full_refresh_time = 0
        self.error_title = error_title
        self.error_message = error_message


class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.text_start = self.width

    def draw_big_scoreboard(self, game):
        print("Drawing big scoreboard, game " + game.id)
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)  # let's draw on this image
        team_font = ImageFont.load(big_font)

        # add teams
        draw.rectangle(((0, 0), (64, 9)), fill=game.away.primary_color)
        draw.rectangle(((0, 0), (2, 9)), fill=game.away.secondary_color)
        draw.text((5, 1), game.away.display_name,
                  font=team_font, fill=game.away.secondary_color)
        draw.text((57, 1), str(game.away_score), font=team_font,
                  fill=game.away.secondary_color)

        draw.rectangle(((0, 10), (64, 19)), fill=game.home.primary_color)
        draw.rectangle(((0, 10), (2, 19)), fill=game.home.secondary_color)
        draw.text((5, 11), game.home.display_name,
                  font=team_font, fill=game.home.secondary_color)
        draw.text((57, 11), str(game.home_score),
                  font=team_font, fill=game.home.secondary_color)

        return (image, draw)

    def draw_small_scoreboard(self, game, image=None):
        if image is None:
            image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)  # let's draw on this image
        team_font = ImageFont.load(small_font)

        # add teams
        draw.rectangle(((0, 0), (64, 6)), fill=game.away.primary_color)
        draw.rectangle(((0, 0), (2, 6)), fill=game.away.secondary_color)
        draw.text((5, 1), game.away.display_name,
                  font=team_font, fill=game.away.secondary_color)
        away_score_message = str(game.away_score)
        w, _ = team_font.getsize(away_score_message)
        draw.text((61 - w, 1), str(game.away_score),
                  font=team_font, fill=game.away.secondary_color)

        draw.rectangle(((0, 7), (64, 13)), fill=game.home.primary_color)
        draw.rectangle(((0, 7), (2, 13)), fill=game.home.secondary_color)
        draw.text((5, 8), game.home.display_name,
                  font=team_font, fill=game.home.secondary_color)
        home_score_message = str(game.home_score)
        w, _ = team_font.getsize(home_score_message)
        draw.text((61 - w, 8), str(game.home_score),
                  font=team_font, fill=game.home.secondary_color)

        return (image, draw)

    def draw_error(self, title, scrollingText=None):
        image, draw = self.draw_border(color=(255, 0, 0))
        height = None
        if scrollingText is not None:
            height = self.height + 6
            image, draw, self.text_start = self.get_scrolling_text(
                self.text_start, image, scrollingText, (255, 0, 0), (0, 0, 0))
        image, draw = self.draw_text(
            title, centered=True, image=image, height=height, color=(255, 0, 0))
        return image

    def draw_text(self, text, centered=False, x=None, y=None, width=None, height=None, color=None, image=None, font_filename=small_font):
        if image is None:
            image = Image.new("RGB", (self.width, self.height))
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if x is None:
            x = width/2
        if y is None:
            y = height/2
        if color is None:
            color = (255, 255, 255)
        font = ImageFont.load(font_filename)
        draw = ImageDraw.Draw(image)

        w, h = font.getsize(text)
        if centered:
            x = x - w/2
            y = y - h/2
        draw.text((x, y), text, font=font, fill=color)

        return (image, draw)

    def draw_border(self, color=None, image=None):
        if image is None:
            image = Image.new("RGB", (self.width, self.height))
        if color is None:
            color = (255, 255, 255)
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (self.width-1, self.height-1)],
                       outline=color, fill=(0, 0, 0))

        return (image, draw)

    def draw_info(self, text):
        image, draw = self.draw_border()
        image, draw = self.draw_text(text, centered=True, image=image)
        return (image, draw)

    def draw_icon(self, icon, image=None):
        pass

    def draw_pixels(self, pixels, x, y):
        return [(x+xi, y-yi) for xi, yi in pixels]

    def get_scrolling_text(self, text_start, image=None, message="Message", background_color=(255, 255, 255), text_color=(0, 0, 0)):
        if image is None:
            image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)  # let's draw on this image
        draw.rectangle(((0, 0), (64, 6)), fill=background_color)
        font = ImageFont.load(small_font)
        w, _ = font.getsize(message)
        text_end = text_start + w
        secondary_start = text_end + 16

        self.draw_text(message, x=text_start, y=1,
                       color=text_color, image=image)
        self.draw_text(message, x=secondary_start, y=1,
                       color=text_color, image=image)

        text_start -= 1
        if text_end <= 0:
            text_start = secondary_start - 1
        return image, draw, text_start
