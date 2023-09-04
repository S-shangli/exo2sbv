# exo2sbv
AviUtlのエキスポートファイルから字幕ファイル(sbv)ファイルを作成するためのコード

* https://github.com/S-shangli/exo2sbv/blob/main/exo2sbv.exe
* https://github.com/S-shangli/exo2sbv/blob/main/exo2sbv.py

## 使い方
* exoファイルをexo2sbvにドラッグアンドドロップして下さい
* exoファイルがあるフォルダにsbvファイルが保存されます
* 保存されるファイル名はexoファイルのものにsbvの拡張子が追加されます
* 面倒なことが嫌いな方はexeファイルを使って下さい
* pythonちょっとわかる人はpyファイルを使うといろいろカスタマイズできます

## 注意点
* 保存先のファイルは警告なしに上書きしようとします

## その他
* Forked from
  * S-shangli/exo2sbv.py
  * S-shangli/exo2srt.py
* Original Gist
  * pandanote-info/exo2srt.py
* exeファイルの作り方 `pyinstaller --onefile exo2sbv.py`
