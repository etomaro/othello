# 可能なアクションを取得する


def get_actionables(state, player_id):
    """
    args: 
        state: 盤上の状態
            ['...101..', '..0101..', ...]
        player_id: 自分のプレイヤーID(0 or 1)
    
    処理: 
        1. 石が置かれていない場所を取得
        2. 石を置くことができるか判定
        3. game用のstateに直す(col: a-h, row: 1-8)
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
    
    # 3. game用のstateに直す(col: a-h, row: 1-8)
    for idx, actionable in enumerate(actionables):
        row, col = actionable
        col = chr(col + 97)
        row = str(row + 1)
        actionables[idx] = col + row

    
    return actionables


def get_next_state(state, action, player_id):
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
            change_places_all.append([frame_row, frame_col])
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
                        # 値の更新
                        new_row = list(next_state[change_row])
                        new_row[change_col] = player_id
                        next_state[change_row] = "".join(new_row)
                    break
                # 相手の石がある場合は次の座標を更新
                if state[next_row][next_col] == OPPONENT_ID:
                    # 挟める石を追加
                    change_places.append([next_row, next_col])
                    change_places_all.append([next_row, next_col])

                    next_row += vector[0]
                    next_col += vector[1]
                    continue

                # ここには来ないはず
                print("error")


    next_player_id = "0" if player_id == "1" else "1"

    return next_state, next_player_id, change_places_all


# アクションを選択する
def choice(actionable, state, player_id):
    """
    引数
        actionable: 自分の可能なアクション
        state: 現在の状態
        player_id: 自分のプレイヤーID(0 or 1)
    
    処理
        自分がアクション出来るそれぞれの場所に対して、相手がアクション出来る場所を計算
        評価する
          (現在の相手が取れる角の数 - 次の相手が取れる角の数) * 1万点 +
          (現在の相手が取れる端の数 - 次の相手が取れる端の数) * 100点 +
          (100点 - 次の相手の手数)
          自分が角を取れるアクション: 1万点
          自分が端を取れるアクション: 100点
          自分のアクションによってひっくり返した相手の端の数 * (200点) 
          (現在の相手がひっくり返すことができる端の数 - 次の相手がひっくり返すことができる端の数) * 200点



        相手がアクション出来る場所が角、端が減る藻をの選択。次に角、端が増えないものを優先的に選択する(優先度は角 < 端 < それ以外)。角、端がない場合は相手の手数が少ないものを選択する
    """
    OPPONENT_ID = "0" if player_id == "1" else "1"

    # 角がある: 0, 端がある: 1, それ以外: 99-相手の手数
    evaluete = {}

    # 相手の角、端を置ける個数を計算
    opponent_corner_count = 0
    opponent_edge_count = 0
    now_opponet_actionables = get_actionables(state, OPPONENT_ID)
    # 現在相手がひっくり返すことのできる端の数
    now_reverse_my_edge_count = 0
    for action in now_opponet_actionables:
        # 角の場合
        if action == "a1" or action == "a8" or action == "h1" or action == "h8":
            opponent_corner_count += 1
        elif action == "a2" or action == 'a3' or action == 'a4' or action == 'a5' or action == 'a6' or action == 'a7' or \
             action == 'b1' or action == 'b8' or action == 'c1' or action == 'c8' or action == 'd1' or action == 'd8' or \
             action == 'e1' or action == 'e8' or action == 'f1' or action == 'f8' or action == 'g1' or action == 'g8' or \
             action == 'h2' or action == 'h3' or action == 'h4' or action == 'h5' or action == 'h6' or action == 'h7':
            opponent_edge_count += 1
        
        reverse_count = 0
        next_state, next_player_id, opponent_reverse_places = get_next_state(state, action, OPPONENT_ID)
        for opponent_reverse_place in opponent_reverse_places:
            if opponent_reverse_place == "a2" or opponent_reverse_place == 'a3' or opponent_reverse_place == 'a4' or opponent_reverse_place == 'a5' or opponent_reverse_place == 'a6' or opponent_reverse_place == 'a7' or \
                 opponent_reverse_place == 'b1' or opponent_reverse_place == 'b8' or opponent_reverse_place == 'c1' or opponent_reverse_place == 'c8' or opponent_reverse_place == 'd1' or opponent_reverse_place == 'd8' or \
                 opponent_reverse_place == 'e1' or opponent_reverse_place == 'e8' or opponent_reverse_place == 'f1' or opponent_reverse_place == 'f8' or opponent_reverse_place == 'g1' or opponent_reverse_place == 'g8' or \
                 opponent_reverse_place == 'h2' or opponent_reverse_place == 'h3' or opponent_reverse_place == 'h4' or opponent_reverse_place == 'h5' or opponent_reverse_place == 'h6' or opponent_reverse_place == 'h7':
                reverse_count += 1
        
        if reverse_count > now_reverse_my_edge_count:
            now_reverse_my_edge_count = reverse_count

    for action in actionable:
        # アクションをした時の次の状態を取得
        next_state, next_player_id, my_reverse_places = get_next_state(state, action, player_id)

        # ひっくり返すことができる相手の端の数
        reverse_opponent_edge_count = 0
        for my_reverse_place in my_reverse_places:
            if my_reverse_place == "a2" or my_reverse_place == 'a3' or my_reverse_place == 'a4' or my_reverse_place == 'a5' or my_reverse_place == 'a6' or my_reverse_place == 'a7' or \
                 my_reverse_place == 'b1' or my_reverse_place == 'b8' or my_reverse_place == 'c1' or my_reverse_place == 'c8' or my_reverse_place == 'd1' or my_reverse_place == 'd8' or \
                 my_reverse_place == 'e1' or my_reverse_place == 'e8' or my_reverse_place == 'f1' or my_reverse_place == 'f8' or my_reverse_place == 'g1' or my_reverse_place == 'g8' or \
                 my_reverse_place == 'h2' or my_reverse_place == 'h3' or my_reverse_place == 'h4' or my_reverse_place == 'h5' or my_reverse_place == 'h6' or my_reverse_place == 'h7':
                reverse_opponent_edge_count += 1
                
        # 相手がアクション出来る場所を取得
        next_actionable = get_actionables(next_state, next_player_id)

        # 次の相手がひっくり返すことのできる端の数
        next_reverse_my_edge_count = 0
        for next_action in next_actionable:
            reverse_count = 0
            next_next_state, next_next_player_id, next_opponent_reverse_places = get_next_state(next_state, next_action, OPPONENT_ID)
            for next_opponent_reverse_place in next_opponent_reverse_places:
                if next_opponent_reverse_place == "a2" or next_opponent_reverse_place == 'a3' or next_opponent_reverse_place == 'a4' or next_opponent_reverse_place == 'a5' or next_opponent_reverse_place == 'a6' or next_opponent_reverse_place == 'a7' or \
                    next_opponent_reverse_place == 'b1' or next_opponent_reverse_place == 'b8' or next_opponent_reverse_place == 'c1' or next_opponent_reverse_place == 'c8' or next_opponent_reverse_place == 'd1' or next_opponent_reverse_place == 'd8' or \
                    next_opponent_reverse_place == 'e1' or next_opponent_reverse_place == 'e8' or next_opponent_reverse_place == 'f1' or next_opponent_reverse_place == 'f8' or next_opponent_reverse_place == 'g1' or next_opponent_reverse_place == 'g8' or \
                    next_opponent_reverse_place == 'h2' or next_opponent_reverse_place == 'h3' or next_opponent_reverse_place == 'h4' or next_opponent_reverse_place == 'h5' or next_opponent_reverse_place == 'h6' or next_opponent_reverse_place == 'h7':
                    reverse_count += 1
        
            if reverse_count > next_reverse_my_edge_count:
                next_reverse_my_edge_count = reverse_count

        # 次の相手の角、端を置ける個数を計算
        next_opponent_corner_count = 0
        next_opponent_edge_count = 0
        for next_action in next_actionable:
            # 角の場合
            if next_action == "a1" or next_action == "a8" or next_action == "h1" or next_action == "h8":
                next_opponent_corner_count += 1
            elif next_action == "a2" or next_action == 'a3' or next_action == 'a4' or next_action == 'a5' or next_action == 'a6' or next_action == 'a7' or \
                 next_action == 'b1' or next_action == 'b8' or next_action == 'c1' or next_action == 'c8' or next_action == 'd1' or next_action == 'd8' or \
                 next_action == 'e1' or next_action == 'e8' or next_action == 'f1' or next_action == 'f8' or next_action == 'g1' or next_action == 'g8' or \
                 next_action == 'h2' or next_action == 'h3' or next_action == 'h4' or next_action == 'h5' or next_action == 'h6' or next_action == 'h7':
                 
                 next_opponent_edge_count += 1
        
        # 評価する
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
        evaluate_value += reverse_opponent_edge_count * 200
        evaluate_value += (now_reverse_my_edge_count - next_reverse_my_edge_count) * 200

        evaluete[action] = evaluate_value

    
    # 選択(一番点数が高いものを選択)
    choice_action = max(evaluete.items(), key=lambda x:x[1])[0]

    print("evaluete: ", evaluete)

    return choice_action


# テスト
state = ['........', '........', '....10..', '...11101', '..111000', '..011001', '...0.01.', '..00001.']
actionable = ['g2', 'h7', 'b7', 'f2', 'g3', 'b6', 'h3', 'c7', 'e7', 'b8']
player_id = "1"

# # next_state, next_player_id, change_places = get_next_state(state, "g2", player_id)
# # actionable = get_actionables(next_state, next_player_id)
choice_action = choice(actionable, state, player_id)
print("choice_action: ", choice_action)

