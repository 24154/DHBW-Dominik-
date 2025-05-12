import random

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces = [0, 0, 0, 0]  # All pieces start at the home position

    def move_piece(self, piece_index, steps):
        if self.pieces[piece_index] + steps <= 40:  # The board has 40 positions
            self.pieces[piece_index] += steps

    def has_won(self):
        return all(piece == 40 for piece in self.pieces)

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"{current_player.name}'s turn. Pieces: {current_player.pieces}")

        dice_roll = self.roll_dice()
        print(f"{current_player.name} rolled a {dice_roll}")

        if dice_roll == 6:
            print(f"{current_player.name} gets another turn!")
            self.play_turn()

        movable_pieces = [i for i in range(4) if current_player.pieces[i] + dice_roll <= 40]
        
        if not movable_pieces:
            print(f"{current_player.name} cannot move any piece.")
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return False

        piece_index = random.choice(movable_pieces)
        current_player.move_piece(piece_index, dice_roll)
        print(f"{current_player.name} moved piece {piece_index} to position {current_player.pieces[piece_index]}")

        if current_player.has_won():
            print(f"{current_player.name} has won the game!")
            return True

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return False

def main():
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    player_colors = ["Red", "Blue", "Green", "Yellow"]
    players = [Player(name, color) for name, color in zip(player_names, player_colors)]
    
    game = Game(players)
    
    game_over = False
    while not game_over:
        game_over = game.play_turn()

if __name__ == "__main__":
    main()
