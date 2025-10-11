"""Example game using PyTerminal."""
from pyterminal import PyTerminal,time


class Game:
    """A simple demo game that animates a name in the terminal."""
    def __init__(self):
        """Initialize the game variables."""
        self.index = 0
        self.forward = True
        self.display_text = ""
        self.name = None
        self.elapsed = 0
        
        self.engine = PyTerminal(init_func=self.init, end_func=self.end)

    def init(self, engine):
        name = engine.get_input("/cRANDWhat is your name? ")
        self.name = name or "Person"

    def update(self, _delta):
        if self.forward:
            if self.index < len(self.name):
                self.index += 1
                self.display_text = self.name[:self.index]
            else:
                self.forward = False
        else:
            if self.index > 0:
                self.index -= 1
                self.display_text = self.name[:self.index]
            else:
                self.forward = True

    def draw(self, delta):
        self.elapsed += delta
        self.engine.draw(f"/cRANDHello, {self.display_text}!")
        
        if self.elapsed >= 10:
            self.engine.quit()

    def end(self):
        """End of game message."""
        self.engine.draw("/cYELLOWExample ended")
        self.engine.draw("/cGREENThanks for checking it out")

    def run_game(self):  # call once at game loop begin
        """Start the game loop."""
        self.engine.run_loop(self.update, self.draw, fps=5)


game = Game()
game.run_game()
