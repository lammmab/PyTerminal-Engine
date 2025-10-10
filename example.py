from pyterminal import PyTerminal


class Game:
    def __init__(self):
        self.engine = PyTerminal(init_func=self.init, end_func=self.end)
        self.index = 0
        self.forward = True
        self.elapsed = 0

    def init(self, engine):
        self.name = engine.get_input("What is your name?: ", color="blue")

    def update(self, _delta):
        if self.forward:
            self.index += 1
            if self.index >= len(self.name):
                self.forward = False
                self.index -= 1
        else:
            self.index -= 1
            if self.index < 0:
                self.forward = True
                self.index += 1

        self.anim_name = self.name[:self.index + 1]

    def draw(self, delta):
        self.elapsed += delta

        self.engine.draw(self.anim_name, color="blue")
        if self.elapsed >= 1:
            self.engine.quit()

    def end(self):
        self.engine.draw("Example ended", color="yellow")
        self.engine.draw("Thanks for checking it out", color="green")

    def run_game(self):  # call once at game loop begin
        self.engine.run_loop(self.update, self.draw, fps=10)


game = Game()
game.run_game()
