# Path: FindSteamIDs.py
# Description: iterate through all games with full controller support and get their steam IDs using the steam pypi API then create a desktop shortcut for each game

# import the necessary modules
import requests
import json
import os
import sys
import subprocess
import time
import winreg
from steam.steamid import SteamID
from steam.webapi import WebAPI
from steam.webauth import WebAuth

#steam api key
web_api = WebAPI(key="583A41F107BD02A0ABF67579E0EBD524")

#authenticate the user via cli
user = WebAuth("richmar2", "SoftEngine90")
session = user.cli_login()

#steam id of the user
steam_id = user.steam_id

#steam api call to get all games with full controller support
response = web_api.IPlayerService.GetOwnedGames(steamid=steam_id.as_64,
include_appinfo=1, include_played_free_games=0, appids_filter=None,
include_free_sub=0, format="json", language="en", include_extended_appinfo=1)

#iterate through the response and get the steam id of each game
for game in response["response"]["games"]:
    #dont overload the steam api
    time.sleep(1.6)
    #get the game app details
    app_details_response = session.get("https://store.steampowered.com/api/appdetails?appids=" + str(game["appid"]))
    #check if call was successful
    if app_details_response.status_code == requests.codes.ok:
        #convert the response to json
        app_details = app_details_response.json()

        #check if call was successful
        if app_details[str(game["appid"])]["success"] == True:
            #get the game name
            game_name = app_details[str(game["appid"])]["data"]["name"]
            #convert game name to a valid file name
            game_name = game_name.replace(":", "")
            game_name = game_name.replace("/", "")
            game_name = game_name.replace("\\", "")
            game_name = game_name.replace("*", "")
            game_name = game_name.replace("?", "")
            game_name = game_name.replace("\"", "")
            game_name = game_name.replace("<", "")
            game_name = game_name.replace(">", "")
            game_name = game_name.replace("|", "")

            game_controller_support = "none"
            #get the game steam id
            game_steam_id = game["appid"]
            #check if controller support is included in the app details
            if "controller_support" in app_details[str(game["appid"])]["data"]:
                #get the game controller support
                game_controller_support = app_details[str(game["appid"])]["data"]["controller_support"]
            print(game_name + ": Controller Support: " + str(game_controller_support))
            #if the game has full controller support
            if game_controller_support == "full":
                #create a file url shortcut for the game
                #create the directory if it doesn't exist
                if not os.path.exists(".\\ControllerGames"):
                    os.makedirs(".\\ControllerGames")
                #create the shortcut file if it doesn't exist
                if not os.path.exists(".\\ControllerGames\\" + game_name + ".url"):
                    file = open(".\\ControllerGames\\" + game_name + ".url", "w")
                    file.write("[InternetShortcut]\n")
                    file.write("URL=steam://rungameid/" + str(game_steam_id))
                    file.close()
        else:
            #print the error code and the description
            print("Error: " + str(app_details_response.status_code) + " " + app_details_response.reason)
    else:
        #print the error code abd the description
        print("Error: " + str(app_details.status_code) + " " + app_details.reason)