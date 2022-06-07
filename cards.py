import random


class Cards:
    def __init__(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        names = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen',
                 'King']
        initial_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        initial_values.sort()
        card_names = [f'{name} of {suit}' for name in names for suit in suits]
        deck = dict(zip(card_names, initial_values))
        keys = list(deck.keys())
        self.deck = [[key, deck[key]] for key in keys]
        self.deck *= 6
        random.shuffle(self.deck)
        self.discard = []

    def shuffle_cards(self):
        self.deck += self.discard
        random.shuffle(self.deck)
        self.discard = []

    def cut(self):
        cut_length = random.randint(60, 75)
        self.discard = self.deck[-cut_length:]
        del self.deck[-cut_length:]

    def deal(self):
        player = []
        dealer = []
        for i in range(4):
            card = self.deck.pop()
            self.discard.append(card)
            if i == 0 or i == 2:
                player.append(card)
            else:
                dealer.append(card)
        return player, dealer

    def hit(self):
        card = self.deck.pop()
        self.discard.append(card)
        return card
