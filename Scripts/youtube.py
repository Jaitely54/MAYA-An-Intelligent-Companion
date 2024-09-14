import os
import webbrowser
import logging
from googleapiclient.discovery import build
from keys import youtube_api_key
from voice import speak

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your own YouTube Data API key
YOUTUBE_API_KEY = youtube_api_key

def search_youtube(query):
    """
    Searches YouTube and returns the URL and title of the first video.
    """
    try:
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
            logging.warning(f"No results found for query: {query}")
            return None, None
    except Exception as e:
        logging.error(f"Error fetching YouTube video: {e}")
        return None, None

def play_media(url):
    """
    Opens the provided URL in the default web browser.
    """
    webbrowser.open(url)

def get_main_title(title):
    """
    Extracts the main part of the title by splitting on common separators.
    """
    separators = ["¦", "|", "-", "•", "."]
    for sep in separators:
        if sep in title:
            return title.split(sep)[0].strip()
    return title

def process_command(command):
    """
    Processes a command to play a YouTube video.
    """
    if "play" in command:
        title = command.replace("play", "").strip()
        url, official_title = search_youtube(title)
        if url:
            main_title = get_main_title(official_title)
            speak(f"Sure, now playing {main_title}")
            logging.info(f"Playing: {url}")
            play_media(url)
        else:
            speak(f"No media found for '{title}'.")
            logging.info(f"No media found for '{title}'.")

def main():
    try:
        command = "maya play B Praak: Dil Tod Ke Official Song"
        logging.info(f"Command received: {command}")
        process_command(command)
    except Exception as e:
        logging.error(f"Error: {e}")
        speak("An error occurred while processing your request.")

if __name__ == "__main__":
    main()
