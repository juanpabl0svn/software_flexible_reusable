from random import randrange

class Player:
    name: str
    purse: int
    in_penalty_box: bool
    place: int

    def __init__(self, name: str):
        self.name = name
        self.purse = 0
        self.in_penalty_box = False
        self.place = 0

    def get_current_place(self):
        return f"{self.name}\'s new location is {self.place}"
    
    def move(self, roll: int):
        self.place = self.place + roll
        if self.place > 11:
            self.place = self.place - 12
        return self.get_current_place()
    
    def get_golden_coins(self):
        return f"{self.name} now has {self.purse} Gold Coins."

    def add_golden_coin(self):
        self.purse += 1


class Question:
    text: str
    answer: str
    category: str

    def __init__(self, text: str, answer: str, category: str):
        self.text = text
        self.category = category


class Game:
    players: list[Player]
    questions: list[Question]
    current_player: int
    # is_getting_out_of_penalty_box: bool

    def __init__(self):
        self.players = []
        self.questions = []
        self.current_player = 0
        self.current_category = ""


    @property
    def _current_category(self):
        player = self.players[self.current_player]
        if player.place in [0, 4, 8]: return 'Pop'
        if player.place in [1, 5, 9]: return 'Science'
        if player.place in [2, 6, 10]: return 'Sports'
        return 'Rock'

    @property
    def how_many_players(self):
        return len(self.players)

    def is_playable(self):
        return self.how_many_players >= 2

    def add_player(self, player: Player):
        self.players.append(player)

        print(player.name + " was added")
        print("They are player number %s" % len(self.players))

        return True
    
    def _ask_question(self):
        print("The category is %s" % self._current_category)
        for question in self.questions:
            if question.category == self._current_category:
                print(question.text)
                self.questions.remove(question)
                return

    def roll(self, roll: int):
        player = self.players[self.current_player]

        print("%s is the current player" % player.name)
        print("They have rolled a %s" % roll)

        if player.in_penalty_box and roll % 2 != 0:
              print("%s is not getting out of the penalty box" % player.name)
              self.is_getting_out_of_penalty_box = False
              return
        
        if player.in_penalty_box:
            self.is_getting_out_of_penalty_box = True

        print("%s is getting out of the penalty box" % player.name)

        player.move(roll)

        print(player.get_current_place())

        self._ask_question()

    def was_correctly_answered(self):
        player = self.players[self.current_player]

        if player.in_penalty_box and not self.is_getting_out_of_penalty_box:
            self.next_player()
            return True
        
        if player.in_penalty_box:
            player.in_penalty_box = False

        print("Answer was correct!!!!")
        player.add_golden_coin()
        print(player.get_golden_coins())

        winner = self._did_player_win()
        
        self.next_player()

        return winner 
    
    def next_player(self):
        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
    

    def wrong_answer(self):
        player = self.players[self.current_player]
        print('Question was incorrectly answered')
        print("%s was sent to the penalty box" % player.name)
        player.in_penalty_box = True

        self.next_player()
        return True
    
    def _did_player_win(self):
        player = self.players[self.current_player]
        return not (player.purse == 6)
    
        

# if __name__ == '__main__':
#     not_a_winner = False

#     game = Game()

#     game.questions = [Question(f"Question {i}", "Answer", category) for i, category in 
#                       zip(range(50), ['Pop', 'Science', 'Sports', 'Rock'] * 13)]

#     game.add_player(Player("Chet"))
#     game.add_player(Player("Pat"))
#     game.add_player(Player("Sue"))

#     while True:
#         roll = randrange(5) + 1
#         game.roll(roll)


#         if randrange(9) == 7:
#             not_a_winner = game.wrong_answer()
#         else:
#             not_a_winner = game.was_correctly_answered()

#         if not not_a_winner:
#             print(f"{game.players[game.current_player].name} has won the game!")
#             break
        
import pytest
@pytest.fixture
def game():
  g = Game()
  g.questions = [Question(f"Question {i}", "Answer", category) for i, category in 
           zip(range(50), ['Pop', 'Science', 'Sports', 'Rock'] * 13)]
  g.add_player(Player("Chet"))
  g.add_player(Player("Pat"))
  g.add_player(Player("Sue"))
  return g

def test_chet_wins(game):
  not_a_winner = True
  i = 0
  while True:
    game.roll(randrange(5) + 1)
    if i % 3 == 0:
      not_a_winner = game.was_correctly_answered()
    else:
      not_a_winner = game.wrong_answer()
    if not not_a_winner:
      assert game.current_player == 1
      break
    i += 1

def test_pat_wins(game):
  not_a_winner = True
  i = 0
  while True:
    game.roll(randrange(5) + 1)
    if i % 3 == 1:
      not_a_winner = game.was_correctly_answered()
    else:
      not_a_winner = game.wrong_answer()
    if not not_a_winner:
      assert game.current_player == 2
      break
    i += 1

def test_sue_wins(game):
  not_a_winner = True
  i = 0
  while True:
    game.roll(randrange(5) + 1)
    if i % 3 == 2:
      not_a_winner = game.was_correctly_answered()
    else:
      not_a_winner = game.wrong_answer()
    if not not_a_winner:
      assert game.current_player == 0
      break
    i += 1

def test_moves_6_and_gets_1_coin(game):
  game.roll(6)
  game.was_correctly_answered()
  assert game.players[0].place == 6
  assert game.players[0].purse == 1

def test_enters_penalty_box_and_gets_out(game):
  game.roll(5)
  game.wrong_answer()
  assert game.players[0].in_penalty_box is True
  game.current_player = 0
  game.roll(2)
  game.was_correctly_answered()
  assert game.players[0].in_penalty_box is False

def test_enters_penalty_box_and_doesnt_get_out(game):
  game.roll(5)
  game.wrong_answer()
  assert game.players[0].in_penalty_box is True
  game.current_player = 0
  game.roll(3)
  game.was_correctly_answered()
  assert game.players[0].in_penalty_box is True

def test_cant_move_more_than_12(game):
  game.roll(11)
  game.was_correctly_answered()
  assert game.players[0].place == 11
  game.current_player = 0
  game.roll(2)
  game.was_correctly_answered()
  assert game.players[0].place == 1


