from abc import ABCMeta, abstractmethod

class Player(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, player_id=""):
        pass

    @abstractmethod
    def action(self, game):
        """
        アクションをする
        """
        pass