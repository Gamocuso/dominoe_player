from basic_players import Player
# Implemente neste arquivo seus jogadores
class GuiPLayer(Player):
    
    def __init__(self):
        super().__init__(0, "Guilherme")
    
    def generate(self):
        dominoes = [[] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                dominoes[i].append((i, j))
        return dominoes

    def play(self, board_extremes, play_hist):

        def find_double(tiles, number):

            tiles = organize_tiles(tiles)

            double = [0,(-1,-1)]

            for tile in tiles:
                if tile[1][1] == tile[1][0] and t_sum(double[1]) < t_sum(tile[1]):
                    double = tile
                    if tile[1][0] == number:
                        return double

            if double[1][0] >= 0:
                return double
            else:
                return None
            
        def nones(p, play_hist):

            p_plays = [i for i in play_hist if i[0] == p]
            p_plays = p_plays[-1::-1] # inverter para pegar o histórico em seu seguimento

            nones = set()

            for play in p_plays:
                tile_played = play[-1]
                if tile_played == None:
                    if len(play[1]) > 0:
                        nones.add(play[1][0])
                        nones.add(play[1][1])

            return nones

        def play_mode(player, nones, poss_tiles, board_extremes):

            left = board_extremes[0]
            right = board_extremes[1]

            plays = []

            if player == "TEAM":

                for i in poss_tiles:
                    first = i[0]
                    second = i[1]
                    if first == left:
                        if second not in nones:
                            plays.append([0, i])
                    if first == right:
                        if second not in nones:
                            plays.append([1, i])
                    if second == left:
                        if first not in nones:
                            plays.append([0, i])
                    if second == right:
                        if first not in nones:
                            plays.append([1, i])
            
            else:

                for i in poss_tiles:
                    first = i[0]
                    second = i[1]
                    if first == left:
                        if second in nones:
                            plays.append([0, i])
                    if first == right:
                        if second in nones:
                            plays.append([1, i])
                    if second == left:
                        if first in nones:
                            plays.append([0, i])
                    if second == right:
                        if first in nones:
                            plays.append([1, i])

            return plays

        def t_sum(tile):
            return tile[0] + tile[1]

        def organize_tiles(tiles):

            def quick_sort(tile_list):

                if len(tile_list) <= 1:
                    return tile_list

                pivot = tile_list[-1]
                mid = []
                left = []
                right = []

                for tile in tile_list:

                    if type(tile) == tuple:
                        tile = [0, tile]    
                    if type(pivot) == tuple:
                        pivot = [0,pivot]

                    if t_sum(tile[1]) > t_sum(pivot[1]):
                        right.append(tile)
                    elif t_sum(tile[1]) < t_sum(pivot[1]):
                        left.append(tile)
                    else:
                        mid.append(tile)
                
                return quick_sort(left) + mid + quick_sort(right)
            
            return quick_sort(tiles)

    
        def count_hand():
            better_number = -1
            better_quantity = 0
            hand_tiles = self._tiles
            for x in range(10):  # eu acho que dá pra deixar isso mais eficiente usando um dicionário
                contagem = 0
                for tile in hand_tiles:
                    if tile[0] == x and tile[1] != x:
                        contagem += 1
                    elif tile[1] == x and tile[0] != x:
                        contagem += 1
                    elif tile[0] == x and tile[1] == x:
                        contagem += 1
                if contagem > better_quantity:
                    better_number = x
                    better_quantity = contagem
                elif contagem == better_quantity and x > better_number:
                    better_number = x
            return better_number, better_quantity
        
        def best_play (number, hand, extremes):

            if len(extremes) > 1 and len(hand) > 1:

                if len(play_hist) > 2:

                    friend_nones = nones(play_hist[-2][0], play_hist)
                    enemie_nones = nones(play_hist[-3][0], play_hist)

                    defensive_plays = []
                    offensive_plays = []

                    if len(friend_nones) > 1:
                        defensive_plays = play_mode("TEAM", friend_nones, hand.copy(), extremes)
                    if len(enemie_nones) > 1:
                        offensive_plays = play_mode("ENEMIE", enemie_nones, hand.copy(), extremes)

                    plays = []

                    if len(defensive_plays) > 0:
                        plays += defensive_plays
                    if len(offensive_plays) > 0:
                        plays += offensive_plays

                    if len(plays) > 0:
                        plays = organize_tiles(plays)
                        double_play = find_double(plays, number)
                        play = plays[-1] if not double_play else double_play
                        return play[0], play[1]

                hand = organize_tiles(hand)
                double_hand = find_double(hand, number)
                if double_hand:
                    return double_hand[0], double_hand[1]
                left = extremes[0]
                right = extremes[1]

                for tile in hand:
                    if tile[1][0] == number:
                        if tile[1][1] == left:
                            return tile[0], tile[1]
                        elif tile[1][1] == right:
                            return tile[0] , tile[1]
                    elif tile[1][1] == number:
                        if tile[1][0] == left:
                            return tile[0] , tile[1]
                        elif tile[1][0] == right:
                            return tile[0] , tile[1]
                
                
                last_attempt = hand[-1]

                if left == last_attempt[1][0] or left == last_attempt[1][1]:
                    last_attempt[0] = 0
                else:
                    last_attempt[0] = 1

                return last_attempt[0], last_attempt[1]

            return 1, None

        playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        print(playable_tiles)
        hand_tiles = self._tiles
        if len(board_extremes) < 1:
            return 1, hand_tiles[0]
        if len(playable_tiles) == 1:
            return 1, playable_tiles[0]
        number_ , quantity = count_hand()
        print(number_)
        
        best_play = best_play(number_, playable_tiles, board_extremes)

        return best_play

class MoreiraPlayer(Player):
    
    def __init__(self):
        super().__init__(2, "Moreira")
    
    def generate(self):
        dominoes = [[] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                dominoes[i].append((i, j))
        return dominoes

    def play(self, board_extremes, play_hist):

        def probabilitie(play_hist, poss_tiles, board_extremes):

            p_enemie = play_hist[-3][0]
            enemie_plays = [i for i in play_hist if i[0] == p_enemie]
            enemie_plays = enemie_plays[-1::-1] # inverter para pegar o histórico em seu seguimento

            nones = set()

            for play in enemie_plays:
                if play[-1] == None and len(play[1]) > 0:
                    nones.add(play[1][0])
                    nones.add(play[1][1])

            left = board_extremes[0]
            right = board_extremes[1]

            plays = []

            for i in poss_tiles:
                first = i[0]
                second = i[1]
                if first == left:
                    if second in nones:
                        plays.append((0, i))
                if first == right:
                    if second in nones:
                        plays.append((1, i))
                if second == left:
                    if first in nones:
                        plays.append((0, i))
                if second == right:
                    if first in nones:
                        plays.append((1, i))

            return plays

        def count_hand():
            better_number = -1
            better_quantity = 0
            hand_tiles = self._tiles
            for x in range(10):
                contagem = 0
                for tile in hand_tiles:
                    if tile[0] == x and tile[1] != x:
                        contagem += 1
                    elif tile[1] == x and tile[0] != x:
                        contagem += 1
                    elif tile[0] == x and tile[1] == x:
                        contagem += 1
                if contagem > better_number:
                    better_number = x
                    better_quantity = contagem
                return better_number, better_quantity
        
        def best_play (number, hand, extremes):

            if len(extremes) > 1:
                if len(play_hist) > 2:
                    agressive_play_ = probabilitie(play_hist, hand, extremes)

                    if len(agressive_play_) > 0:
                        better = [0, [0]]

                        for play in agressive_play_:
                            side = play[0]
                            tile = play[1]
                            if sum(tile) > sum(better[1]):
                                better = [side, tile]
                        
                        return better[0], better[1]

                for tile in hand:
                    if tile[0] == number:
                        if tile[1] == extremes[0]:
                            return 0 , tile
                        elif tile[1] == extremes[1]:
                            return 1 , tile
                    elif tile[1] == number:
                        if tile[0] == extremes[0]:
                            return 0 , tile
                        elif tile[0] == extremes[1]:
                            return 1 , tile
            return None

        playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        hand_tiles = self._tiles
        if len(board_extremes) < 1 and len(playable_tiles) > 1:
            return playable_tiles[0]
        number_ , quantity = count_hand()
        
        if best_play(number_, playable_tiles, board_extremes) != None:
            return best_play(number_, playable_tiles, board_extremes)
        else:
            bigger = -1
            tile = -1
            for x in playable_tiles:
                if (int(x[0]) + int(x[1])) > bigger:
                    bigger = int(x[0]) + int(x[1])
                    tile = x
            if tile != -1:
                if board_extremes[0] == tile[0] or board_extremes[0] == tile[1]:
                    return 1, tile
                else:
                    return 2, tile
        return 1, None

class fdpPlayer(Player):

    def __init__(self):
        super().__init__(2, "Moreira")

    def play(self, board_extremes, play_hist):
        playable_tiles = self._tiles
        if len(board_extremes) > 0:
            playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        highest = -1
        tile_sum = -1
        for i in range(len(playable_tiles)):
            if playable_tiles[i][0] + playable_tiles[i][1] > tile_sum:
                tile_sum = playable_tiles[i][0] + playable_tiles[i][1]
                highest = i
        if highest >= 0:
            return 1, playable_tiles[highest]
        else:
            return 1, None

# Função que define o nome da dupla:
def pair_name():
    return "Winners" # Defina aqui o nome da sua dupla

# Função que cria a dupla:
def create_pair():
    return (GuiPLayer(), GuiPLayer()) # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.	
