![d1](https://github.com/KacperHaras/YT_Manager/assets/96292573/eb9f12db-e8e0-45d2-9e62-c5565b2a3519)# YT Manager

## Introduction

YT Manager is a comprehensive tool designed for downloading YouTube videos, audio, playlists, and for fetching important video information such as captions and video description links. It leverages the PyTube library to facilitate these downloads and information retrieval, offering a user-friendly interface and efficient processing.                                                                                                 | 
At the very bottom of the document I explain what the individual sections of the application look like.     |
                                                                                                           \|/                
                                                                                                            '
## Features

* **Video Download**: Download videos in various resolutions.
* **Audio Download**: Extract and download audio from YouTube videos.
* **Playlist Download**: Download all videos from a YouTube playlist.
* **Information Retrieval**: Get detailed information about videos, including captions and description links.
* **User Interface**: A simple and intuitive web interface for easy operation.

## App Structure

* `__init__.py`: Initializes the Flask application and sets up the necessary configurations for the app to run.

* `routes.py`: Contains all the route definitions for the app. It includes routes for downloading videos, audio, fetching video information, and handling playlist downloads.

* `utils.py`: A utility module that encapsulates the logic for additional functions interacting with the PyTube library.

* `index.html`: The main landing page of the app, providing users with the option to download videos and to retrieve video information.

* `download.html`: A page that guides users through the process of downloading videos or audio, including selection of format and quality.

* `get_info.html`: Displays detailed information about a video, including available video descriptions and captions - allows users to download this information.

* `style.css`: Contains the CSS styles for the app's frontend, ensuring a user-friendly and visually appealing interface.

## Using PyTube

This app utilizes the PyTube library for all interactions with YouTube, including downloading videos, playlists, and retrieving video information. PyTube is a lightweight, dependency-free Python library that provides an easy interface for accessing YouTube content.

## Setup and Installation

To set up and run your app, you will need to install Python, Flask, PyTube and any other dependencies which are required. Here are the general steps you would follow:

* Install **Python**: Make sure Python 3.x is installed.

* Install **Flask**: pip install Flask.

* Install **PyTube**: pip install pytube.

* Install **moviepy**: pip install moviepy.

* (Optional) Update **Werkzeug**: pip install --upgrade Werkzeug.


## Acknowledgments

I would like to express my gratitude to the PyTube documentation for their invaluable assistance during the development of this app. The guidance provided by their official documentation and API reference, found at https://pytube.io/en/latest/ and https://pytube.io/en/latest/api.html, was instrumental in leveraging the PyTube library effectively. For anyone interested in exploring the capabilities of the PyTube library further, these resources come highly recommended for their thoroughness and clarity.


## App Preview

The main page:
![h](https://github.com/KacperHaras/YT_Manager/assets/96292573/839a5936-78b7-48df-aa1a-228258a666f8)

The get_info page with example info:
![vi1](https://github.com/KacperHaras/YT_Manager/assets/96292573/09d72e64-d791-4cab-aa35-44cef1c1371e)

Preview on description:
![vi2](https://github.com/KacperHaras/YT_Manager/assets/96292573/d580c1ef-4c63-4651-be2b-4f285de02ce1)

Preview on captions:
![vi3](https://github.com/KacperHaras/YT_Manager/assets/96292573/e5bc8fd2-148a-4177-b01a-30399da24350)

The download page with example video:
![d1](https://github.com/KacperHaras/YT_Manager/assets/96292573/ee3fe484-1d2b-4f2e-ab37-5735eca35c31)

The download page with example playlist:
![d2](https://github.com/KacperHaras/YT_Manager/assets/96292573/1087e144-10c1-4c1f-be06-1fa84955b04b)


