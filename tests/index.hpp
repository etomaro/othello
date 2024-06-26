#pragma once
#include <iostream>

using namespace std;

#define hw 8            // ボードの大きさ
#define hw2 64          // ボードのマス数
#define n_board_idx 38  // インデックスの個数 縦横各8x2、斜め11x2
#define n_line 6561     // ボードの1つのインデックスが取りうる値の種類。3^8
#define black 0         // 黒の番号
#define white 1         // 白の番号
#define vacant 2        // 空の番号

// インデックスごとのマスの移動数
const int move_offset[n_board_idx] = {1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7};
// インデックス化するときのマス
const int global_place[n_board_idx][hw] = {
    // 行
    {0, 1, 2, 3, 4, 5, 6, 7},
    {8, 9, 10, 11, 12, 13, 14, 15},
    {16, 17, 18, 19, 20, 21, 22, 23},
    {24, 25, 26, 27, 28, 29, 30, 31},
    {32, 33, 34, 35, 36, 37, 38, 39},
    {40, 41, 42, 43, 44, 45, 46, 47},
    {48, 49, 50, 51, 52, 53, 54, 55},
    {56, 57, 58, 59, 60, 61, 62, 63},
    // 列
    {0, 8, 16, 24, 32, 40, 48, 56},
    {1, 9, 17, 25, 33, 41, 49, 57},
    {2, 10, 18, 26, 34, 42, 50, 58},
    {3, 11, 19, 27, 35, 43, 51, 59},
    {4, 12, 20, 28, 36, 44, 52, 60},
    {5, 13, 21, 29, 37, 45, 53, 61},
    {6, 14, 22, 30, 38, 46, 54, 62},
    {7, 15, 23, 31, 39, 47, 55, 63},
    // 左上から右下にかけての斜め
    {5, 14, 23, -1, -1, -1, -1, -1},
    {4, 13, 22, 31, -1, -1, -1, -1},
    {3, 12, 21, 30, 39, -1, -1, -1},
    {2, 11, 20, 29, 38, 47, -1, -1},
    {1, 10, 19, 28, 37, 46, 55, -1},
    {0, 9, 18, 27, 36, 45, 54, 63},
    {8, 17, 26, 35, 44, 53, 62, -1},
    {16, 25, 34, 43, 52, 61, -1, -1},
    {24, 33, 42, 51, 60, -1, -1, -1},
    {32, 41, 50, 59, -1, -1, -1, -1},
    {40, 49, 58, -1, -1, -1, -1, -1},
    // 右上から左下にかけての斜め
    {2, 9, 16, -1, -1, -1, -1, -1},
    {3, 10, 17, 24, -1, -1, -1, -1},
    {4, 11, 18, 25, 32, -1, -1, -1},
    {5, 12, 19, 26, 33, 40, -1, -1},
    {6, 13, 20, 27, 34, 41, 48, -1},
    {7, 14, 21, 28, 35, 42, 49, 56},
    {15, 22, 29, 36, 43, 50, 57, -1},
    {23, 30, 37, 44, 51, 58, -1, -1},
    {31, 38, 45, 52, 59, -1, -1, -1},
    {39, 46, 53, 60, -1, -1, -1, -1},
    {47, 54, 61, -1, -1, -1, -1, -1}
};
int move_arr[2][n_line][hw][2];     // move_arr[プレイヤー][ボードのインデックス][マスの位置][0: 左 1: 右] = 何マスひっくり返せるか
bool legal_arr[2][n_line][hw];      // legal_arr[プレイヤー][ボードのインデックス][マスの位置] = trueなら合法、falseなら非合法
int flip_arr[2][n_line][hw];        // flip_arr[プレイヤー][ボードのインデックス][マスの位置] = ボードのインデックスのマスの位置をひっくり返した後のインデックス
int put_arr[2][n_line][hw];         // put_arr[プレイヤー][ボードのインデックス][マスの位置] = ボードのインデックスのマスの位置に着手した後のインデックス
int local_place[n_board_idx][hw2];  // local_place[インデックス番号][マスの位置] = そのインデックス番号におけるマスのローカルな位置
int place_included[hw2][4];         // place_included[マスの位置] = そのマスが関わるインデックス番号の配列(3つのインデックスにしか関わらない場合は最後の要素に-1が入る)
int reverse_board[n_line];          // reverse_board[ボードのインデックス] = そのインデックスにおけるボードの前後反転
int pow3[11];                       // pow3[i] = 3^i
int pop_digit[n_line][hw];          // pop_digit[ボードのインデックス][i] = そのインデックスの左からi番目の値(3進数なので0か1か2)
int pop_mid[n_line][hw][hw];        // pop_mid[ボードのインデックス][i][j] = そのインデックスの左からi番目、左からj番目に挟まれる場所の値

// インデックスからボードの1行/列をビットボードで生成する
inline int create_one_color(int idx, const int k) {
    int res = 0;
    for (int i = 0; i < hw; ++i) {
        if (idx % 3 == k) {
            res |= 1 << i;
        }
        idx /= 3;
    }
    return res;
}

// ビットボードにおける着手に使う
inline int trans(const int pt, const int k) {
    if (k == 0)
        return pt << 1;
    else
        return pt >> 1;
}

// ビットボードで1行/列において着手
inline int move_line_half(const int p, const int o, const int place, const int k) {
    int mask;
    int res = 0;
    int pt = 1 << (hw - 1 - place);
    if (pt & p || pt & o)
        return res;
    mask = trans(pt, k);
    while (mask && (mask & o)) {
        ++res;
        mask = trans(mask, k);
        if (mask & p)
            return res;
    }
    return 0;
}

void board_init() {
    int idx, b, w, place, i, j, k, l_place, inc_idx;

    // pow3(3のi乗)の初期化(3^0から3^10まで)
    pow3[0] = 1;
    for (idx = 1; idx < 11; ++idx)
        pow3[idx] = pow3[idx- 1] * 3;
    // そのインデックスの左からi番目の値(3進数なので0か1か2)の初期化
    for (i = 0; i < n_line; ++i){
        for (j = 0; j < hw; ++j)
            pop_digit[i][j] = (i / pow3[hw - 1 - j]) % 3;
    }
    for (i = 0; i < n_line; ++i){
        for (j = 0; j < hw; ++j){
            for (k = 0; k < hw; ++k)
                pop_mid[i][j][k] = (i - i / pow3[j] * pow3[j]) / pow3[k];
        }
    }
    for (idx = 0; idx < n_line; ++idx) {
        b = create_one_color(idx, 0);
        w = create_one_color(idx, 1);
        for (place = 0; place < hw; ++place) {
            reverse_board[idx] *= 3;
            if (1 & (b >> place))
                reverse_board[idx] += 0;
            else if (1 & (w >> place)) 
                reverse_board[idx] += 1;
            else
                reverse_board[idx] += 2;
        }
        for (place = 0; place < hw; ++place) {
            move_arr[black][idx][place][0] = move_line_half(b, w, place, 0);
            move_arr[black][idx][place][1] = move_line_half(b, w, place, 1);
            if (move_arr[black][idx][place][0] || move_arr[black][idx][place][1])
                legal_arr[black][idx][place] = true;
            else
                legal_arr[black][idx][place] = false;
            move_arr[white][idx][place][0] = move_line_half(w, b, place, 0);
            move_arr[white][idx][place][1] = move_line_half(w, b, place, 1);
            if (move_arr[white][idx][place][0] || move_arr[white][idx][place][1])
                legal_arr[white][idx][place] = true;
            else
                legal_arr[white][idx][place] = false;
        }
        for (place = 0; place < hw; ++place) {
            flip_arr[black][idx][place] = idx;
            flip_arr[white][idx][place] = idx;
            put_arr[black][idx][place] = idx;
            put_arr[white][idx][place] = idx;
            if (b & (1 << (hw - 1 - place)))
                flip_arr[white][idx][place] += pow3[hw - 1 - place];
            else if (w & (1 << (hw - 1 - place)))
                flip_arr[black][idx][place] -= pow3[hw - 1 - place];
            else{
                put_arr[black][idx][place] -= pow3[hw - 1 - place] * 2;
                put_arr[white][idx][place] -= pow3[hw - 1 - place];
            }
        }
    }

    // place_includedの初期化(そのマスのかかわっているインデックス番号を記録(マス1つづつ見ていく))
    for (place = 0; place < hw2; ++place){
        inc_idx = 0;
        // インデックス番号を1つづつ見ていく(全部で38個)
        for (idx = 0; idx < n_board_idx; ++idx){
            // 8でループを回す(インデックス番号ごとに8個のマスがかかわっている)
            for (l_place = 0; l_place < hw; ++l_place){
                if (global_place[idx][l_place] == place)
                    place_included[place][inc_idx++] = idx;
            }
        }
        if (inc_idx == 3)
            place_included[place][inc_idx] = -1;
    }

    // local_placeの初期化(global_placeの一つ一つに対してマスの位置を記録)
    for (idx = 0; idx < n_board_idx; ++idx){
        for (place = 0; place < hw2; ++place){
            local_place[idx][place] = -1;
            for (l_place = 0; l_place < hw; ++l_place){
                if (global_place[idx][l_place] == place)
                    local_place[idx][place] = l_place;
            }
        }
    }
    cerr << "board initialized" << endl;
}

class board {
    public:
        int board_idx[n_board_idx]; // インデックス
        int player;                 // 盤面から打つ手番
        int policy;                 // 盤面に至る直前に打った手
        int value;                  // 盤面の仮の評価値(move orderingに使う)
        int n_stones;               // 石数

    public:
        // move orderingでソートするためにオペレータをオーバーロード
        bool operator<(const board& another) const {
            return value > another.value;
        }

        // ハッシュテーブル(unordered_map)で使う同値判定
        bool operator==(const board& another) const {
            if (this->player != another.player)
                return false;
            for (int i = 0; i < hw; ++i) {
                if (this->board_idx[i] != another.board_idx[i])
                    return false;
            }
            return true;
        }

        // ハッシュテーブル(unordered_map)で使う非同値判定
        bool operator!=(const board& another) const {
            return !(this->operator==(another));
        }

        // ハッシュテーブル(unordered_map)に使うハッシュ関数
        struct hash {
            typedef size_t result_type;

            // ハッシュテーブルで使うためのハッシュ関数
            // hash = sum(i=0からi=7)(インデックス[i] * 17^i)
            // 17を使うとやたら性能が良い。
            size_t operator()(const board& b) const {
                return
                    b.board_idx[0] + 
                    b.board_idx[1] * 17 + 
                    b.board_idx[2] * 289 + 
                    b.board_idx[3] * 4913 + 
                    b.board_idx[4] * 83521 + 
                    b.board_idx[5] * 1419857 + 
                    b.board_idx[6] * 24137549 + 
                    b.board_idx[7] * 410338673;
            }
        };


        // ボードのコンソールへの表示
        inline void print() {
            int i, j, tmp;
            string res;
            for (i = 0; i < hw; ++i) {
                tmp = this->board_idx[i];
                res = "";
                for (j = 0; j < hw; ++j) {
                    if (tmp % 3 == 0)
                        res = "X " + res;
                    else if (tmp % 3 == 1)
                        res = "O " + res;
                    else
                        res = ". " + res;
                    tmp /= 3;
                }
                cerr << res << endl;
            }
            cerr << endl;
        }

        // 合法手判定
        inline bool legal(int g_place) {
            bool res = false;
            for (int i = 0; i < 3; ++i)
                res |= legal_arr[this->player][this->board_idx[place_included[g_place][i]]][local_place[place_included[g_place][i]][g_place]];
            if (place_included[g_place][3] != -1)
                res |= legal_arr[this->player][this->board_idx[place_included[g_place][3]]][local_place[place_included[g_place][3]][g_place]];
            return res;
        }

        // 着手
        inline board move(const int g_place) {
            board res;
            for (int i = 0; i < n_board_idx; ++i)
                res.board_idx[i] = this->board_idx[i];
            move_p(&res, g_place, 0);
            move_p(&res, g_place, 1);
            move_p(&res, g_place, 2);
            if (place_included[g_place][3] != -1)
                move_p(&res, g_place, 3);
            for (int i = 0; i < 3; ++i)
                res.board_idx[place_included[g_place][i]] = put_arr[this->player][res.board_idx[place_included[g_place][i]]][local_place[place_included[g_place][i]][g_place]];
            if (place_included[g_place][3] != -1)
                res.board_idx[place_included[g_place][3]] = put_arr[this->player][res.board_idx[place_included[g_place][3]]][local_place[place_included[g_place][3]][g_place]];
            res.player = 1 - this->player;
            res.n_stones = this->n_stones + 1;
            res.policy = g_place;
            return res;
        }

        // インデックス形式から一般的な配列形式に変換
        inline void translate_to_arr(int res[]) {
            int i, j;
            for (i = 0; i < hw; ++i) {
                for (j = 0; j < hw; ++j)
                    res[i * hw + j] = pop_digit[this->board_idx[i]][j];
            }
        }

        // 一般的な配列形式からインデックス形式に変換
        inline void translate_from_arr(const int arr[], int player) {
            int i, j;
            for (i = 0; i < n_board_idx; ++i)
                this->board_idx[i] = n_line - 1;  // 22222222を初期値
            this->n_stones = hw2;  // 石の数64を初期値(hw2=64)
            for (i = 0; i < hw2; ++i) {
                for (j = 0; j < 4; ++j) {
                    if (place_included[i][j] == -1)
                        continue;
                    if (arr[i] == black)
                        this->board_idx[place_included[i][j]] -= 2 * pow3[hw - 1 - local_place[place_included[i][j]][i]];
                    else if (arr[i] == white)
                        this->board_idx[place_included[i][j]] -= pow3[hw - 1 - local_place[place_included[i][j]][i]];
                    else if (j == 0)
                        --this->n_stones;
                }
            }
            this->player = player;
        }

    private:
        // 石をひっくり返す
        inline void flip(board *res, int g_place) {
            for (int i = 0; i < 3; ++i)
                res->board_idx[place_included[g_place][i]] = flip_arr[this->player][res->board_idx[place_included[g_place][i]]][local_place[place_included[g_place][i]][g_place]];
            if (place_included[g_place][3] != -1)
                res->board_idx[place_included[g_place][3]] = flip_arr[this->player][res->board_idx[place_included[g_place][3]]][local_place[place_included[g_place][3]][g_place]];
        }

        // 石をひっくり返す
        inline void move_p(board *res, int g_place, int i) {
            int j, place;
            place = local_place[place_included[g_place][i]][g_place];
            for (j = 1; j <= move_arr[this->player][this->board_idx[place_included[g_place][i]]][place][0]; ++j)
                flip(res, g_place - move_offset[place_included[g_place][i]] * j);
            for (j = 1; j <= move_arr[this->player][this->board_idx[place_included[g_place][i]]][place][1]; ++j)
                flip(res, g_place + move_offset[place_included[g_place][i]] * j);
        }

};