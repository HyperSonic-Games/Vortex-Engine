import os
import subprocess

def create_executable(entry_file, assets_dir, engine_dir, build_dir):
    """
    Packages the specified entry file and assets directory into a single executable using PyInstaller.

    :param entry_file: The main Python script to be packaged.
    :param assets_dir: The directory containing assets to include in the package.
    :param engine_dir: The directory containing engine source code to include in the package.
    :param build_dir: The directory where the build output will be placed.
    """
    # Ensure the build directory exists
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    # Construct the command for PyInstaller
    command = [
        'pyinstaller', 
        '--onefile',            # Create a one-file bundled executable.
        '--add-data', f'{assets_dir}{os.pathsep}{assets_dir}',  # Include the ASSETS directory.
        '--add-data', f'{engine_dir}{os.pathsep}{engine_dir}',  # Include the engine directory.
        '--distpath', os.path.join(build_dir, 'dist'),          # Set the output directory for the executable.
        '--workpath', os.path.join(build_dir, 'build'),         # Set the build directory for PyInstaller temporary files.
        '--specpath', os.path.join(build_dir, 'spec'),          # Set the directory for the spec file.
        entry_file              # The main entry file for the game.
    ]

    try:
        # Run the PyInstaller command
        subprocess.run(command, check=True)
        print(f"Successfully created executable for {entry_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the executable: {e}")

if __name__ == "__main__":
    # Define the base directory
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Define the entry file, assets directory, engine directory, and build directory
    ENTRY_FILE = os.path.join(BASE_DIR, 'GAME_ENTRY.py')
    ASSETS_DIR = os.path.join(BASE_DIR, 'ASSETS')
    ENGINE_DIR = os.path.join(BASE_DIR, 'engine')
    BUILD_DIR = os.path.join(BASE_DIR, 'build')

    # Check if the entry file, assets directory, and engine directory exist
    if not os.path.isfile(ENTRY_FILE):
        print(f"Error: {ENTRY_FILE} does not exist.")
    elif not os.path.isdir(ASSETS_DIR):
        print(f"Error: {ASSETS_DIR} directory does not exist.")
    elif not os.path.isdir(ENGINE_DIR):
        print(f"Error: {ENGINE_DIR} directory does not exist.")
    else:
        # Create the executable in the specified build directory
        create_executable(ENTRY_FILE, ASSETS_DIR, ENGINE_DIR, BUILD_DIR)
