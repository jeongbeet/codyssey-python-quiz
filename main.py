import json
import os


class Quiz:
    """개별 퀴즈 문제를 표현하는 클래스"""

    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index: int) -> None:
        """문제와 4개의 선택지를 화면에 출력합니다."""
        print(f"\n[문제 {index}]")
        print(self.question)
        print()
        for idx, choice in enumerate(self.choices, start=1):
            print(f"{idx}. {choice}")
        print()

    def check_answer(self, user_answer: int) -> bool:
        """사용자가 입력한 번호가 정답인지 확인합니다."""
        return self.answer == user_answer

    def to_dict(self) -> dict:
        """JSON 파일 저장을 위해 퀴즈 객체를 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리 데이터를 읽어 Quiz 객체로 변환합니다."""
        question = str(data["question"]).strip()
        choices = [str(c) for c in data["choices"]]
        answer = int(data["answer"])
        if not question or len(choices) != 4 or not (1 <= answer <= 4):
            raise ValueError("유효하지 않은 퀴즈 데이터 형식입니다.")
        return cls(question=question, choices=choices, answer=answer)


def get_default_quizzes() -> list[Quiz]:
    """파이썬 기초 문법 주제의 기본 퀴즈 5개를 생성하여 반환합니다."""
    return [
        Quiz(
            question="Python 언어를 처음 만든 창시자는 누구인가요?",
            choices=["Guido van Rossum", "Elon Musk", "Bill Gates", "James Gosling"],
            answer=1,
        ),
        Quiz(
            question="Python에서 리스트(list)의 맨 끝에 새로운 요소를 추가하는 메서드는?",
            choices=["add()", "append()", "push()", "insert_end()"],
            answer=2,
        ),
        Quiz(
            question="Python 소스 코드 파일의 기본 확장자는 무엇인가요?",
            choices=[".py", ".python", ".pt", ".pyc"],
            answer=1,
        ),
        Quiz(
            question="Python에서 키(Key)와 값(Value)의 쌍으로 데이터를 저장하는 자료형은?",
            choices=["int", "str", "list", "dict"],
            answer=4,
        ),
        Quiz(
            question="Python 클래스에서 객체가 생성될 때 자동으로 호출되는 초기화 메서드는?",
            choices=["__start__", "__main__", "__init__", "__new__"],
            answer=3,
        ),
    ]


class QuizGame:
    """퀴즈 게임 전체 흐름과 데이터를 관리하는 클래스"""

    def __init__(self, file_path: str = "state.json"):
        self.file_path = file_path
        self.quizzes: list[Quiz] = []
        self.best_score: int = 0
        self.best_correct: int = 0
        self.best_total: int = 0
        self.has_played: bool = False
        self.loaded_from_file: bool = False
        self.load_data()

    def load_data(self) -> None:
        """state.json 파일에서 데이터를 불러오고, 없거나 손상된 경우 기본 데이터로 복구합니다."""
        if not os.path.exists(self.file_path):
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.save_data()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict) or "quizzes" not in data or "best_score" not in data:
                raise ValueError("JSON 필수 키가 누락되었습니다.")

            loaded_quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            best_score = int(data["best_score"])
            if best_score < 0:
                raise ValueError("최고 점수는 음수일 수 없습니다.")

            self.quizzes = loaded_quizzes
            self.best_score = best_score
            self.best_correct = int(data.get("best_correct", 0))
            self.best_total = int(data.get("best_total", len(self.quizzes)))
            self.has_played = bool(data.get("has_played", self.best_score > 0))
            self.loaded_from_file = True
        except Exception:
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.best_correct = 0
            self.best_total = len(self.quizzes)
            self.has_played = False
            self.loaded_from_file = False
            self.save_data()

    def save_data(self) -> None:
        """현재 퀴즈 목록과 최고 점수를 state.json 파일에 UTF-8로 저장합니다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "has_played": self.has_played,
        }
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 데이터 저장 중 오류가 발생했습니다: {e}")

    def get_int_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """정수 입력을 받아 앞뒤 공백을 제거하고 범위를 검증합니다."""
        while True:
            raw = input(prompt).strip()
            if not raw:
                print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.\n")
                continue
            try:
                value = int(raw)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.\n")
                continue

            if not (min_val <= value <= max_val):
                print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.\n")
                continue
            return value

    def get_non_empty_text(self, prompt: str) -> str:
        """빈 문자열이 아닌 텍스트 입력을 받을 때까지 반복합니다."""
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("⚠️ 내용을 비워둘 수 없습니다. 다시 입력해 주세요.")

    def display_menu(self, show_loaded_banner: bool = False) -> None:
        """메인 메뉴 화면을 출력합니다."""
        print("\n==========================================")
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("==========================================")
        if show_loaded_banner and self.loaded_from_file:
            print(f"📁 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
            print("==========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("==========================================")

    def play_quiz(self) -> None:
        """등록된 퀴즈를 출제하고 정답 여부와 점수를 계산합니다."""
        if not self.quizzes:
            print("\n⚠️ 출제할 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for idx, quiz in enumerate(self.quizzes, start=1):
            print("------------------------------------------")
            quiz.display(idx)
            user_ans = self.get_int_input("정답 입력: ", 1, 4)
            if quiz.check_answer(user_ans):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다! (정답: {quiz.answer}번)")

        score = round((correct_count / total) * 100)
        print("\n==========================================")
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        self.has_played = True
        if score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total
            print("🎉 새로운 최고 점수입니다!")
        print("==========================================")
        self.save_data()

    def add_quiz(self) -> None:
        """사용자로부터 새로운 퀴즈 정보를 입력받아 등록하고 파일에 저장합니다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.get_non_empty_text("문제를 입력하세요: ")
        choices = []
        for idx in range(1, 5):
            choice = self.get_non_empty_text(f"선택지 {idx}: ")
            choices.append(choice)
        answer = self.get_int_input("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_data()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def show_quizzes(self) -> None:
        """저장된 전체 퀴즈 목록을 출력합니다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("------------------------------------------")
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"[{idx}] {quiz.question}")
        print("------------------------------------------")

    def show_score(self) -> None:
        """역대 최고 점수를 확인합니다."""
        if not self.has_played and self.best_score == 0:
            print("\n📊 아직 퀴즈를 풀이한 기록이 없습니다. 먼저 퀴즈를 풀어보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점 ({self.best_total}문제 중 {self.best_correct}문제 정답)")

    def run(self) -> None:
        """프로그램 메인 루프를 실행합니다."""
        first_turn = True
        try:
            while True:
                self.display_menu(show_loaded_banner=first_turn)
                first_turn = False
                choice = self.get_int_input("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.save_data()
                    print("\n👋 퀴즈 게임을 종료합니다. 감사합니다!")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 프로그램 종료 요청이 감지되었습니다. 데이터를 안전하게 저장하고 종료합니다.")
            self.save_data()


if __name__ == "__main__":
    game = QuizGame()
    game.run()