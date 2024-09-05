import os
import webbrowser
from googleapiclient.discovery import build
from pytube import YouTube
from keys import youtube_api_key
# Replace with your own YouTube Data API key
YOUTUBE_API_KEY = youtube_api_key

# Function to search YouTube and get the first video URL
def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        order='relevance',
        maxResults=1
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None

# Function to open the video in the web browser
def play_media(url):
    webbrowser.open(url)

# Test function
def main():
    try:
        command = "maya play mahabarat new theme song"
        print(f"Command received: {command}")
        process_command(command)
    except Exception as e:
        print(f"Error: {e}")

# Function to handle the test command
def process_command(command):
    if "play" in command:
        title = command.replace("play", "").strip()
        url = search_youtube(title)
        if url:
            print(f"Playing: {url}")
            play_media(url)
        else:
            print(f"No media found for '{title}'.")

if __name__ == "__main__":
    main()
