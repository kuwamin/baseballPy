class Player:
    """共通クラス"""
    def __init__(self, data_dict):
        self.team = data_dict.get('所属')
        self.number = data_dict.get('背番号')
        self.name = data_dict.get('名前')
        self.throwing = data_dict.get('投')
        self.batting = data_dict.get('打')

class Pitcher(Player):
    """投手クラス"""
    def __init__(self, data_dict):
        super().__init__(data_dict)
        # --- 基本能力 ---
        self.role = data_dict.get('適性')
        self.speed = data_dict.get('球速')
        self.control = data_dict.get('制球')
        self.stamina = data_dict.get('スタミナ')
        self.breaking_ball = data_dict.get('変化球')

        # --- 特殊能力 ---
        self.clutch_p = data_dict.get('対ピンチ')
        self.vs_left_p = data_dict.get('対左打者')
        self.toughness = data_dict.get('打たれ強さ')
        self.injury_res = data_dict.get('ケガしにくさ')
        self.fastball_life = data_dict.get('ノビ')
        self.quick = data_dict.get('クイック')
        self.recovery = data_dict.get('回復')

        # --- 成績 ---
        self.stats = {
            'games': data_dict.get('登板数', 0),
            'starts': data_dict.get('先発数', 0),
            'wins': data_dict.get('勝利', 0),
            'losses': data_dict.get('敗北', 0),
            'saves': data_dict.get('セーブ', 0),
            'holds': data_dict.get('ホールド', 0),
            'outs_pitched': data_dict.get('投球アウト数', 0),
            'complete_games': data_dict.get('完投', 0),
            'shutouts': data_dict.get('完封', 0),
            'batters_faced': data_dict.get('打者数', 0),
            'strikeouts': data_dict.get('奪三振', 0),
            'walks': data_dict.get('与四球', 0),
            'hit_by_pitch': data_dict.get('与死球', 0),
            'hr_allowed': data_dict.get('被本塁打', 0),
            'hits_allowed': data_dict.get('被安打', 0),
            'runs_allowed': data_dict.get('失点', 0),
            'earned_runs': data_dict.get('自責点', 0),
            'qs': data_dict.get('QS', 0),
            'hqs': data_dict.get('HQS', 0),
            'risp_batters': data_dict.get('得点圏打者数', 0),
            'risp_hits': data_dict.get('得点圏被安打', 0)
        }

    def __repr__(self):
        return f"{self.team} {self.number} {self.name} ({self.role})"
    
class Batter(Player):
    """野手クラス"""
    def __init__(self, data_dict):
        super().__init__(data_dict)
        # --- 基本能力 ---
        self.position = data_dict.get('ポジション')
        self.trajectory = data_dict.get('弾道')
        self.meet = data_dict.get('ミート')
        self.power = data_dict.get('パワー')
        self.speed = data_dict.get('走力')
        self.arm = data_dict.get('肩力')
        self.fielding = data_dict.get('守備')
        self.catching = data_dict.get('捕球')

        # --- 特殊能力 ---
        self.clutch_b = data_dict.get('チャンス')
        self.vs_left_b = data_dict.get('対左投手')
        self.injury_res = data_dict.get('ケガしにくさ')
        self.stealing_res = data_dict.get('盗塁')  # 能力としての盗塁（技術）
        self.base_running = data_dict.get('走塁')
        self.throwing_res = data_dict.get('送球')
        self.recovery = data_dict.get('回復')
        self.eye = data_dict.get('選球眼')

        # --- 成績スタッツ (エクセルからの読み込みに対応) ---
        self.stats = {
            'games': data_dict.get('試合数', 0),
            'pa': data_dict.get('打席', 0),
            'ab': data_dict.get('打数', 0),
            'hits': data_dict.get('安打', 0),
            'singles': data_dict.get('単打', 0),
            'doubles': data_dict.get('二塁打', 0),
            'triples': data_dict.get('三塁打', 0),
            'hr': data_dict.get('本塁打', 0),
            'rbi': data_dict.get('打点', 0),
            'walks': data_dict.get('四球', 0),
            'hbp': data_dict.get('死球', 0),
            'so': data_dict.get('三振', 0),
            'sac_bunt': data_dict.get('犠打', 0),
            'sac_fly': data_dict.get('犠飛', 0),
            'stolen_bases': data_dict.get('盗塁成功', 0), # 成績としての盗塁
            'caught_stealing': data_dict.get('盗塁死', 0),
            'gdp': data_dict.get('併殺打', 0),
            'risp_pa': data_dict.get('得点圏打席', 0),
            'risp_hits': data_dict.get('得点圏安打', 0)
        }

    def __repr__(self):
        return f"{self.team} {self.number} {self.name} ({self.position})"