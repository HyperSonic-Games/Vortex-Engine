import os
import subprocess
import requests
import zipfile
import shutil
import PySimpleGUI as sg

def GetLatestReleaseInfo(repoUrl):
    """
    Fetches the latest release information from a GitHub repository.

    :param repoUrl: URL of the GitHub repository.
    :return: The URL of the latest release asset.
    """
    apiUrl = f"https://api.github.com/repos/{repoUrl}/releases/latest"
    response = requests.get(apiUrl)
    response.raise_for_status()
    releaseInfo = response.json()
    assetUrl = releaseInfo['assets'][0]['browser_download_url']
    return assetUrl

def DownloadFile(url, destPath, window):
    """
    Downloads a file from a URL to a specified path and updates the GUI.

    :param url: URL of the file to download.
    :param destPath: Path to save the downloaded file.
    :param window: PySimpleGUI window for updating progress.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    totalSize = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(destPath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            downloaded += len(chunk)
            progress = (downloaded / totalSize) * 100
            window.write_event_value('progress', progress)

def ExtractZip(zipPath, extractTo):
    """
    Extracts a zip file to a specified directory.

    :param zipPath: Path to the zip file.
    :param extractTo: Directory to extract files to.
    """
    with zipfile.ZipFile(zipPath, 'r') as zipRef:
        zipRef.extractall(extractTo)

def UpdateGUI(window, message):
    """
    Updates the GUI with a message.

    :param window: PySimpleGUI window for updating messages.
    :param message: Message to display.
    """
    window['-MESSAGE-'].update(message)

def Main():
    repoUrl = "yourusername/yourrepository"  # Change this to your GitHub repository URL
    latestReleaseUrl = GetLatestReleaseInfo(repoUrl)
    
    # Paths
    tempZipPath = "update.zip"
    extractToDir = "update"
    
    # Define GUI layout
    layout = [
        [sg.Text('Checking for updates...', size=(30, 1), key='-MESSAGE-')],
        [sg.ProgressBar(100, orientation='h', size=(30, 20), key='-PROGRESS-')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Update Checker', layout)

    try:
        UpdateGUI(window, 'Downloading update...')
        DownloadFile(latestReleaseUrl, tempZipPath, window)
        
        UpdateGUI(window, 'Extracting update...')
        if os.path.exists(extractToDir):
            shutil.rmtree(extractToDir)
        os.makedirs(extractToDir)
        ExtractZip(tempZipPath, extractToDir)
        
        # Replace old files with new ones
        UpdateGUI(window, 'Replacing old files...')
        for filename in os.listdir(extractToDir):
            filePath = os.path.join(extractToDir, filename)
            shutil.copy(filePath, ".")
        
        # Clean up
        os.remove(tempZipPath)
        shutil.rmtree(extractToDir)
        
        UpdateGUI(window, 'Starting the game...')
    except Exception as e:
        UpdateGUI(window, f'Error: {e}')
    
    # Close the GUI and run the game
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        subprocess.run(["python", "GAME_ENTRY.py"], check=True)

if __name__ == "__main__":
    Main()
