''' split_csv_file
'''

import glob
import csv
from datetime import datetime
import os


def split_csv_file(input_csv_file:str, output_dir:str, target_column_index:int=0) -> None:
    """split_csv_file
    input_csv_fileの、target_column_index(0-base)の列を日付に変換し
    その項目ごとのcsvファイルをoutput_dirへ作成する。
    作成するcsvファイルは、元のinput_csv_fileと同じ形式。(dialectが修正される可能性があるため、CSVモジュールを通さない)
    1行目はすべてのファイルで共通で、列名(input_csv_fileの1行目)。
    
    遅くなることはわかっているが、わかりやすさを優先するため、必要な都度ファイルを開く。
    速度優先・メモリ消費増加を求めたくなったら、ファイルを全部開いたままにし、更新する。

    Args:
        input_csv_file (str): 元のCSVファイル
        output_dir (str): 出力先のフォルダ
        target_column_index (int, optional): 分割するキーとなる列番号.日付型である前提. Defaults to 0.
    """
    # 出力ファイルの準備
    os.makedirs(output_dir, exist_ok=True)
    output_file_base = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(input_csv_file))[0]   # 拡張子を除いたファイル名
    )
    #print(output_file_base)
    
    # この時点で出力ファイルが存在していたら削除する
    # （後でmode='a'で開くので、実行のたびに追記されないように、この時点で削除しておく）
    for file in glob.glob(f'{output_file_base}_*'):
        os.remove(file)
    
    # ファイルを読んで出力
    # 生のファイルを読むファイルポインタと、CSVとして読むポインタを各々開く(もっとスマートな方法がありそう)
    header = ''
    with open(input_csv_file, mode='r', encoding='utf-8') as f:
        with open(input_csv_file, mode='r', encoding='utf-8') as f_forcsv:
            csv_reader = csv.reader(f_forcsv)
            for i, (raw_line, csv_rec) in enumerate(zip(f, csv_reader)):
                if i==0:
                    header = raw_line
                    continue
                
                # 日付列の値を取得
                split_key = csv_rec[target_column_index]
                #print(split_key)
                
                # CSV出力
                output_csv(output_file_base, split_key, header, raw_line)
       
    return


def output_csv(output_file_base:str, split_key:str, header_line:str, raw_line:str) -> None:
    """output_csv
    CSVファイルを出力する

    Args:
        output_file_base (str): 出力ファイルのベース.
        split_key (str): 出力ファイル名を決定する日付の文字列.
        header_line (str): ヘッダー行.
        raw_line (str): 出力する行データ.
    """
    # 文字列を日付に読み替える
    try:
        key_date = datetime.strptime(split_key, '%Y-%m-%d')
        key_str = key_date.strftime('%Y%m%d')   # yyyymmdd（ゼロ埋め）
    except ValueError as e:
        print('ValueError:', e)
        raise e
    
    # 出力ファイル名
    output_file = f'{output_file_base}_{key_str}.csv'
    file_exists = os.path.exists(output_file)
    
    # 出力
    with open(output_file, mode='a', encoding='utf-8') as f:
        # 存在していない場合は、ヘッダー行を書く
        if not file_exists:
            f.write(header_line)
        
        # 出力
        f.write(raw_line)
    
    return


def main():
    input_file = './input/owid-covid-data.csv'
    output_dir = './output'
    
    split_csv_file(input_file, output_dir, 3)


if __name__=='__main__':
    main()