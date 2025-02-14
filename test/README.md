# test
## ファイル説明
* scan.pdf
    * マークシートをスキャンしたデータ
* img
  * `scan.pdf` を `pdf2image.py` で画像化したもの
* ans.csv
  * テストの回答
* name_list.csv
  * 学籍番号と名前
* desc.csv
  * 記述式があった場合の各学生の記述式の点数

## 実行方法
* `python scoring.py ./test/scan.csv ./test/ans.csv ./test/name_list.csv`
  * `result_mmdd_HHMMSS` 内に採点した結果が出力
* `python ./add_descriptive_points.py ./result_mmdd_HHMMSS/result.csv ./test/desc.csv`
  * 記述の点数を加えた結果のcsvを出力