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
        self.role = data_dict.get('適性')
        self.speed = data_dict.get('球速')
        self.control = data_dict.get('制球')
        self.stamina = data_dict.get('スタミナ')
        self.breaking_ball = data_dict.get('変化球')

    def __repr__(self):
        return f"{self.team} {self.number} {self.name} ({self.role})"
    
class Batter(Player):
    """野手クラス"""
    def __init__(self, data_dict):
        super().__init__(data_dict)
        self.position = data_dict.get('ポジション')
        self.trajectory = data_dict.get('弾道')
        self.meet = data_dict.get('ミート')
        self.power = data_dict.get('パワー')
        self.speed = data_dict.get('走力')
        self.arm = data_dict.get('肩力')
        self.fielding = data_dict.get('守備')
        self.catching = data_dict.get('捕球')

    def __repr__(self):
        return f"{self.team} {self.number} {self.name} ({self.position})"

