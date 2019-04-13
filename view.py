from backend import Game, NHL
from PIL import Image, ImageDraw, ImageFont

class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height


    def render(self, game):
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image) #  let's draw on this image
        team_font = ImageFont.load("/home/pi/nhlscoreboard/rpi-rgb-led-matrix/fonts/5x8.pil")

        #add teams
        draw.rectangle(((0,0), (64,9)), fill=game.away.team_color)
        draw.rectangle(((0,0), (2, 9)), fill=game.away.team_secondary_color)
        draw.text((5, 1), game.away.team_name if len(game.away.team_name) < 10 else game.away.team_city, font=team_font, fill=game.away.team_secondary_color)
        draw.text((57, 1), str(game.away_score), font=team_font, fill=game.away.team_secondary_color)

        draw.rectangle(((0,10), (64,19)), fill=game.home.team_color)
        draw.rectangle(((0,10), (2, 19)), fill=game.home.team_secondary_color)
        draw.text((5, 11), game.home.team_name if len(game.home.team_name) < 10 else game.home.team_city, font=team_font ,fill=game.home.team_secondary_color)
        draw.text((57, 11), str(game.home_score), font=team_font, fill=game.home.team_secondary_color)

        #add period
        draw.text((5, 21), game.ordinal, font=team_font, fill=(255, 255, 255))

        #add FINAl
        if game.current_period_time == "Final":
            draw.text((37, 21), game.current_period_time, font=team_font, fill=(255, 255, 0)) 

        #add powerplay
        message = ""
        powerplay = False
        if game.away_powerplay:
            powerplay = True
            message = game.away.abbreviation
        if game.home_powerplay:
            powerplay = True
            message = game.home.abbreviation
        if game.away_powerplay and game.home_powerplay :
            powerplay = True
            message = "{}-{}".format(game.away_skaters, game.home_skaters)
        if powerplay:
            w, h = team_font.getsize(message) 
            rightPoint = 63 - w - 3
            draw.rectangle(((rightPoint,21),(rightPoint+w+2,30)), fill=(255,255,0))
            draw.text((rightPoint+2,22), message, font=team_font, fill=(0,0,0))

        return image



    def render_no_games(self):
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        team_font = ImageFont.load("/home/pi/nhlscoreboard/rpi-rgb-led-matrix/fonts/5x8.pil")
        message = "No games today :("
        w, h = team_font.getsize(message)
        draw.text(((64-w)/2, ((32-h)/2)), message, font=team_font, fill=(255, 255, 255))
        return image
