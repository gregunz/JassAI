from typing import Sequence, List, Dict

from jass.logic.card import Card, Suit, Rank
from jass.logic.illegal_move import IllegalMoveError


class Hand:
    def __init__(self, cards: Sequence[Card]):
        self.__cards = set(cards)
        if len(cards) != 9:
            raise ValueError('A hand must contains exactly 9 unique cards at the start')
        self.__playable_cards_cached: Dict[int, List[Card]] = dict()

    @property
    def cards(self) -> List[Card]:
        return list(self.__cards)

    def play(self, card: Card, cards_played: List[Card], trump: Suit) -> None:
        if card not in self.playable_cards(cards_played=cards_played, trump=trump):
            raise IllegalMoveError(f'Cannot play this card ({card})')
        self.__cards.remove(card)
        # return self

    def has(self, card: Card) -> bool:
        return card in self.__cards

    def playable_cards(self, cards_played: List[Card], trump: Suit):
        return self.__cached_playable_cards(cards_played=cards_played, trump=trump)

    def __cached_playable_cards(self, cards_played: List[Card], trump: Suit):
        key = len(self.__cards)
        if key not in self.__playable_cards_cached:
            # using dict but not keeping previous cached playable cards
            self.__playable_cards_cached = {key: self.__find_playable_cards(cards_played=cards_played, trump=trump)}
        return self.__playable_cards_cached[key]

    def __find_playable_cards(self, cards_played: List[Card], trump: Suit) -> List[Card]:
        # we are the first to play -> all cards are playable
        if len(cards_played) == 0:
            return self.cards
        else:
            served: Suit = cards_played[0].suit

            # first played a trump card -> must play a trump card (except if none available)
            if served is trump:
                if self.__can_serve(trump, including_jack=False):
                    # must serve a trump card
                    return [card for card in self.cards if card.suit is trump]
                else:
                    # no trump or only the trump jack -> all cards are playable
                    return self.cards
            else:
                # checking if any trump cards have been played yet (keeping the best of them)
                trump_card = None
                for card_played in cards_played:
                    if card_played.suit is trump:
                        if trump_card is None or card_played.beats(trump_card, served=served, trump=trump):
                            trump_card = card_played

                if self.__can_serve(served):  # can serve
                    if trump_card is None:  # no trump card played yet
                        return [card for card in self.cards if card.suit is served or card.suit is trump]
                    else:  # someone played a trump card -> can serve or play stronger trump card
                        return [card for card in self.cards
                                if card.suit is served or card.beats(trump_card, served=served, trump=trump)]

                else:  # cannot serve
                    if trump_card is None:  # cannot serve and no trump card played -> all cards are playable
                        return self.cards
                    else:  # someone played a trump card -> can play any non trump card and stronger trump card
                        playable_cards = [card for card in self.cards
                                          if card.suit is not trump
                                          or card.beats(trump_card, served=served, trump=trump)]
                        if len(playable_cards) == 0:
                            # this means all remaining cards are weaker trump cards, then it is okay to play them
                            return self.cards
                        else:
                            return playable_cards

    def __can_serve(self, suit: Suit, including_jack=True) -> bool:
        return suit in {card.suit for card in self.__cards if including_jack or card.rank is not Rank.jack}

    def __repr__(self):
        return f'Hand: {sorted(self.cards)}'
