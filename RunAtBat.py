# ライブラリインポート
import JudgeRisp
import Logic


def run_at_bat(pitcher, batter, game_condition):
    
    # 変数


    # 事前処理


    # 得点圏判定
    risp = JudgeRisp.judge_risp(game_condition)

    # 打席結果決定
    game_condition = Logic.logic(pitcher, batter, game_condition, risp)

    # 事後処理
    return game_condition
