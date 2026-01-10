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

    # （投手）特殊能力による能力変動
    speed_corr, control_corr, breaking_ball_corr = SpecialAbility.special_ability_p(pitcher, batter, is_risp)

    # （野手）特殊能力による能力変動
    meet_corr_SA, power_corr_SA = SpecialAbility.special_ability_b(pitcher, batter, is_risp)

    # 投手能力による変動
    meet_corr_p, power_corr_p = PitcherAbility.pitcher_ability(pitcher, batter, is_risp)

    # 能力変動を受けて最終的な能力値決定
    # 野手能力
    trajectory = batter.trajectory
    meet = batter.meet + meet_corr_p + meet_corr_SA
    power = batter.power + power_corr_p + power_corr_SA
    speed_b = batter.speed
    eye = batter.eye

    # 投手能力
    speed_p = pitcher.speed + speed_corr
    control = pitcher.control + control_corr
    breaking_ball = pitcher.breaking_ball + breaking_ball_corr

    # 打席結果決定
    result = ResultLogic.result_logic(trajectory, meet, power, speed_b, eye, speed_p, control, breaking_ball)


    old_score = game_condition[4] # 更新前のスコアを保持（打点計算用）

    # 進塁処理
    game_condition = BaseAdvancementLogic.base_advancement_logic(result, game_condition)

    # 今回の打席で発生した得点（＝打点）を計算
    rbi = game_condition[4] - old_score

    # --- 5. 成績(stats)の更新 ---
    UpdateStats.update_stats_b(pitcher, batter, result, is_risp, rbi)
    UpdateStats.update_stats_p(pitcher, batter, result, is_risp, rbi)

    # print(f"({batter.position}) {batter.name} : {result}")
    
    return game_condition