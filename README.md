# test-scoring

## 環境構築
### python関連
* Pythonは3.12以上を推奨
  * 動作確認は3.12
* 仮想環境を作りライブラリをインストール
  * `pip install -r requirements.txt`

### 採点の流れ
1. `pdf2image.py` でスキャンデータを画像化
   * スキャンを画像で行った場合省略可
1. `MarkScan` でマークシートをデータ化
1. スキャンされたcsvを用いて`scoring.py` で採点
1. 記述式がある場合採点して以下の形でcsvにする
   * 学籍番号は下四桁でよい
    ```csv
    学生番号,点数
    1111,3
    4567,5
    3210,2    
    ```
  
1. `add_descriptive_points.py` で記述とマークシートの点数を合算
### MarkScan
* マークシートを読み取るためのアプリ    
  * [https://colorful-class.com/markscan/](https://colorful-class.com/markscan/) 
* .exeなのでmac or linuxの場合はwineを使ってください
* 参考
  * [Arm Mac (M1 Mac) 上で Wine を使ってA5:SQL Mk-2を動作させる方法](https://a5m2.mmatsubara.com/wp/?p=8950)
  * [MacでWindowsアプリを動かす!! - Wineを使ってC-Style動かしてみた](https://note.com/coderdojoginowan/n/n2a6a110cf2a9)

## 各プログラムの説明と使用方法
### pdf2img.py
* スキャンされた生徒の解答pdfを画像に変換するプログラム
* スキャン時点でJPEGであれば使用する必要はない
* 実行するとjpegが格納されたファイルが作られる
* MarkScanで読み込めない場合はコントラストを上げる
#### 実行方法
* `python pdf2img.py [変換するpdfファイルのパス]`
* コントラスト, 画像化時のDPIなどを指定する方法はhelpで確認
  * `python pdf2img.py -h`

### scoring.py
* mark scanから得たcsv, 解答csvのpath, 名簿csvのpath から採点結果を出力するプログラム
#### 実行方法
* `python scoring.py [MarkScanの出力csv] [解答csv] [名簿csv]`
#### 実行(採点)に必要なファイルの形式
* MarkScanの出力csv
  ```csv
  グループ名,日付,時間,通番,設問1,設問2,設問3,設問4,設問5,設問6,設問7,設問8,設問9,設問10,設問11,設問12,設問13,設問14,設問15,設問16,設問17,設問18,設問19,設問20,設問21,設問22,設問23,設問24,設問25,設問26,設問27,設問28,設問29,設問30,設問31,設問32,設問33,設問34,設問35,設問36,設問37,設問38,設問39,設問40,設問41,設問42,設問43,設問44,設問45,設問46,設問47,設問48,設問49,設問50
  ,2024/4/25,9:45:07,1,03,07,10,02,01,04,01,03,03,,01,02,02,03,04,02,02,01,02,04,03,02,03,02,03,,,,,,,,,,,,,,,,,,,,,,,,,
  ,2024/4/25,9:45:07,2,02,07,10,02,10,08,02,02,03,,01,02,02,03,03,02,02,02,02,01,03,01,01,04,03,,,,,,,,,,,,,,,,,,,,,,,,,
  ...省略


  ,【簡易集計結果】
  ,標準集計,集計値,1番目,,,,,6,,1,2,,,19,,2,1,2,,,14,2,5,1,6,4,2,,,,,,,,,,,,,,,,,,,,,,,,,,
  ,標準集計,集計値,2番目,5,,,21,10,,4,4,2,,1,20,15,4,8,17,17,3,19,2,,4,2,16,7,,,,,,,,,,,,,,,,,,,,,,,,,
  ... 省略
  ```
  * 画像読み込みエラーがある行は手動で削除してください
    ```csv
    ,2024/4/18,10:24:18,10,03,07,10,02,02,04,09,08,02,,02,04,04,03,01,04,03,01,04,02,03,03,04,02,04,03,02,01,02,03,,,,,,,,,,,,,,,,,,,,
    ,2024/4/18,10:24:18,13,エラー [13シート目|通算13シート目] : 読み込んだ様式が直前に読み込んだ様式とセクション数が異なります。 <- この行を削除
    <- この行を削除
    画像ファイルを確認してください。<- この行を削除
    ファイル：file_path\013.jpeg,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, <- この行を削除
    ,2024/4/18,10:24:18,14,03,07,10,02,01,04,03,04,02,,01,04,03,03,01|02,03,03,03,04,02,03,02|04,04,01|03,04,03,02,04,01,04,,,,,,,,,,,,,,,,,,,,
    ```
* 解答csv
  * ア,イ,ウ,エ はそれぞれ1~4に自動で置換される 
  ```csv
  問題,解答
  1,ア
  2,イ
  ...省略
  ```
* 名簿csv
  ```
  学生番号,氏名
  01234567,田中 太郎
  76543210,山田 次郎
  ...省略
  ```
### name_search.py
* scoring.py で出力されたフォルダのパスをコマンドライン引数と名前が不一致の生徒の候補をあげるプログラム
* 不一致生徒を列挙するのにレーベンシュタイン距離を利用している
    * [『レーベンシュタイン距離』で2つの文字列の類似度を計算してみた - Qiita](https://qiita.com/shoku-pan/items/befa11396a7c3cc10f6c)
### 実行方法
* `python name_search.py [scoreing.pyから出力されたno_name_student.csvのパス] [scoreing.pyから出力されたno_score_student.csvのパス]`


### add_descriptive_points.py
* 記述の点数とマーク試験の結果を合計するプログラム
#### 実行方法
* `python add_descriptive_points.py [マークシートの結果csv] [記述式の採点結果csv]`
  * マークシートの結果csv
    * scoring.pyで作成された result.csv
    ```csv
      学生番号,氏名
      12345678,田中　太郎,14
      12345679,空白　次郎
      98765431,休田　普
      98765432,関学　三郎,13
    ```
  * 記述式の採点結果csv
    * 記述の採点は手動
    * 学籍番号は下四桁でよい
        ```csv
        学籍番号,点数
        5678,8
        5432,5
        ```