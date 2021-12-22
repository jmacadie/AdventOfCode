from typing import List, Tuple

class Player:

    def __init__(self, posn: int, score: int=0, count: int=1) -> None:
        self.posn = posn
        self.score = score
        self.count = count

class DeterministicDiracDice:

    WIN_SCORE = 1000

    def __init__(self, player1_posn: int, player2_posn: int) -> None:
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

DDD = DeterministicDiracDice(4, 8)
DDD.play_game()
assert DDD.game_score() == 739785

DDD = DeterministicDiracDice(6, 10)
DDD.play_game()
assert DDD.game_score() == 853776
print(DDD.game_score())

class DiracDice:

    WIN_SCORE = 21
    SCORE_FREQ = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1
    }

    def __init__(self, player1_posn: int, player2_posn: int) -> None:
        self.player1 = [Player(player1_posn)]
        self.player2 = [Player(player2_posn)]
        self.player1_count = 1
        self.player2_count = 1
        self.player1_wins = 0
        self.player2_wins = 0
        self.next_go = 1

    def have_turn_one(self, player: Player) -> List[Player]:
        output = []
        for val in range(3, 10):
            new_posn = (player.posn + val) % 10
            if new_posn == 0:
                new_posn = 10
            new_score = player.score + new_posn
            new_count = player.count * self.SCORE_FREQ.get(val)
            new_player = Player(new_posn, new_score, new_count)
            output.append(new_player)
        return output

    def have_turn(self, player_states: List[Player]) -> List[Player]:
        output = [] # type: List[Player]
        for player in player_states:
            new_players = self.have_turn_one(player)
            output = self.combine_player_lists(output, new_players)
        return output

    def combine_player_lists(self, list1: List[Player], list2: List[Player]) -> List[Player]:
        output = list1.copy()
        for player2 in list2:
            found = False
            for player1 in output:
                if player1.score == player2.score and player1.posn == player2.posn:
                    player1.count += player2.count
                    found = True
                    break
            if not found:
                output.append(player2)
        output.sort(key=lambda p: p.score)
        return output

    def remove_winning_positions(self, player_states: List[Player]) -> Tuple[List[Player], int]:
        output = [] # type: List[Player]
        removed_count = 0
        for player in player_states:
            if player.score < self.WIN_SCORE:
                output.append(player)
            else:
                removed_count += player.count
        return output, removed_count

    def play_game(self) -> None:
        while self.player1 and self.player2:
            if self.next_go == 1:
                self.player1 = self.have_turn(self.player1)
                self.player1_count *= 27
                self.player1, removed_count = self.remove_winning_positions(self.player1)
                self.player1_count -= removed_count
                self.player1_wins += removed_count * self.player2_count
            else:
                self.player2 = self.have_turn(self.player2)
                self.player2_count *= 27
                self.player2, removed_count = self.remove_winning_positions(self.player2)
                self.player2_count -= removed_count
                self.player2_wins += removed_count * self.player1_count
            self.next_go = 2 if self.next_go == 1 else 1

    def winning_universes(self) -> int:
        return max(self.player1_wins, self.player2_wins)

DD = DiracDice(4, 8)
DD.play_game()
assert DD.winning_universes() == 444356092776315

DD = DiracDice(6, 10)
DD.play_game()
#assert DD.winning_universes() = 1
print(DD.winning_universes())
