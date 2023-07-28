import main


def test_get_actionables():
    #  実際の棋譜を基にテスト

    # -- 先攻の場合 --
    PLAYER_ID = "0"

    # 1手目
    state = ['........', '........', '........', '...10...', '...01...', '........', '........', '........']
    expect = ['e6', 'c4', 'd3', 'f5']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 2手目
    state = ['........', '........', '...0....', '...00...', '..111...', '........', '........', '........']
    expect = ['f6', 'd6', 'b6', 'e6', 'c6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 3手目
    state = ['........', '........', '...0....', '...00...', '..101...', '..1.....', '..1.....', '........']
    expect = ['f6', 'b6', 'e6', 'f5', 'b7', 'b5']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 4手目
    state = ['........', '........', '...0.1..', '...01...', '..110...', '..1..0..', '..1.....', '........']
    expect = ['f4', 'd6', 'b6', 'e3', 'b5', 'f5']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 5手目
    state = ['........', '........', '..1111..', '...00...', '..110...', '..1..0..', '..1.....', '........']
    expect = ['d2', 'f2', 'd6', 'b6', 'b2', 'e2', 'g2', 'b7', 'c2', 'b5']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 6手目
    state = ['........', '........', '..1111..', '...01...', '..110...', '..1..0..', '.11.....', '1.......']
    expect = ['d2', 'f2', 'f4', 'd6', 'b6', 'b2', 'e2', 'b5']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 7手目
    state = ['.....1..', '....1...', '..1101..', '...00...', '..110...', '..1..0..', '.11.....', '1.......']
    expect = ['d2', 'd6', 'b6', 'b2', 'g2', 'c2', 'b5', 'e1', 'g3', 'b3']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 8手目
    state = ['...111..', '....1...', '..1101..', '...00...', '..110...', '..1..0..', '.11.....', '1.......']
    expect = ['d2', 'd6', 'b6', 'b2', 'g2', 'c2', 'b5', 'g3', 'b3']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 9手目
    state = ['...111..', '....1...', '..1101..', '..100...', '..110...', '.01..0..', '.11.....', '1.......']
    expect = ['d2', 'd6', 'b4', 'b2', 'g2', 'c2', 'b5', 'g3', 'b3', 'd8', 'b8']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 10手目
    state = ['...111..', '....1...', '..1101..', '..100...', '..110...', '.11..0..', '111.....', '10......']
    expect = ['d2', 'd6', 'b4', 'b2', 'g2', 'c2', 'b5', 'g3', 'b3']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 11手目
    state = ['...111..', '....1...', '..1101..', '..100...', '..100...', '.110.0..', '111.....', '111.....']
    expect = ['d2', 'b4', 'b2', 'g2', 'c2', 'b5', 'b3', 'g3', 'a6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 12手目
    state = ['...111..', '....11..', '..1111..', '..110...', '..100...', '0000.0..', '111.....', '111.....']
    expect = ['g2', 'b4', 'c2', 'd2', 'b5', 'b3', 'b2', 'g1', 'd8']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 13手目
    state = ['...11111', '....10..', '..1101..', '..100...', '..000...', '0000.0..', '111.....', '111.....']
    expect = ['d2', 'b4', 'b2', 'g2', 'c2', 'b3', 'g3', 'd8', 'f4']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 14手目
    state = ['...11111', '....10..', '..1101..', '..100...', '1.000...', '1000.0..', '110.....', '1110....']
    expect = ['d2', 'b4', 'b2', 'g2', 'c2', 'b3', 'g3', 'f4']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 15手目
    state = ['...11111', '...100..', '..1101..', '..110...', '1.010...', '1001.0..', '1111....', '1110....']
    expect = ['g2', 'b4', 'c2', 'b2', 'e7', 'e6', 'e8', 'g3', 'b3', 'c1', 'g4', 'b5', 'f4']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 16手目
    state = ['...11111', '...100..', '..1101..', '.1110...', '1.110...', '1001.0..', '1110....', '11100...']
    expect = ['g2', 'a4', 'c2', 'b5', 'b2', 'e6', 'g3', 'b3', 'c1', 'g4', 'f4']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 17手目
    state = ['...11111', '...1111.', '..1101..', '00000...', '1.110...', '1001.0..', '1110....', '11100...']
    expect = ['b2', 'c2', 'b5', 'e6', 'g3', 'b3', 'c1', 'e7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 18手目
    state = ['.1111111', '...0111.', '..1101..', '00000...', '1.110...', '1001.0..', '1110....', '11100...']
    expect = ['b2', 'c2', 'b5', 'e6', 'g3', 'b3', 'h2', 'e7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 19手目
    state = ['.1111111', '...00000', '..1101..', '00000...', '1.110...', '1001.0..', '1110....', '111111..']
    expect = ['b2', 'c2', 'b5', 'e6', 'g3', 'b3', 'g4', 'f4', 'e7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 20手目
    state = ['.1111111', '.0.00110', '..01011.', '00000...', '1.110...', '1001.0..', '1110....', '111111..']
    expect = ['c2', 'b5', 'e6', 'h3', 'g4', 'e7', 'f4']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 21手目
    state = ['.1111111', '.1.00110', '1.010000', '11000...', '1.110...', '1001.0..', '1110....', '111111..']
    expect = ['c2', 'b5', 'e6', 'a1']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 22手目
    state = ['01111111', '.0.00111', '1.010011', '11000..1', '1.110...', '1001.0..', '1110....', '111111..']
    expect = ['c2', 'b5', 'e6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 23手目
    state = ['01111111', '11111111', '1.000011', '11000..1', '1.110...', '1001.0..', '1110....', '111111..']
    expect = ['b5', 'e6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 24手目
    state = ['01111111', '11111111', '11111111', '11000..1', '10000...', '1001.0..', '1110....', '111111..']
    expect = ['e7', 'e6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 25手目
    state = ['01111111', '11111111', '11111111', '111111.1', '10001...', '100100..', '1110....', '111111..']
    expect = ['f5', 'e7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 26手目
    state = ['01111111', '11111111', '11111111', '111111.1', '100011..', '100010..', '11110...', '111111..']
    expect = ['g5', 'f7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)
    
    # 27手目
    state = ['01111111', '11111111', '11111111', '111111.1', '1000111.', '100001..', '111110..', '111111..']
    expect = ['h5', 'g7', 'g4', 'g6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 28手目
    state = ['01111111', '11111111', '11111111', '11111111', '10000100', '100011..', '111110..', '111111..']
    expect = ['g7', 'g6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 29手目
    state = ['01111111', '11111111', '11111111', '11111111', '10000110', '1000111.', '1111110.', '111111..']
    expect = ['g8', 'h6']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 30手目
    state = ['01111111', '11111111', '11111111', '11111111', '10000111', '10000111', '1111101.', '1111110.']
    expect = ['h8', 'h7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)


    # -- 後攻の場合 --
    PLAYER_ID = "1"
    
    # 1手目
    state = ['........', '........', '...0....', '...00...', '...01...', '........', '........', '........']
    expect = ['e3', 'c5', 'c3']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 2手目
    state = ['........', '........', '...000..', '...00...', '...01...', '........', '........', '........']
    expect = ['e2', 'c5', 'c3']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 3手目
    state = ['........', '........', '...000..', '...00...', '..101...', '..0.....', '........', '........']
    expect = ['e2', 'c3', 'f2', 'c7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 4手目
    state = ['........', '........', '..1000..', '...00...', '..001...', '.00.....', '........', '........']
    expect = ['e2', 'b5', 'g3']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

    # 5手目
    state = ['........', '........', '..1000..', '...00...', '.1110...', '.00..0..', '........', '........']
    expect = ['d2', 'g2', 'f5', 'b7', 'f2', 'c7', 'a7', 'g3', 'g7', 'd7']
    result = main.get_actionables(state, PLAYER_ID)
    assert set(result) == set(expect)

