player: プレイヤーファイル
game: オセロゲーム
simulator: プレイ

---コマンド---
・処理の計測時間を調べる
    ・ncalls: 関数の呼び出し回数
    ・tottime: 関数の実行時間（サブルーチンの実行時間は除く）
    ・percall: 関数呼び出し 1 回あたりの実行時間
    ・cumtime: 関数の実行時間（サブルーチンの実行時間も含む）
    ・filename:lineno(function): ファイル名：行数（関数名）
python -m cProfile -s cumtime simulator3.py