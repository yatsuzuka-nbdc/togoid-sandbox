# genttl.py 使用方法
入力CSVファイル名は、{csv name}.csvであるとする。
## ttl変換設定ファイル {csv name}_genttl_config.csvの作成 (Mandatory)
## 目的語置換用辞書ファイル {csv name}_genttl_config.jsonの作成 (Optional)
特定の列に含まれる特定の目的語を、csvにあるそのままの文字列ではなくURIなど、別の文字列に置換する場合にはその内容をこのファイルに記述する。列番号は0-origin。
    
    (仕様)
    {
        "{column index}": {
            "word in csv": "corresponding word in ttl", ...
        }
    }
## genttl.py実行
`> python genttl.py`  
`PATH TO INPUT FILE?`  
`{csv name}.csv`