import pygame

class BaseObject(pygame.sprite.DirtySprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.DirtySprite.__init__(self)
        #super().__init__(self)
        self.x = x
        self.y = y
        self.width = w
        self.height = h

class Wall(BaseObject):
    def __init__(self, x, y, w, h, solid=True):
        BaseObject.__init__(self, x, y, w, h)
        self.solid = solid
sprGroup = pygame.sprite.Group()
bricks = Wall(0, 1, 2, 3)
sprGroup.add(bricks)
print(sprGroup)
