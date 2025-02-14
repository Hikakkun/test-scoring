import copy
import argparse
from pathlib import Path
from datetime import datetime
from student import Student, CONSTANT
from csv_operation import read_csv_to_array, write_array_to_csv


def get_answers_list(filename: str, encode: str) -> list:
    """
    解答のリストを取得する関数。
    CSVファイルから解答情報を読み込み、Studentクラスが採点できる形に変換する。

    引数:
        filename (str): 解答CSVファイルのパス
        encode (str): CSVファイルのエンコーディング

    戻り値:
        list: 変換済みの解答リスト
    """
    csv_answer = read_csv_to_array(filename, encode)
    answer_list = []
    for row in csv_answer:
        answer_list.append(CONSTANT.CONVERTING_DICTIONARY[row[1]])
    return answer_list


def get_student_dict(student_answers_data: list, example_answers_list: list) -> dict:
    """
    生徒情報をStudentオブジェクトに保持し、採点を実施する関数。

    引数:
        student_answers_data (list): CSVから読み込んだ生徒解答データのリスト
        example_answers_list (list): 変換済みの解答リスト

    戻り値:
        dict: 学籍番号をキー、Studentオブジェクトを値とする辞書
    """
    student_dict = {}
    for line in student_answers_data:
        student = Student(line)
        student.set_score(example_answers_list)
        student_dict[student.number] = student
    return student_dict


def described_score_to_list(student_dict: dict, name_list_data: list) -> tuple:
    """
    生徒の採点結果を名簿に反映し、必要な情報をリストに整理する関数。

    引数:
        student_dict (dict): 学籍番号をキーとするStudentオブジェクトの辞書
        name_list_data (list): 名簿データのリスト

    戻り値:
        tuple: (採点済みStudentオブジェクトのリスト, 採点未実施生徒のリスト, 名簿と点数を記入したリスト)
    """
    student_list = []
    no_score_student_list = []
    output_data = copy.deepcopy(name_list_data)
    for index in range(len(output_data)):
        output_data[index].append("")

    for index, line in enumerate(name_list_data):
        number = line[0]
        name = line[1]
        # 名簿に学籍番号が存在する場合、student_dictから削除
        if number in student_dict:
            student = student_dict[number]
            if len(output_data[index]) == 2:
                output_data[index].append("")
            output_data[index][2] = student.score
            student.name = name
            student_list.append(student)
            del student_dict[number]
        else:
            no_score_student_list.append([number, name])

    for number, student in student_dict.items():
        output_data.append([number, "", student.score])
        student_list.append(student)
    print(output_data)
    return student_list, no_score_student_list, output_data


def output_scoring_result(
    output_data: list,
    student_list: list,
    no_score_student_list: list,
    student_dict: dict,
) -> None:
    """
    採点結果とデバッグ情報をCSVファイルに出力する関数。

    引数:
        output_data (list): 名簿と点数を記入したリスト
        student_list (list): 採点結果を保持するStudentオブジェクトのリスト
        no_score_student_list (list): 採点が未実施の生徒のリスト
        student_dict (dict): 学籍番号をキーとする未処理のStudentオブジェクトの辞書
    """
    new_dir_path = Path.cwd() / datetime.now().strftime("result_%m%d_%H%M%S")
    new_dir_path.mkdir(exist_ok=True)

    # 提出用CSVの出力
    write_array_to_csv(str(new_dir_path / "result.csv"), output_data)

    debug_output = [["学籍番号", "名前", "点数"]]
    for student in student_list:
        debug_output.append(student.get_debug_str())

    # デバッグ用: 採点済み生徒情報をCSV出力
    write_array_to_csv(str(new_dir_path / "debug.csv"), debug_output)

    # デバッグ用: 採点未実施生徒情報をCSV出力
    write_array_to_csv(
        str(new_dir_path / "no_score_student.csv"), no_score_student_list
    )

    no_name_student = [["学籍番号", "点数"]]
    for number, student in student_dict.items():
        no_name_student.append([number, student.score])

    write_array_to_csv(str(new_dir_path / "no_name_student.csv"), no_name_student)


def main(
    input_csv_path: str,
    answers_csv_path: str,
    name_list_csv_path: str,
    input_csv_encode: str,
    answers_csv_encode: str,
    name_list_csv_encode: str,
) -> None:
    """
    メイン関数。必要なファイルを読み込み、採点を実行し、結果を出力する。

    引数:
        input_csv_path (str): mark scanから得たCSVファイルのパス
        answers_csv_path (str): 解答CSVファイルのパス
        name_list_csv_path (str): 名簿CSVファイルのパス
        input_csv_encode (str): mark scan CSVファイルのエンコーディング
        answers_csv_encode (str): 解答CSVファイルのエンコーディング
        name_list_csv_encode (str): 名簿CSVファイルのエンコーディング
    """
    # 必要なファイルを読み込む
    student_answers_data = read_csv_to_array(input_csv_path, input_csv_encode)
    example_answers_list = get_answers_list(answers_csv_path, answers_csv_encode)
    name_list_data = read_csv_to_array(name_list_csv_path, name_list_csv_encode, True)

    # 全生徒の情報を取得
    student_dict = get_student_dict(student_answers_data, example_answers_list)

    # 名簿の学籍番号をキーとして採点結果を反映
    student_list, no_score_student_list, output_data = described_score_to_list(
        student_dict, name_list_data
    )

    # 採点結果とデバッグ情報の出力
    output_scoring_result(
        output_data, student_list, no_score_student_list, student_dict
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="mark scanから得たCSVを基に採点を実行する"
    )
    parser.add_argument("input_csv_path", help="mark scanから得たCSVのパス")
    parser.add_argument("answers_csv_path", help="解答CSVのパス")
    parser.add_argument("name_list_csv_path", help="名簿CSVのパス")
    parser.add_argument(
        "--input_csv_encode",
        help="mark scan CSVのエンコーディング（指定しない場合は shift_jis）",
    )
    parser.add_argument(
        "--answers_csv_encode",
        help="解答CSVのエンコーディング（指定しない場合は utf_8）",
    )
    parser.add_argument(
        "--name_list_csv_encode",
        help="名簿CSVのエンコーディング（指定しない場合は utf_8）",
    )

    args = parser.parse_args()
    input_csv_path = args.input_csv_path
    answers_csv_path = args.answers_csv_path
    name_list_csv_path = args.name_list_csv_path

    def set_encode(default_encode: str, arg: str) -> str:
        return default_encode if arg is None else arg

    input_csv_encode = set_encode("shift_jis", args.input_csv_encode)
    answers_csv_encode = set_encode("utf_8", args.answers_csv_encode)
    name_list_csv_encode = set_encode("utf_8", args.name_list_csv_encode)

    main(
        input_csv_path,
        answers_csv_path,
        name_list_csv_path,
        input_csv_encode,
        answers_csv_encode,
        name_list_csv_encode,
    )
