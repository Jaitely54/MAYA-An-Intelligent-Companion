import os
import speech_recognition as sr

# Path to the Desktop (adjusted to the user's path)
desktop_path = r"C:\Users\jaite\OneDrive\Desktop"


def create_directory(directory_name):
    path = os.path.join(desktop_path, directory_name)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Directory '{directory_name}' created.")
        else:
            print(f"Directory '{directory_name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_directory(directory_name):
    path = os.path.join(desktop_path, directory_name)
    try:
        if os.path.exists(path):
            os.rmdir(path)
            print(f"Directory '{directory_name}' deleted.")
        else:
            print(f"Directory '{directory_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_command(command):
    command = command.lower()
    
    if "create a directory named" in command:
        directory_name = command.replace("create a directory named", "").strip()
        create_directory(directory_name)
    elif "delete the directory named" in command:
        directory_name = command.replace("delete the directory named", "").strip()
        delete_directory(directory_name)
    else:
        print("Command not recognized. Please say 'create a directory named [directory_name]' or 'delete the directory named [directory_name]'.")

if __name__ == "__main__":
        # command ="create a directory named my_folder"
        command ="delete the directory named bhaikipardai"
        if command:
            process_command(command)
