import random


class UnoCard:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}"

class UnoDeck:
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
    special_values = ['Wild', '+4']

    def __init__(self):
        self.cards = []
        for color in self.colors:
            for value in self.values:
                self.cards.append(UnoCard(color, value))
                if value != '0':
                    self.cards.append(UnoCard(color, value))
        for _ in range(4):
            self.cards.append(UnoCard('Black', 'Wild'))
            self.cards.append(UnoCard('Black', '+4'))
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.reshuffle_discard_pile()
        return self.cards.pop()

    def reshuffle_discard_pile(self):
        if len(self.discard_pile) > 1:
            self.cards = self.discard_pile[:-1]
            random.shuffle(self.cards)
            self.discard_pile = [self.discard_pile[-1]]

class UnoPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_cards(self, deck, num=1):
        for _ in range(num):
            self.hand.append(deck.draw_card())

    def play_card(self, card):
        self.hand.remove(card)
        return card
class UnoGame:
    def __init__(self, players):
        self.deck = UnoDeck()
        self.players = [UnoPlayer(name) for name in players]
        for player in self.players:
            player.draw_cards(self.deck, 7)
        self.discard_pile = [self.deck.draw_card()]
        self.deck.discard_pile = self.discard_pile
        self.current_player_index = 0
        self.direction = 1

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"{current_player.name}'s turn. Hand: {current_player.hand}")
        
        playable_cards = [card for card in current_player.hand if card.color == self.discard_pile[-1].color or card.value == self.discard_pile[-1].value or card.color == 'Black']
        
        if playable_cards:
            chosen_card = random.choice(playable_cards)
            print(f"{current_player.name} plays {chosen_card}")
            self.discard_pile.append(current_player.play_card(chosen_card))
            
            if chosen_card.value == 'Reverse':
                self.direction *= -1
            elif chosen_card.value == 'Skip':
                self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
            elif chosen_card.value == '+2':
                next_player_index = (self.current_player_index + self.direction) % len(self.players)
                self.players[next_player_index].draw_cards(self.deck, 2)
            elif chosen_card.value == '+4':
                next_player_index = (self.current_player_index + self.direction) % len(self.players)
                self.players[next_player_index].draw_cards(self.deck, 4)
        
        else:
            print(f"{current_player.name} has no playable cards and draws a card")
            current_player.draw_cards(self.deck)

        if not current_player.hand:
            print(f"{current_player.name} wins!")
            return True
        
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        return False

def main():
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    game = UnoGame(player_names)
    
    game_over = False
    while not game_over:
        game_over = game.play_turn()

if __name__ == "__main__":
    main()

