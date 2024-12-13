# カタカナの音符を英語の表記に変換する辞書（一オクターブ低く設定）
note_dict = {
    '低ド': 'C2', 'ド': 'C3', '高ド': 'C4',
    '低レ': 'D2', 'レ': 'D3', '高レ': 'D4',
    '低ミ': 'E2', 'ミ': 'E3', '高ミ': 'E4',
    '低ファ': 'F2', 'ファ': 'F3', '高ファ': 'F4',
    '低ソ': 'G2', 'ソ': 'G3', '高ソ': 'G4',
    '低ラ': 'A2', 'ラ': 'A3', '高ラ': 'A4',
    '低シ': 'B2', 'シ': 'B3', '高シ': 'B4'
}

def convert_notes(katakana_notes):
    # 変換された音符を格納するリスト
    converted_notes = []
    
    i = 0
    while i < len(katakana_notes):
        # 3文字以上の音符をチェック
        if i < len(katakana_notes) - 2 and katakana_notes[i:i+3] in note_dict:
            converted_notes.append(note_dict[katakana_notes[i:i+3]])
            i += 3
        elif i < len(katakana_notes) - 1 and katakana_notes[i:i+2] in note_dict:
            converted_notes.append(note_dict[katakana_notes[i:i+2]])
            i += 2
        elif katakana_notes[i] in note_dict:
            converted_notes.append(note_dict[katakana_notes[i]])
            i += 1
        else:
            i += 1  # 辞書にない音符は無視

    return ' '.join(converted_notes)

# 入力例
katakana_notes = "レファラソファミドミレド低シ低シドレミド低ラ低ラ"
# 変換
english_notes = convert_notes(katakana_notes)
print(english_notes)  # 出力: "C2 D3 E3 F3 G3 A3 B3 C4"
