import random
import BaseAdvancementLogic
import PitcherAbility
import ResultLogic
import SpecialAbility
import UpdateStats

def logic(pitcher, batter, game_condition, is_risp):
    """
    打席の結果を判定し、進塁処理を行い、成績を更新する
    """

    # 投手能力による変動
    meet_corr_p, power_corr_p = PitcherAbility.pitcher_ability(pitcher)

    # 特殊能力による能力変動
    meet_corr_SA, power_corr_SA = SpecialAbility.special_ability(pitcher, batter, is_risp)

    # 能力変動を受けて最終的な能力値決定
    trajectory = batter.trajectory
    meet = batter.meet + meet_corr_p + meet_corr_SA
    power = batter.power + power_corr_p + power_corr_SA
    speed = batter.speed

    # 打席結果決定
    result = ResultLogic.result_logic(trajectory, meet, power, speed)


    old_score = game_condition[4] # 更新前のスコアを保持（打点計算用）

    # 進塁処理
    game_condition = BaseAdvancementLogic.base_advancement_logic(result, game_condition)

    # 今回の打席で発生した得点（＝打点）を計算
    rbi = game_condition[4] - old_score

    # --- 5. 成績(stats)の更新 ---
    UpdateStats.update_stats_b(pitcher, batter, result, is_risp, rbi)
    UpdateStats.update_stats_p(pitcher, batter, result, is_risp, rbi)

    print(f"{batter.name} : {result}")
    
    return game_condition