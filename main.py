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