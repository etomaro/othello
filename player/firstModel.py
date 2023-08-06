from player.abstruct import Player
import random


class FirstModelPlayer(Player):
    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id

    def action(self, game):
        """
        アクションをする
        """
        actionables = game.get_actionables(self.player_id)
        if len(actionables) == 0:
            raise Exception("アクションできません")
        
        action = self._choice(actionables, game.board.copy(), self.player_id)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        return next_player_id, actionables, is_game_over


    def _get_actionables(self, state, player_id):
        """
        args: 
            state: 盤上の状態
                ['...101..', '..0101..', ...]
            player_id: 自分のプレイヤーID(0 or 1)
        
        処理: 
            1. 石が置かれていない場所を取得
            2. 石を置くことができるか判定
            3. game用の表記に直す(col: a-h, row: 1-8)
        """

        OPPONENT_ID = "0" if player_id == "1" else "1"

        # 1. 石が置かれていない場所を取得
        empty_places = []
        for idx, row in enumerate(state):
            for jdx, col in enumerate(row):
                if col == ".":
                    empty_places.append([idx, jdx])
        
        # 2. 石を置くことができるか判定
        actionables = []
        for empty_place in empty_places:
            row, col = empty_place
            # 周りの8隅の座標
            frame_places = [[row-1, col-1], [row-1, col], [row-1, col+1], [row, col-1], [row, col+1], [row+1, col-1], [row+1, col], [row+1, col+1]]
            # 周りの8個に相手の石があるかどうか。ある場合挟めるかどうか判定
            for frame_place in frame_places:
                frame_row, frame_col = frame_place
                # ボードの外に出る場合は除外
                if frame_row < 0 or frame_row > 7 or frame_col < 0 or frame_col > 7:
                    continue
                # 自分の石がある場合は除外
                if state[frame_row][frame_col] == player_id:
                    continue
                # 石がない場合は除外
                if state[frame_row][frame_col] == ".":
                    continue
                # 相手の石がある場合
                if state[frame_row][frame_col] == OPPONENT_ID:
                    # ベクトル(周りの8個の座標 - 相手の石の場所の座標)
                    vector = [frame_row - row, frame_col - col]
                    # 自分の石があるまでループ
                    next_row = frame_row + vector[0]
                    next_col = frame_col + vector[1]
                    while True:
                        # ボードの外に出る場合は除外
                        if next_row < 0 or next_row > 7 or next_col < 0 or next_col > 7:
                            break 
                        # 石が置かれていない場合は除外
                        if state[next_row][next_col] == ".":
                            break
                        # 自分の石がある場合は挟める
                        if state[next_row][next_col] == player_id:
                            if empty_place not in actionables:
                                actionables.append(empty_place)
                            break
                        # 相手の石がある場合は次の座標を更新
                        if state[next_row][next_col] == OPPONENT_ID:
                            next_row += vector[0]
                            next_col += vector[1]
                            continue

                        # ここには来ないはず
                        print("error")
        
        # 3. game用の表記に直す(col: a-h, row: 1-8)
        for idx, actionable in enumerate(actionables):
            row, col = actionable
            col = chr(col + 97)
            row = str(row + 1)
            actionables[idx] = col + row

        
        return actionables


    def _get_next_state(self, state, action, player_id):
        """
        player_id: アクションをするプレイヤーのID
        """
        OPPONENT_ID = "0" if player_id == "1" else "1"

        # 1. actionを座標に変換
        col = ord(action[0]) - 97
        row = int(action[1]) - 1

        next_state = state.copy()
        # アクションした座標の値の更新
        new_row = list(next_state[row])
        new_row[col] = player_id
        next_state[row] = "".join(new_row)

        # 2. 挟める石を挟む
        # 周りの8隅の座標
        frame_places = [[row-1, col-1], [row-1, col], [row-1, col+1], [row, col-1], [row, col+1], [row+1, col-1], [row+1, col], [row+1, col+1]]
        # 周りの8個に相手の石があるかどうか。ある場合挟めるかどうか判定
        change_places_all = []  # 挟んだすべての石の座標
        for frame_place in frame_places:
            frame_row, frame_col = frame_place
            # ボードの外に出る場合は除外
            if frame_row < 0 or frame_row > 7 or frame_col < 0 or frame_col > 7:
                continue
            # 自分の石がある場合は除外
            if state[frame_row][frame_col] == player_id:
                continue
            # 石がない場合は除外
            if state[frame_row][frame_col] == ".":
                continue
            # 相手の石がある場合
            change_places = []  # 挟める石の座標
            if state[frame_row][frame_col] == OPPONENT_ID:
                # 挟める石を追加
                change_places.append([frame_row, frame_col])
                # ベクトル(周りの8個の座標 - 相手の石の場所の座標)
                vector = [frame_row - row, frame_col - col]
                # 自分の石があるまでループ
                next_row = frame_row + vector[0]
                next_col = frame_col + vector[1]
                while True:
                    # ボードの外に出る場合は除外
                    if next_row < 0 or next_row > 7 or next_col < 0 or next_col > 7:
                        break 
                    # 石が置かれていない場合は除外
                    if state[next_row][next_col] == ".":
                        break
                    # 自分の石がある場合は挟める
                    if state[next_row][next_col] == player_id:
                        # 挟む
                        for change_place in change_places:
                            change_row, change_col = change_place
                            # stateの更新
                            new_row = list(next_state[change_row])
                            new_row[change_col] = player_id
                            next_state[change_row] = "".join(new_row)

                            # 挟んだ石の座標を追加
                            change_places_all.append([change_row, change_col])
                        break
                    # 相手の石がある場合は次の座標を更新
                    if state[next_row][next_col] == OPPONENT_ID:
                        # 挟める石を追加
                        change_places.append([next_row, next_col])

                        next_row += vector[0]
                        next_col += vector[1]
                        continue

                    # ここには来ないはず
                    print("error")


        next_player_id = "0" if player_id == "1" else "1"

        # game用の表記に直す(col: a-h, row: 1-8)
        for idx, change_place in enumerate(change_places_all):
            row, col = change_place
            col = chr(col + 97)
            row = str(row + 1)
            change_places_all[idx] = col + row

        return next_state, next_player_id, change_places_all


    # アクションを選択する
    def _choice(self, actionable, state, player_id):
        """
        引数
            actionable: 自分の可能なアクション
            state: 現在の状態
            player_id: 自分のプレイヤーID(0 or 1)
        
        処理
            計算する状態の推移(t -> t+1 -> t+2)

            評価する
            評価に必要なパラメーター(get_next_stateでt+1になる)
                [t]
                opponent_corner_count: 現在の相手が取れる角の数
                opponent_edge_count: 現在の相手が取れる端の数
                reverse_my_edge_count: 現在の相手がひっくり返すことができる端の数
                [t+1]
                is_good_musikui: 「相手の石、自分の石、相手の石」のような行動
                is_bad_musikui:「自分の石 , 何も置かれてない , 自分の石」のような行動
                reverse_opponent_edge_count: 現在の自分がひっくり返すことができる端の数
                action: 自分のアクションが角か端かそれ以外か
                len(next_actionable): 次の相手のアクション数
                next_opponent_corner_count: 次の相手が取れる角の数
                next_opponent_edge_count: 次の相手が取れる端の数
                [t+2]
                next_reverse_my_edge_count: 次の相手がひっくり返すことができる端の数

            計算方法
                (現在の相手が取れる角の数 - 次の相手が取れる角の数) * 1万点 +
                (現在の相手が取れる端の数 - 次の相手が取れる端の数) * 100点 +
                (100点 - 次の相手の手数)
                自分が角を取れるアクション: 1万点
                自分が端を取れるアクション: 100点
                自分のアクションによってひっくり返した相手の端の数 * (200点) 
                (現在の相手がひっくり返すことができる端の数 - 次の相手がひっくり返すことができる端の数) * 200点
                a1に石が置いてない場合にb2に石を置くと-3000点。
                a8に石が置いてない場合にa7に石を置くと-3000点。
                h1に石が置いてない場合にg2に石を置くと-3000点。
                h8に石が置いてない場合にg7に石を置くと-3000点。
                a1に石が置いてない場合にb2の石をひっくり返すと-3000点。
                a8に石が置いてない場合にa7の石をひっくり返すと-3000点。
                h1に石が置いてない場合にg2の石をひっくり返すと-3000点。
                h8に石が置いてない場合にg7の石をひっくり返すと-3000点。
                「自分の石 , 何も置かれてない , 自分の石」のようにする行動をすると-1000点
                「相手の石、自分の石、相手の石」となるような行動をすると+1000点

        """
        # 座標をゲーム用に変換
        for idx, action in enumerate(actionable):
            row, col = action
            col = chr(col + 97)
            row = str(row + 1)
            actionable[idx] = col + row


        OPPONENT_ID = "0" if player_id == "1" else "1"

        # 評価結果
        evaluete = {}

        # --- [t] ---
        opponent_corner_count = 0  # 現在の相手が取れる角の数
        opponent_edge_count = 0  # 現在の相手が取れる端の数
        reverse_my_edge_count = 0  # 現在の相手がひっくり返すことができる端の数

        now_opponet_actionables = self._get_actionables(state, OPPONENT_ID)
        for action in now_opponet_actionables:
            if action == "a1" or action == "a8" or action == "h1" or action == "h8":
                opponent_corner_count += 1
            elif action == "a2" or action == 'a3' or action == 'a4' or action == 'a5' or action == 'a6' or action == 'a7' or \
                action == 'b1' or action == 'b8' or action == 'c1' or action == 'c8' or action == 'd1' or action == 'd8' or \
                action == 'e1' or action == 'e8' or action == 'f1' or action == 'f8' or action == 'g1' or action == 'g8' or \
                action == 'h2' or action == 'h3' or action == 'h4' or action == 'h5' or action == 'h6' or action == 'h7':
                opponent_edge_count += 1

            reverse_count = 0
            next_state, next_player_id, opponent_reverse_places = self._get_next_state(state, action, OPPONENT_ID)
            for opponent_reverse_place in opponent_reverse_places:
                if opponent_reverse_place == "a2" or opponent_reverse_place == 'a3' or opponent_reverse_place == 'a4' or opponent_reverse_place == 'a5' or opponent_reverse_place == 'a6' or opponent_reverse_place == 'a7' or \
                    opponent_reverse_place == 'b1' or opponent_reverse_place == 'b8' or opponent_reverse_place == 'c1' or opponent_reverse_place == 'c8' or opponent_reverse_place == 'd1' or opponent_reverse_place == 'd8' or \
                    opponent_reverse_place == 'e1' or opponent_reverse_place == 'e8' or opponent_reverse_place == 'f1' or opponent_reverse_place == 'f8' or opponent_reverse_place == 'g1' or opponent_reverse_place == 'g8' or \
                    opponent_reverse_place == 'h2' or opponent_reverse_place == 'h3' or opponent_reverse_place == 'h4' or opponent_reverse_place == 'h5' or opponent_reverse_place == 'h6' or opponent_reverse_place == 'h7':
                    reverse_count += 1
            
            if reverse_count > reverse_my_edge_count:
                reverse_my_edge_count = reverse_count
        

        for action in actionable:
            # --- [t+1] ---
            is_good_musikui = False  # 逆虫食い
            is_bad_musikui = False  # 虫食い
            reverse_opponent_edge_count = 0  # 現在の自分がひっくり返すことができる端の数

            # 座標を取得
            col = ord(action[0]) - 97
            row = int(action[1]) - 1
            
            # 虫食いの判定
            if action == "b1" or action == "b8":
                # 右に石無いかつ右の右に自分の石がある場合は虫食い
                if state[row][col+1] == "." and state[row][col+2] == player_id:
                    is_bad_musikui = True
            elif action == "c1" or action == "d1" or action == "e1" or action == "f1" or action == "c8" or action == "d8" or action == "e8" or action == "f8":
                if state[row][col-1] == "." and state[row][col-2] == player_id:
                    # 左に石無いかつ左の左に自分の石がある場合は虫食い
                    is_bad_musikui = True
                elif state[row][col+1] == "." and state[row][col+2] == player_id:
                    # 右に石無いかつ右の右に自分の石がある場合は虫食い
                    is_bad_musikui = True
            elif action == "g1" or action == "g8":
                # 左に石無いかつ左の左に自分の石がある場合は虫食い
                if state[row][col-1] == "." and state[row][col-2] == player_id:
                    is_bad_musikui = True
            elif action == "a2" or action == "h2":
                # 下に石無いかつ下の下に自分の石がある場合は虫食い
                if state[row+1][col] == "." and state[row+2][col] == player_id:
                    is_bad_musikui = True
            elif action == "a3" or action == "a4" or action == "a5" or action == "a6" or action == "h3" or action == "h4" or action == "h5" or action == "h6":
                if state[row-1][col] == "." and state[row-2][col] == player_id:
                    # 上に石無いかつ上の上に自分の石がある場合は虫食い
                    is_bad_musikui = True
                elif state[row+1][col] == "." and state[row+2][col] == player_id:
                    # 下に石無いかつ下の下に自分の石がある場合は虫食い
                    is_bad_musikui = True
            elif action == "a7" or action == "h7":
                # 上に石無いかつ上の上に自分の石がある場合は虫食い
                if state[row-1][col] == "." and state[row-2][col] == player_id:
                    is_bad_musikui = True

            # 逆虫食いの判定
            if action == "a2" or action == "a3" or action == "a4" or action == "a5" or action == "a6" or action == "a7" or \
            action == "h2" or action == "h3" or action == "h4" or action == "h5" or action == "h6" or action == "h7":
                # 上下に相手の石があれば逆虫食い
                if state[row-1][col] == OPPONENT_ID and state[row+1][col] == OPPONENT_ID:
                    is_good_musikui = True
            elif action == "b1" or action == "c1" or action == "d1" or action == "e1" or action == "f1" or action == "g1" or \
            action == "b8" or action == "c8" or action == "d8" or action == "e8" or action == "f8" or action == "g8":
                # 左右に相手の石があれば逆虫食い
                if state[row][col-1] == OPPONENT_ID and state[row][col+1] == OPPONENT_ID:
                    is_good_musikui = True

            # アクションをした時の次の状態を取得
            next_state, next_player_id, my_reverse_places = self._get_next_state(state, action, player_id)

            for my_reverse_place in my_reverse_places:
                if my_reverse_place == "a2" or my_reverse_place == 'a3' or my_reverse_place == 'a4' or my_reverse_place == 'a5' or my_reverse_place == 'a6' or my_reverse_place == 'a7' or \
                    my_reverse_place == 'b1' or my_reverse_place == 'b8' or my_reverse_place == 'c1' or my_reverse_place == 'c8' or my_reverse_place == 'd1' or my_reverse_place == 'd8' or \
                    my_reverse_place == 'e1' or my_reverse_place == 'e8' or my_reverse_place == 'f1' or my_reverse_place == 'f8' or my_reverse_place == 'g1' or my_reverse_place == 'g8' or \
                    my_reverse_place == 'h2' or my_reverse_place == 'h3' or my_reverse_place == 'h4' or my_reverse_place == 'h5' or my_reverse_place == 'h6' or my_reverse_place == 'h7':
                    reverse_opponent_edge_count += 1

            # 相手がアクション出来る場所を取得
            next_actionable = self._get_actionables(next_state, next_player_id)

            next_opponent_corner_count = 0  # 次の相手が取れる角の数
            next_opponent_edge_count = 0  # 次の相手が取れる端の数
            next_reverse_my_edge_count = 0  # 次の相手がひっくり返すことができる端の数

            for next_action in next_actionable:
                if next_action == "a1" or next_action == "a8" or next_action == "h1" or next_action == "h8":
                    next_opponent_corner_count += 1
                elif next_action == "a2" or next_action == 'a3' or next_action == 'a4' or next_action == 'a5' or next_action == 'a6' or next_action == 'a7' or \
                    next_action == 'b1' or next_action == 'b8' or next_action == 'c1' or next_action == 'c8' or next_action == 'd1' or next_action == 'd8' or \
                    next_action == 'e1' or next_action == 'e8' or next_action == 'f1' or next_action == 'f8' or next_action == 'g1' or next_action == 'g8' or \
                    next_action == 'h2' or next_action == 'h3' or next_action == 'h4' or next_action == 'h5' or next_action == 'h6' or next_action == 'h7':
                    next_opponent_edge_count += 1
                

                # --- [t+2] ---
                next_next_state, next_next_player_id, next_opponent_reverse_places = self._get_next_state(next_state, next_action, next_player_id)

                reverse_count = 0
                for next_opponent_reverse_place in next_opponent_reverse_places:
                    if next_opponent_reverse_place == "a2" or next_opponent_reverse_place == 'a3' or next_opponent_reverse_place == 'a4' or next_opponent_reverse_place == 'a5' or next_opponent_reverse_place == 'a6' or next_opponent_reverse_place == 'a7' or \
                        next_opponent_reverse_place == 'b1' or next_opponent_reverse_place == 'b8' or next_opponent_reverse_place == 'c1' or next_opponent_reverse_place == 'c8' or next_opponent_reverse_place == 'd1' or next_opponent_reverse_place == 'd8' or \
                        next_opponent_reverse_place == 'e1' or next_opponent_reverse_place == 'e8' or next_opponent_reverse_place == 'f1' or next_opponent_reverse_place == 'f8' or next_opponent_reverse_place == 'g1' or next_opponent_reverse_place == 'g8' or \
                        next_opponent_reverse_place == 'h2' or next_opponent_reverse_place == 'h3' or next_opponent_reverse_place == 'h4' or next_opponent_reverse_place == 'h5' or next_opponent_reverse_place == 'h6' or next_opponent_reverse_place == 'h7':
                        reverse_count += 1
                
                if reverse_count > next_reverse_my_edge_count:
                    next_reverse_my_edge_count = reverse_count

            # 計算する
            evaluate_value = 0
            evaluate_value += (opponent_corner_count - next_opponent_corner_count) * 10000
            evaluate_value += (opponent_edge_count - next_opponent_edge_count) * 100
            evaluate_value += (100 - len(next_actionable))
            if action == "a1" or action == "a8" or action == "h1" or action == "h8":
                evaluate_value += 10000
            elif action == "a2" or action == 'a3' or action == 'a4' or action == 'a5' or action == 'a6' or action == 'a7' or \
                    action == 'b1' or action == 'b8' or action == 'c1' or action == 'c8' or action == 'd1' or action == 'd8' or \
                    action == 'e1' or action == 'e8' or action == 'f1' or action == 'f8' or action == 'g1' or action == 'g8' or \
                    action == 'h2' or action == 'h3' or action == 'h4' or action == 'h5' or action == 'h6' or action == 'h7':
                evaluate_value += 100
            elif action == "b2" and state[0][0] == ".":
                evaluate_value -= 3000
            elif action == "b7" and state[7][0] == ".":
                evaluate_value -= 3000
            elif action == "g2" and state[0][7] == ".":
                evaluate_value -= 3000
            elif action == "g7" and state[7][7] == ".":
                evaluate_value -= 3000
            if state[0][0] == "." and "b2" in my_reverse_places:
                evaluate_value -= 3000
            if state[7][0] == "." and "b7" in my_reverse_places:
                evaluate_value -= 3000
            if state[0][7] == "." and "g2" in my_reverse_places:
                evaluate_value -= 3000
            if state[7][7] == "." and "g7" in my_reverse_places:
                evaluate_value -= 3000
            evaluate_value += reverse_opponent_edge_count * 200
            evaluate_value += (reverse_my_edge_count - next_reverse_my_edge_count) * 200
            if is_bad_musikui:
                evaluate_value -= 1000
            if is_good_musikui:
                evaluate_value += 1000

            # debug
            # if action == "e1":
            #     print("action: ", action)
            #     print("next_actionable: ", next_actionable)
            #     print("evaluate_value: ", evaluate_value)
            #     print("[opponent_corner_count] 現在の相手が取れる角の数: ", opponent_corner_count)
            #     print("[next_opponent_corner_count] 次の相手が取れる角の数: ", next_opponent_corner_count)
            #     print("[opponent_edge_count]: 現在の相手が取れる端の数", opponent_edge_count)
            #     print("[next_opponent_edge_count] 次の相手が取れる端の数: ", next_opponent_edge_count)
            #     print("[reverse_my_edge_count] 現在の相手がひっくり返すことができる端の数: ", reverse_my_edge_count)
            #     print("[next_reverse_my_edge_count] 次の相手がひっくり返すことができる端の数: ", next_reverse_my_edge_count)
            #     print("[reverse_opponent_edge_count]: 現在の自分がひっくり返すことができる端の数", reverse_opponent_edge_count)

            evaluete[action] = evaluate_value

        
        # 選択(一番点数が高いものを選択)
        choice_action = max(evaluete.items(), key=lambda x:x[1])[0]

        # 座標に戻す
        col = ord(choice_action[0]) - 97
        row = int(choice_action[1]) - 1

        result = [row, col]
        print("evaluete: ", evaluete)

        return result