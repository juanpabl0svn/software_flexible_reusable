from random import randrange
import pytest

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

    def move(self, roll: int, game: 'Game'):
        self.place = self.place + roll
        if self.place >= game.MAX_POSITION:
            self.place = self.place - game.MAX_POSITION
        return self.get_current_place()

    def get_golden_coins(self):
        return f"{self.name} now has {self.purse} Gold Coins."

    def add_golden_coin(self):
        self.purse += 1


class Question:
    text: str
    answer: str
    category: str

    def __init__(self, text: str, category: str):
        self.text = text
        self.category = category


class Game:
    players: list[Player]
    questions: list[Question]
    current_player: int
    is_getting_out_of_penalty_box: bool

    
    POP_PLACES = [0, 4, 8]
    SCIENCE_PLACES = [1, 5, 9]
    SPORTS_PLACES = [2, 6, 10]


    MAX_POSITION = 12

    MIN_PLAYERS = 2

    MAX_POINTS_TO_WIN = 6

    def __init__(self):
        self.players = []
        self.questions = []
        self.current_player = 0
        self.current_category = ""
        self.is_getting_out_of_penalty_box = False


    @property
    def _current_category(self):
        player = self.players[self.current_player]
        if player.place in self.POP_PLACES: return 'Pop'
        if player.place in self.SCIENCE_PLACES: return 'Science'
        if player.place in self.SPORTS_PLACES: return 'Sports'
        return 'Rock'

    @property
    def how_many_players(self):
        return len(self.players)

    def is_playable(self):
        return self.how_many_players >= self.MIN_PLAYERS

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

        player.move(roll, self)

        print(player.get_current_place())

        self._ask_question()

    def was_correctly_answered(self):
        player = self.players[self.current_player]

        if player.in_penalty_box and not self.is_getting_out_of_penalty_box:
            self.next_player()
            return False
        
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
        return False
    
    def _did_player_win(self):
        player = self.players[self.current_player]
        return (player.purse == self.MAX_POINTS_TO_WIN)
    
        
@pytest.fixture
def game():
  g = Game()
  g.questions = [Question(f"Question {i}", category) for i, category in 
           zip(range(50), ['Pop', 'Science', 'Sports', 'Rock'] * 13)]
  g.add_player(Player("Chet"))
  g.add_player(Player("Pat"))
  g.add_player(Player("Sue"))
  return g

def test_chet_wins(game: Game):
  winner = False
  i = 0
  while True:
    game.roll(randrange(5) + 1)
    if i % 3 == 0:
      winner = game.was_correctly_answered()
    else:
      winner = game.wrong_answer()
    if winner:
      assert game.current_player == 1
      break
    i += 1

def test_pat_wins(game: Game):
  winner = False
  i = 0
  while True:
    game.roll(randrange(5) + 1)
    if i % 3 == 1:
      winner = game.was_correctly_answered()
    else:
      winner = game.wrong_answer()
    if winner:
      assert game.current_player == 2
      break
    i += 1

def test_sue_wins(game: Game):
  winner = False
  i = 0
  while True:
    game.roll(randrange(5) + 1)
    if i % 3 == 2:
      winner = game.was_correctly_answered()
    else:
      winner = game.wrong_answer()
    if winner:
      assert game.current_player == 0
      break
    i += 1

def test_moves_6_and_gets_1_coin(game: Game):
  game.roll(6)
  game.was_correctly_answered()
  assert game.players[0].place == 6
  assert game.players[0].purse == 1

def test_enters_penalty_box_and_gets_out(game: Game):
  game.roll(5)
  game.wrong_answer()
  assert game.players[0].in_penalty_box is True
  game.current_player = 0
  game.roll(2)
  game.was_correctly_answered()
  assert game.players[0].in_penalty_box is False

def test_enters_penalty_box_and_doesnt_get_out(game: Game):
  game.roll(5)
  game.wrong_answer()
  assert game.players[0].in_penalty_box is True
  game.current_player = 0
  game.roll(3)
  game.was_correctly_answered()
  assert game.players[0].in_penalty_box is True

def test_cant_move_more_than_12(game: Game):
  game.roll(11)
  game.was_correctly_answered()
  assert game.players[0].place == 11
  game.current_player = 0
  game.roll(2)
  game.was_correctly_answered()
  assert game.players[0].place == 1


def test_can_move_more_than_12(game: Game):
  game.MAX_POSITION = 20
  game.roll(11)
  game.was_correctly_answered()
  assert game.players[0].place == 11
  game.current_player = 0
  game.roll(3)
  game.was_correctly_answered()
  assert game.players[0].place == 14

def test_game_not_playable_with_1_player():
  g = Game()
  g.add_player(Player("Chet"))
  assert g.is_playable() is False

def test_game_playable_with_2_players():
  g = Game()
  g.add_player(Player("Chet"))
  g.add_player(Player("Pat"))
  assert g.is_playable() is True
