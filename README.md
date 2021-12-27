# Discord-Music-Bot
Plays audio from youtube using yt-dlp (fork of youtube-dl)

## Dependencies:
- discord
- ffmpeg
- yt_dlp

## Usage:
Update properties.txt to include your API key and run main.py. 
Sidenote: properties.txt values must not contain any whitespace.

Bot commands:
  - help   Shows help message
  - join   Join a voice channel
  - leave  Leave a voice channel
  - pause  Pause audio
  - play [url/ID] [codec] [quality] Play a song from YouTube Link/ID. Default codec and quality are mp3 and 192.
  - resume Resume paused audio
  - stop   Stop currently playing audio
  - test   Test command
