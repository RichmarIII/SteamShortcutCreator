#Copyright (C) 2023 Richard G. Marcoux III
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#This software is provided in the hopes that it will be useful, but without any warranty. It is provided "as is" and the author disclaims all warranties with regard to this software including all implied warranties of merchantability and fitness. In no event shall the author be liable for any special, direct, indirect, or consequential damages or any damages whatsoever resulting from loss of use, data or profits, whether in an action of contract, negligence or other tortious action, arising out of or in connection with the use or performance of this software.

# Path: steamsc.py
# Description: Finds all games with full controller support on the user's steam account and creates a desktop shortcut for each game
# Usage: python steamsc.py (must be run from the same directory as steam_api_key.txt)
# Author: Richard G. Marcoux III
# Libraries: steam (pip install -U "steam[client]")
# Date: 01/30/2023
# Version: 1.0.0
# License: MIT License (https://opensource.org/licenses/MIT)

# import the necessary modules
import getpass
import platform
import requests
import os
import time
from steam.webapi import WebAPI
from steam.webauth import WebAuth

def make_safe_name(game_name):
    """
    Summary:
        Converts a game name to a valid file name

    Args:
        `game_name`: The game name to convert to a valid file name 

    Example:
        make_safe_name("Arma 3: Apex")

    Returns:
        `str`: The game name converted to a valid file name (Arma 3: Apex -> Arma 3 Apex) 
    """

    game_name = game_name.replace(":", "")
    game_name = game_name.replace("/", "")
    game_name = game_name.replace("\\", "")
    game_name = game_name.replace("*", "")
    game_name = game_name.replace("?", "")
    game_name = game_name.replace("\"", "")
    game_name = game_name.replace("<", "")
    game_name = game_name.replace(">", "")
    game_name = game_name.replace("|", "")
    return game_name

def create_game_shortcut(game_name : str, game_steam_id : int):
    """
    Summary:
        Create a shortcut for a game

    Args:
        `game_name`: The name of the game to create a shortcut for
        `game_steam_id`: The steam id of the game to create a shortcut for

    Example:
        create_game_shortcut("Arma 3", 107410)

    Returns:
        `None`

    Notes:
        The shortcut will be created in the directory "./ControllerGames" and will be named "`game_name.url`" for Windows and "`game_name.desktop`" for Linux and "`game_name.app`" for Mac
    """
    
    #default the directory
    directory = "./ControllerGames"

    #create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    #create the shortcut file if it doesn't exist
    operating_system = platform.system()
    if operating_system == "Windows":
        shortcut_path = os.path.join(directory, f"{game_name}.url")
        if not os.path.exists(shortcut_path):
            with open(shortcut_path, "w") as shortcut:
                shortcut.write(f"[InternetShortcut]\nURL=steam://rungameid/{game_steam_id}")
    elif operating_system == "Linux":
        shortcut_path = os.path.join(directory, f"{game_name}.desktop")
        if not os.path.exists(shortcut_path):
            with open(shortcut_path, "w") as shortcut:
                shortcut.write(f"[Desktop Entry]\nType=Application\nName=Steam Game {game_name}\nExec=steam steam://rungameid/{game_steam_id}\nIcon=steam")
    elif operating_system == "Darwin":
        shortcut_path = os.path.join(directory, f"{game_name}.app")
        if not os.path.exists(shortcut_path):
            with open(shortcut_path, "w") as shortcut:
                shortcut.write(f"#!/bin/bash\nopen steam://rungameid/{game_steam_id}")
        os.chmod(shortcut_path, 0o755)

def get_controller_support_for_game(game, app_details) -> str:
    """
    Summary:
        Get the controller support status of a game

    Args:
        `game`: The game to get the controller support status for
        `app_details`: The app details of the game (eg: https://store.steampowered.com/api/appdetails?appids=440&filters=categories,basic)

    Example:
        get_controller_support_for_game(game, app_details)

    Returns:
        `str`: The controller support status of the game (none, partial, full)
    """

    #get the categories of the game
    game_categories = app_details[str(game["appid"])]["data"]["categories"]

    #default controller support to none
    game_controller_support = "none"
    
    #check for controller support
    for category in game_categories:
        if category["id"] == 18: #partial controller support
            game_controller_support = "partial"
            break
        if category["id"] == 28: #full controller support
            game_controller_support = "full"
            break

    #return the controller support status
    return game_controller_support

def process_game(game, session):
    """
    Summary:
        Process a game (check for controller support and create a shortcut if it has full controller support)
    
    Args:
        `game`: The game to process
        `session`: The session to use for the request

    Example:
        process_game(game, `WebAuth`("username", "password").cli_login())

    Returns:
        `None`
    """
    
    #don't overload the steam api (seems to work at 1.6 seconds per call) (https://steamcommunity.com/dev/apiterms) 
    time.sleep(1.6)
    
    #get the app details of the game (eg: https://store.steampowered.com/api/appdetails?appids=440&filters=categories,basic)
    app_details_response = session.get("https://store.steampowered.com/api/appdetails?appids=" + str(game["appid"]) + "&filters=categories,basic")
    
    #check if call was successful
    if app_details_response.status_code == requests.codes.ok:
        
        #convert the response to json
        app_details = app_details_response.json()
        
        #default game name to unknown game
        game_name = "Unknown Game"
        
        #check if the game name exists
        if "name" in game:
            game_name = game["name"]
        
        #convert game name to a valid file name
        game_name = make_safe_name(game_name)

        #check if game details were found
        if app_details[str(game["appid"])]["success"] == True:
            
            #get the categories of the game if they exist and check for controller support (18 = partial controller support, 28 = full controller support)
            if "categories" in app_details[str(game["appid"])]["data"]:
                
                #get the controller support status of the game
                game_controller_support = get_controller_support_for_game(game, app_details)

                #print the game name and controller support status to the console (for debugging)
                print(game_name + ": Controller Support: " + str(game_controller_support) + "\n" )

                #check if the game has full controller support and create a shortcut for it if it does (partial controller support is not supported)
                if game_controller_support == "full":
                    create_game_shortcut(game_name, game["appid"])
        else:
            #print the error to the console (for debugging) if the game details were not found (some games don't return details)
            print("Error: app details not found for: " + game_name)
    else:
        #print the error to the console (for debugging) if the call was not successful (some games don't return details)
        print("Error: " + str(app_details.status_code) + " " + app_details.reason)

def main():
    """
    Summary:
        Main function

    Example:
        main()

    Returns:
        `None`
    """
    #load steam api key from file
    with open("steam_api_key.txt", "r") as file:
        steam_api_key = file.read()

    #create the steam web api object
    web_api = WebAPI(key=steam_api_key)

    #authenticate the user via cli
    
    #ask for username and password
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = WebAuth(username=username, password=password)
    session = user.cli_login()

    #steam id of the user
    steam_id = user.steam_id

    #steam api call to get all games owned by the user
    response = web_api.IPlayerService.GetOwnedGames(steamid=steam_id.as_64,
    include_appinfo=1, include_played_free_games=0, appids_filter=None,
    include_free_sub=0, format="json", language="en", include_extended_appinfo=1)

    #iterate through all games owned by the user and check for controller support (partial controller support is not supported)
    for game in response["response"]["games"]:
        process_game(game, session)

        #print progress to the console
        print("Progress: " + str(response["response"]["games"].index(game) + 1) + "/" + str(len(response["response"]["games"])))

        #estimate time remaining (seconds)
        seconds_remaining = (len(response["response"]["games"]) - response["response"]["games"].index(game)) * 1.6

        #convert seconds to hours, minutes, and seconds
        hours = seconds_remaining // 3600
        seconds_remaining %= 3600
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60

        #print estimated time remaining to the console in format (xxh:xxm:xxs)
        print("Estimated Time Remaining: " + str(int(hours)) + "h:" + str(int(minutes)) + "m:" + str(int(seconds)) + "s\n")

#run the main function of the program
main()