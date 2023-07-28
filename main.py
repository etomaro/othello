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
    
    print("empty_places: ", empty_places)
    
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



