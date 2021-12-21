class Player:

    def __init__(self, posn: int) -> None:
        self.posn = posn
        self.score = 0

class DiracDice:

    WIN_SCORE = 1000

    def __init__(self, player1_posn: int, player2_posn) -> None:
        self.player1 = Player(player1_posn)
        self.player2 = Player(player2_posn)
        self.next_go = 1
        self.die_val = 0

    def roll_dice(self) -> int:
        self.die_val += 1
        return self.die_val

    def roll_turn(self) -> int:
        a = self.roll_dice()
        b = self.roll_dice()
        c = self.roll_dice()
        return (a + b + c) % 10

    def game_over(self) -> bool:
        if self.player1.score >= self.WIN_SCORE:
            return True
        if self.player2.score >= self.WIN_SCORE:
            return True
        return False

    def have_turn(self, player: Player) -> None:
        val = self.roll_turn()
        new_posn = (player.posn + val) % 10
        if new_posn == 0:
            new_posn = 10
        player.posn = new_posn
        player.score += new_posn
        self.next_go = 2 if self.next_go == 1 else 1

    def play_game(self) -> None:
        while not self.game_over():
            if self.next_go == 1:
                self.have_turn(self.player1)
            else:
                self.have_turn(self.player2)

    def game_score(self) -> int:
        score = min(self.player1.score, self.player2.score)
        score *= self.die_val
        return score

DD = DiracDice(4, 8)
DD.play_game()
assert DD.game_score() == 739785

DD = DiracDice(6, 10)
DD.play_game()
assert DD.game_score() == 853776
print(DD.game_score())
