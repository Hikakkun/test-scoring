class CONSTANT:
    """
    定数を保持するクラス
    Parameters:
    RECOGNITION_FAILURE: str
        マークされていない場合の文字列
    CONVERTING_DICTIONARY: dict{str : str}
        解答を 数字に変換するための辞書
    """

    RECOGNITION_FAILURE = "@"
    CONVERTING_DICTIONARY = {"ア": "1", "イ": "2", "ウ": "3", "エ": "4", "x": "0"}

    class LEN:
        """
        要素の長さを保持する定数
        Parameters:
        STUDENT_NUMBER: int
            生徒の学籍番号の桁数
        PROBLEM: int
            問題数
        """

        STUDENT_NUMBER = 8
        PROBLEM = 40

    class START_INDEX:
        """
        各要素がcsvのどの列から始まっているかを保持する定数
        Parameters:
        STUDENT_NUMBER: int
            生徒の学籍番号の開始列
        PROBLEM: int
            問題解答の開始列
        """

        STUDENT_NUMBER = 4
        PROBLEM = 14


class Student:
    """
    生徒の情報を保持するクラス
    Parameters:
    number: str
        生徒の学籍番号 8桁
    score: int
        生徒の点数 初期値は-1
    answers_list: list
        生徒の回答した番号を保持するリスト
        リストの要素は文字列
    """

    number: str
    score: int
    answers_list: list
    name: str

    def __init__(self, csv_line):
        self.__init_number(csv_line)
        self.__init_answers_list(csv_line)
        self.score = -1
        self.name = "unknown"

    def __init_number(self, csv_line):
        """
        mark scanから取得したcsvから学籍番号を取得する関数

        Parameters:
        csv_list: list
            mark scanから取得したcsvの一行分
        """
        self.number = ""
        for i in range(CONSTANT.LEN.STUDENT_NUMBER):
            index = i + CONSTANT.START_INDEX.STUDENT_NUMBER
            self.number += self.__format(csv_line[index])

    def __init_answers_list(self, csv_line):
        """
        mark scanから取得したcsvから解答を取得する関数

        Parameters:
        csv_list: list
            mark scanから取得したcsvの一行分
        """
        self.answers_list = []
        for i in range(CONSTANT.LEN.PROBLEM):
            index = i + CONSTANT.START_INDEX.PROBLEM
            self.answers_list.append(self.__format(csv_line[index]))

    def __format(self, string):
        """
        長さが2の文字列からは末尾 そうでなければ @ を返す関数
        mark scanから取得したcsvの解答は
            0 にマーク -> 10
            1 にマーク -> 01
            2 にマーク -> 02
        となっているため

        mark scan の初期設定でcsvを取ってきた場合なので設定を変えるとformat関数はいらないかも
        Parameters:
        string: str
            mark scanから取得したcsvの要素
        """
        return string[1] if len(string) == 2 else CONSTANT.RECOGNITION_FAILURE

    def set_score(self, example_answers_list):
        """
        解答の情報が保持されたリストをもとに採点する
        Parameters:
        example_answers_list: list
            解答が保持されているリスト
            問題1 [0]
            問題2 [1] ...
            以上のような形式で保持されている
        """
        self.score = 0
        for index, answer_number in enumerate(example_answers_list):
            if self.answers_list[index] == answer_number:
                self.score += 1
                """  
                if index >= 6:
                    self.score += 2
                else:
                    self.score += 1
                """

    def get_debug_str(self):
        return [self.number, self.name, str(self.score), *self.answers_list]

    def __str__(self) -> str:
        return f"number: {self.number}, name: {self.name}, score: {self.score}"
