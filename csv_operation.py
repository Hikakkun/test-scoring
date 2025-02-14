import csv


# 二次元配列をcsvに書き込む
def write_array_to_csv(filename, data):
    """
    二次元配列をCSVファイルに書き込む
    -
        Parameters:
            filename: str
                出力するCSVファイルのパス
            data: list[list]
                CSVファイルに書き込む二次元配列
    """
    with open(filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)


# csvを二次元配列に格納する
def read_csv_to_array(
    filename, encode="utf_8", header_read=False, spaces_row_if_it_after_not_read=True
):
    """
    CSVファイルを読み込み、二次元配列に格納する
    -
        Parameters:
            filename: str
                読み込むCSVファイルのパス
            encode: str, optional
                読み込むCSVファイルの文字エンコード (デフォルトは "utf_8")
            header_read: bool, optional
                最初の行をヘッダーとして読み込むかどうか (デフォルトは False)
            spaces_row_if_it_after_not_read: bool, optional
                空白行が出現した時点で読み込みを終了するかどうか (デフォルトは True)
        Returns:
            data: list[list]
                読み込んだCSVファイルの内容を格納した二次元配列
    """
    data = []
    with open(filename, "r", encoding=encode, errors="replace") as csvfile:
        csvreader = csv.reader(csvfile)
        for index, row in enumerate(csvreader):
            if not row and spaces_row_if_it_after_not_read:
                break

            if index == 0 and header_read or index > 0:
                data.append(row)
    return data


if __name__ == "__main__":
    for row in read_csv_to_array("./解答 copy 2.csv", encode="shift_jis"):
        print(row)
