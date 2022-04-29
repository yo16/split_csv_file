# split_csv_file
csvファイルを、特定の列で分割する。BigQueryのシャード化テーブルを作るための前処理ツール。（もちろんほかの目的にもつかえる）

- 利用したサンプルファイル
  - [owid / covid-19-data](https://github.com/owid/covid-19-data/tree/master/public/data)
    - public/data/latest/owid-covid-latest.csv
    - 2022/4/29時点のデータ。
    - 4列目の`date`を見て、日付ごとにファイルを分割する。

- 処理概要
  - 指定したの列の値を日付型に変換して、その値をもとに`yyyymmdd`のサフィックスをつけたそれぞれのファイルへ出力する。
    - 例: `owid-covid-latest.csv` から `owid-covid-latest_20200101.csv`、`owid-covid-latest_20200102.csv`・・・、`owid-covid-data_20220427.csv`。
    - フォーマットは、`%Y-%m-%d`である前提。
  - 入力ファイルの行の利用において、「csvファイルとして列を解釈する処理」と「ファイルを出力する処理」を独立させる。つまり、解釈し終えたデータ（例えば配列）を整形して出力するのではなく、それとは別に読み込んだ入力情報をそのまま出力する。
    - その場合、処理は複雑になり遅くなりそうだが、使用者にとっては自然であるため。
