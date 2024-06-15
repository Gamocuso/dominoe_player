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
            """
            Baseado no player, a função retorna as possíveis jogadas
            podendo elas serem defensivas ou ofesivas dado o mesmo parâmetro.

            --> jogadas defensivas: não prejudicam o amigo

            --> ofensivas: buscam prejudicar o inimigo
            """
            left = board_extremes[0]
            right = board_extremes[1]

            plays = []
            blocks = []

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

                    if left in nones:
                        if first == right and second in nones:
                            blocks.append([1, i])
                        elif second == right and first in nones:
                            blocks.append([1, i])

                    if right in nones:
                        if first == left and second in nones:
                            blocks.append([0, i])
                        elif second == left and first in nones:
                            blocks.append([0, i])

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
                
                if len(blocks) > 0:
                    print("BLOCK PLAAY!!")
                    return blocks

            return plays

        def t_sum(tile):
            """
            Retorna o valor total da peça
            """
            return tile[0] + tile[1]

        def organize_tiles(tiles):
            """
            Organiza as peças em ordem crescente utilizando o quickSort
            """

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
            """
            Conta as peças na mão e retorna a peça
            de maior ocorrência
            """

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
            """
            Sequência de estratégias que retornam a melhor jogada
            baseado na ordem de prioridade adotada
            """

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

                    if len(offensive_plays) > 0:
                        offensive_plays = organize_tiles(offensive_plays)
                        double_offensive = find_double(offensive_plays, number) 
                        if double_offensive:
                            return double_offensive[0], double_offensive[1]
                        else:
                            return offensive_plays[-1][0], offensive_plays[-1][1]

                    if len(defensive_plays) > 0:
                        defensive_plays = organize_tiles(defensive_plays)
                        double_defensive = find_double(defensive_plays, number) 
                        if double_defensive:
                            return double_defensive[0], double_defensive[1]
                        else:
                            return defensive_plays[-1][0], defensive_plays[-1][1]

                hand = organize_tiles(hand)
                double_hand = find_double(hand, number)

                if double_hand:
                    return double_hand[0], double_hand[1]
                    
                left = extremes[0]
                right = extremes[1]

                for tile in hand[-1::-1]:
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
        hand_tiles = self._tiles
        if len(board_extremes) < 1:
            return 1, hand_tiles[0]
        if len(playable_tiles) == 1:
            return 1, playable_tiles[0]
        number_ , quantity = count_hand()
        
        best_play = best_play(number_, playable_tiles, board_extremes)

        return best_play

# Função que define o nome da dupla:
def pair_name():
    return "Winners" # Defina aqui o nome da sua dupla

# Função que cria a dupla:
def create_pair():
    return (GuiPLayer(), GuiPLayer()) # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.	