def get_season_stats(player):
    """
    その時点での打率、本塁打、打点を計算して文字列で返す
    """
    # エクセルから読み込んだ時点の累積データ
    hits = player.stats.get('hits')
    ab = player.stats.get('ab') # 打数
    hr = player.stats.get('hr')
    rbi = player.stats.get('rbi')

    # 打率の計算（0除算防止）
    if ab > 0:
        avg = hits / ab
    else:
        avg = 0.0
    
    # 表示用に整形（例：.350 12本 45打点）
    return f"{avg:.3f} {hr}本 {rbi}打点"