import argparse
from csv_operation import read_csv_to_array, write_array_to_csv


def is_student_number_duplicated(name_list):
    """
    学籍番号の重複をチェックする
    学籍番号が8桁であることを確認し、下4桁が重複しているかをチェックする
    -
        Parameters:
            name_list: list[list[str]]
                学籍番号、名前、その他の情報を含むリスト
        Returns:
            bool:
                学籍番号が重複している場合はTrue、それ以外の場合はFalse
    """
    number_set = set()
    for number, name, _ in name_list:
        if len(number) != 8:
            print("学籍番号が8桁ではありません")
            return True
        last_four_digits = number[-4:]
        print(number, last_four_digits, name)
        if last_four_digits in number_set:
            print(f"{last_four_digits} が重複しています")
            return True
        else:
            number_set.add(last_four_digits)

    print("学生番号(下四桁)のダブりはありませんでした")
    return False


def add_descriptive_points(mark_sheet_result_list, description_result_list):
    """
    記述点数をマークシートの結果に追加し、合計点数を計算する
    -
        Parameters:
            mark_sheet_result_list: list[list[str]]
                マークシートの結果を含むリスト
            description_result_list: list[list[str]]
                記述式の採点結果を含むリスト
    """
    digit = 4
    description_result_list.sort(key=lambda x: x[0])
    for last_four_digits, point in description_result_list:
        point = int(point)
        match_number_is_exists = False
        for i in range(len(mark_sheet_result_list)):
            number = mark_sheet_result_list[i][0][-digit:]
            name = mark_sheet_result_list[i][1]
            mark_point = mark_sheet_result_list[i][2]
            if number == last_four_digits:
                match_number_is_exists = True
                mark_sheet_result_list[i][2]
                mark_sheet_result_list[i].append(point)
                if mark_point != "":
                    mark_sheet_result_list[i].append(point + int(mark_point))
                print(
                    f"{mark_sheet_result_list[i][0]} {last_four_digits} {name} {mark_point}+{point}={mark_sheet_result_list[i][2]}"
                )
                break

        if not match_number_is_exists:
            print(f"学籍番号不一致 {last_four_digits} {point}")
    mark_sheet_result_list.insert(
        0, ["学籍番号", "名前", "マーク点数", "記述点数", "合計点数"]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="記述の点数とマーク試験の結果を合計する"
    )
    parser.add_argument("mark_sheet_result_csv_path", help="マークシートの結果csv")
    parser.add_argument("description_result_csv_path", help="記述式の採点結果csv")
    args = parser.parse_args()
    mark_sheet_result_csv_path = args.mark_sheet_result_csv_path
    description_result_csv_path = args.description_result_csv_path

    mark_sheet_result_list = read_csv_to_array(mark_sheet_result_csv_path)
    if not is_student_number_duplicated(mark_sheet_result_list):
        description_result_list = read_csv_to_array(description_result_csv_path)
        add_descriptive_points(mark_sheet_result_list, description_result_list)
        write_array_to_csv("./result.csv", mark_sheet_result_list)
    else:
        print("学生番号を修正してください")
