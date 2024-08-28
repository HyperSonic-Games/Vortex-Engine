import os
import sys
import pygame


class AssetLoader:
    def __init__(self):
        self.AssetsDir = self.GetAssetsDir()

    def GetAssetsDir(self):
        """
        Determines the directory where assets are stored.
        In a PyInstaller bundle, this is a temporary folder.
        """
        # When running in a PyInstaller bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'ASSETS')
        # When running from source
        else:
            return os.path.join(os.path.dirname(__file__), 'ASSETS')

    def LoadImage(self, filename):
        """
        Loads an image from the assets directory.
        :param filename: Name of the image file to load.
        :return: Pygame Surface object with the loaded image.
        """
        path = os.path.join(self.AssetsDir, filename)
        try:
            image = pygame.image.load(path)
            return image
        except pygame.error as e:
            print(f"Error loading image: {filename} - {e}")
            return None

    def LoadSound(self, filename):
        """
        Loads a sound file from the assets directory.
        :param filename: Name of the sound file to load.
        :return: Pygame Sound object.
        """
        path = os.path.join(self.AssetsDir, filename)
        try:
            sound = pygame.mixer.Sound(path)
            return sound
        except pygame.error as e:
            print(f"Error loading sound: {filename} - {e}")
            return None

    def LoadFont(self, filename, size):
        """
        Loads a font from the assets directory.
        :param filename: Name of the font file to load.
        :param size: Size of the font.
        :return: Pygame Font object.
        """
        path = os.path.join(self.AssetsDir, filename)
        try:
            font = pygame.font.Font(path, size)
            return font
        except pygame.error as e:
            print(f"Error loading font: {filename} - {e}")
            return None
