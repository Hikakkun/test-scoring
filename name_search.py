import argparse
from pathlib import Path
import Levenshtein
from csv_operation import read_csv_to_array


def compute_similarity(
    no_name_student_list: list[list[str]], no_score_student_list: list[list[str]]
) -> list[str]:
    """
    no_name_student_listとno_score_student_listの間で、Levenshtein距離に基づく類似度を計算する関数。

    Args:
        no_name_student_list (list[list[str]]): no_name_student.csv の [number, score] ペアのリスト。
        no_score_student_list (list[list[str]]): no_score_student.csv の [comp_number, name] ペアのリスト。

    Returns:
        list[str]: 類似度の計算結果を含む文字列のリスト。
    """
    output_str_list: list[str] = []
    for row in no_name_student_list:
        number, score = row  # score は計算には使用しない
        similarity_list: list[list[str]] = []
        for comp_row in no_score_student_list:
            comp_number, name = comp_row
            levenshtein_distance = Levenshtein.distance(number, comp_number)
            similarity_list.append([comp_number, name, str(levenshtein_distance)])
        similarity_list.sort(key=lambda x: x[1])  # 名前順にソート
        output_str_list.append(f"{number}との類似度")
        for student_data in similarity_list:
            similarity_data = ",".join(student_data)
            output_str_list.append(similarity_data)
        output_str_list.append("------------")
    return output_str_list


def main() -> None:
    parser = argparse.ArgumentParser(
        description="scoreringで出力されたcsvから名前無しの生徒の候補を上げる Levenshtein距離を採用"
    )
    parser.add_argument(
        "no_name_student_csv", help="no_name_student.csv のファイルパス"
    )
    parser.add_argument(
        "no_score_student_csv", help="no_score_student.csv のファイルパス"
    )

    args = parser.parse_args()
    no_name_path = Path(args.no_name_student_csv)
    no_score_path = Path(args.no_score_student_csv)

    # CSVファイルを読み込む
    no_name_student_list = read_csv_to_array(no_name_path)
    no_score_student_list = read_csv_to_array(no_score_path)

    # 類似度を計算する
    output_str_list = compute_similarity(no_name_student_list, no_score_student_list)

    # 結果を標準出力に表示する
    for row in output_str_list:
        print(row)

    # 計算結果を "name_similarity.txt" に保存する
    output_file = no_name_path.parent / "name_similarity.txt"
    with open(output_file, mode="w", encoding="utf-8") as f:
        f.write("\n".join(output_str_list))


if __name__ == "__main__":
    main()
