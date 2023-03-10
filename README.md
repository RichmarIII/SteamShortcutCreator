# Steam Shortcut Creator For Controller-Based Games

## Introduction

Steam Shortcut Creator (steamsc.py) is a Python-based software that streamlines the management of your Steam library by automatically creating shortcuts for games that offer full controller support. Designed for use with EmulationStation, this practical tool saves you time and effort by eliminating manual setup and offering a more organized and efficient gaming experience.

## Prerequisites

Before using Steam Shortcut Creator (steamsc.py), make sure you have the following installed:

* Python
* PyPi Steam API (`pip install -U "steam[client]"`)

## Obtaining Steam Web API Key

In order to use Steam Shortcut Creator (steamsc.py), you will need a Steam Web API Key. You can obtain this key by visiting the Steam Web API Key page at the following URL:

[https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)

## Configuration

Place the obtained Steam Web API Key in a text file named "steam_api_key.txt" in the same directory as the program.

## Usage

1. Open the terminal or command line interface.
2. Navigate to the location where you have stored the repository.
3. Run the Steam Shortcut Creator (steamsc.py) program using the following command: `python steamsc.py`
4. The program will scan your Steam library, identify games that offer full controller support, and create shortcuts for them in the designated location.

Note: The program must be run from the same directory as the "steam_api_key.txt" file.

# Installing The Generated Steam Game Shortcuts in EmulationStation

The following are instructions on how to install game shortcuts for Steam in EmulationStation.

`~` *is the installation folder of EmulationStation*

## Windows

1. Minimize the Steam application before launching games from EmulationStation, to prevent Steam from stealing focus.
2. Copy the ` .url` Steam game shortcuts into the  `~/ROMs/steam `directory. These files have the `.url` extension and can be launched directly from within EmulationStation.
3. The final result should look something like this:

   ```
   ~/ROMs/steam/Axiom Verge.url
   ~/ROMs/steam/Undertale.url
   ```

## Unix/Linux

1. Copy the `.desktop` Steam game shortcuts into the `~/ROMs/steam` directory. These files have the `.desktop` extension and can be launched directly from within EmulationStation
2. The final result should look something like this:

   ```
   ~/ROMs/steam/Axiom Verge.desktop
   ~/ROMs/steam/Undertale.desktop
   ```

## macOS

1. Make sure that the Steam application is minimized when launching games from EmulationStation, to prevent Steam from stealing focus.
2. Copy the `.app` Steam game shortcuts into the `~/ROMs/steam` directory. These files have the `.app` extension and can be launched directly from within EmulationStation
3. The final result should look something like this:

   ```
   ~/ROMs/steam/Axiom Verge.app
   ~/ROMs/steam/Undertale.app
   ```

## Author

Steam Shortcut Creator (steamsc.py) was authored by Richard G. Marcoux III.

As a seasoned developer, I am excited to explore the world of public
repositories and see where this journey takes me. I admit that I have
limited experience with Git and managing a public repository, but I am
eager to learn and improve. I kindly request understanding and patience
as I navigate this new territory, and I hope to create a positive and
welcoming environment for anyone who may be interested in contributing
to my repository.

## Support

If you encounter any issues or have questions, feel free to consult the documentation or reach out to the repository owner or community for support.
