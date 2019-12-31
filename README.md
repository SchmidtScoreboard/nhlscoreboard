# PiBoard

This is my implementation of a raspberry pi scoreboard.
It supports getting live scores for MLB and NHL games, as well as some other fun display features.

I've put a lot of work in to make it mom-and-dad friendly--hopefully people with little technical skill would have no trouble getting a PiBoard up and running, using the accompanying [app](https://github.com/schmidtwmark/ScoreboardApp)

Inspired by [MLB LED Scoreboard](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard)

## Getting Started

PiBoard works in two modes--testing mode, which runs on your computer, and live mode, which runs on a Raspberry Pi with a connected 64x32 LED matrix.

Testing mode uses tkinter, which may or may not be installed on your system by default

To skip setup, you can modify your `scoreboard_settings.json` file. Simply set `setup_state` to 10 and `active_screen` to 0 to skip the setup phases.

### Installing and Running

After cloning the repo, install the requirements using pip:

```
pip3 install -r requirements.txt
```

Then, run 
```
python3 owner.py
```


## Deployment

On a raspberry pi, you will need to install the matrix support library, included as a submodule: [Matrix Library](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master)

You must run as root on a raspberry pi in order to draw to the matrix.

## Design

PiBoard is designed to be easy to set up using the companion iOS/Android [app](https://github.com/schmidtwmark/ScoreboardApp). To support communication with the app, a "factory reset" PiBoard first starts up broadcasting a wifi hotspot.

Users are prompted to connect to the wifi network and then give their home wifi credentials. At that point, the PiBoard will restart into client mode, where it will try to connect to the internet using the provided credentials.

After that, users can modify settings, such as favorite teams, page cycle times, and timezone information. Users can also switch between modes. At time of writing, there are three modes--NHL, which displays live scores from NHL games, MLB, which displays live scores from MLB games, and Clock, which shows the current time.

To manage setup/settings change modes, the PiBoard runs a Flask server, listening for API calls to tell it to change settings, power off, or perform other actions.



## Authors

* **[Mark Schmidt](https://github.com/schmidtwmark)**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [MLB LED Scoreboard](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard) inspired the initial design and aesthetic for the sport modes
* For Jamie <3

