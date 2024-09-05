import os
import webbrowser
from keys import youtube_api_key
from googleapiclient.discovery import build
from voice import speak

# Replace with your own YouTube Data API key
YOUTUBE_API_KEY = youtube_api_key

# Function to search YouTube and get the first video URL and title
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
        video_title = response['items'][0]['snippet']['title']
        return video_url, video_title
    else:
        return None, None

# Function to open the video in the web browser
def play_media(url):
    webbrowser.open(url)

# Function to extract the main part of the title
def get_main_title(title):
    # Define your separator or rule here
    separators = ["¦", "|", "-", "•","."]
    for sep in separators:
        if sep in title:
            return title.split(sep)[0].strip()
    return title

# Test function
def main():
    try:
        # command = "maya play mahabharat new theme song"
        command = "maya play Are dwarpalo"
        # command = "maya play TERI BANKI ADAA NE OH SANWARE"
        print(f"Command received: {command}")
        process_command(command)
    except Exception as e:
        print(f"Error: {e}")

# Function to handle the test command
def process_command(command):
    if "play" in command:
        title = command.replace("play", "").strip()
        url, official_title = search_youtube(title)
        if url:
            # Extract the main part of the title
            main_title = get_main_title(official_title)
            # Let Maya speak the official title before playing the video
            speak(f"Sure, now playing {main_title}")
            print(f"Playing: {url}")
            play_media(url)
        else:
            print(f"No media found for '{title}'.")

if __name__ == "__main__":
    main()
