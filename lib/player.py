from entity import Entity

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tick(self):
        super().tick()

    def think(self):
        pass
