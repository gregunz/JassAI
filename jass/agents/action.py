from jass.logic.card import Card, Suit


class PlayCardAction:
    def __init__(self, card_to_play: Card):
        self.card_to_play = card_to_play


class ChooseTrumpAction:
    def __init__(self, suit: Suit = None, chibre: bool = False):
        assert (suit is None and chibre) or \
               (suit is not None and not chibre)
        self.suit = suit
        self.chibre: bool = chibre
