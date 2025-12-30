# テストコード
def test(batters):
    positions = ['捕', '一', '二', '三', '遊', '左', '中', '右', '指']
    starter_batter = [] # (ポジション名, 選手オブジェクト) のタプルを入れるリスト
    
    candidates = batters[:]

    for pos in positions:
        selected_player = None
        
        for p in candidates:
            if pos == '指' or p.position == pos:
                selected_player = p
                break
        
        if selected_player:
            starter_batter.append((pos, selected_player))
            candidates.remove(selected_player)
        else:
            if candidates:
                selected_player = candidates.pop(0)
                starter_batter.append((pos, selected_player))
                print(f"注意: {pos} の適任者がいないため {selected_player.name} を配置しました")

    return starter_batter 
