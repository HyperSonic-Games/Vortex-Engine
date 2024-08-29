import os
import subprocess

def CreateExecutable(entryFile, assetsDir, engineDir, buildDir):
    """
    Packages the specified entry file and assets directory into a single executable using PyInstaller.

    :param entryFile: The main Python script to be packaged.
    :param assetsDir: The directory containing assets to include in the package.
    :param engineDir: The directory containing engine source code to include in the package.
    :param buildDir: The directory where the build output will be placed.
    """
    if not os.path.exists(buildDir):
        os.makedirs(buildDir)

    command = [
        'pyinstaller',
        '--onefile',            # Create a one-file bundled executable.
        '--add-data', f'{assetsDir}{os.pathsep}{assetsDir}',  # Include the ASSETS directory.
        '--add-data', f'{engineDir}{os.pathsep}{engineDir}',  # Include the engine directory.
        '--distpath', os.path.join(buildDir, 'dist'),          # Set the output directory for the executable.
        '--workpath', os.path.join(buildDir, 'build'),         # Set the build directory for PyInstaller temporary files.
        '--specpath', os.path.join(buildDir, 'spec'),          # Set the directory for the spec file.
        'tools/UpdateChecker.py'  # The entry file for the update checker.
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully created executable for UpdateChecker.py.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the executable: {e}")

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    ENTRY_FILE = os.path.join(BASE_DIR, 'tools', 'UpdateChecker.py')
    ASSETS_DIR = os.path.join(BASE_DIR, 'ASSETS')
    ENGINE_DIR = os.path.join(BASE_DIR, 'engine')
    BUILD_DIR = os.path.join(BASE_DIR, 'build')

    if not os.path.isfile(ENTRY_FILE):
        print(f"Error: {ENTRY_FILE} does not exist.")
    elif not os.path.isdir(ASSETS_DIR):
        print(f"Error: {ASSETS_DIR} directory does not exist.")
    elif not os.path.isdir(ENGINE_DIR):
        print(f"Error: {ENGINE_DIR} directory does not exist.")
    else:
        CreateExecutable(ENTRY_FILE, ASSETS_DIR, ENGINE_DIR, BUILD_DIR)
