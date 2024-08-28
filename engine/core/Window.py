import pygame

class GameWindow:
    def __init__(self, Title: str, Width: int, Height: int, Fullscreen: bool, _DEBUG_: bool = False) -> None:
        self._DEBUG_ = _DEBUG_
        self.Title = Title
        self.Width = Width
        self.Height = Height
        self.Fullscreen = Fullscreen
        
        if self._DEBUG_:
            print("Initializing Pygame")
        
        pygame.init()
        
        # Determine the display flags based on fullscreen mode
        flags = pygame.FULLSCREEN if Fullscreen else pygame.RESIZABLE
        
        # Initialize display surface with additional flags
        self.Display: pygame.Surface = None
        
        try:
            self.Display = pygame.display.set_mode(
                (Width, Height), 
                flags | pygame.SCALED | pygame.ASYNCBLIT | pygame.OPENGLBLIT
            )
            pygame.display.set_caption(Title)
            pygame.display.flip()  # Ensure the display updates immediately
            
            # Attempt to enable VSync
            pygame.display.gl_set_swap_interval(1)
            if self._DEBUG_:
                print("VSync enabled")
        except pygame.error:
            if self._DEBUG_:
                print("VSync failed, falling back to default mode")
            # Fallback to initializing without VSync
            self.Display = pygame.display.set_mode((Width, Height), flags)
            pygame.display.set_caption(Title)
            pygame.display.flip()  # Ensure the display updates immediately

    def cleanup(self) -> None:
        if self._DEBUG_:
            print("Cleaning up Pygame")
        pygame.quit()