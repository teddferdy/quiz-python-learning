import json
import random
from dataclasses import dataclass
from pathlib import Path

from quiz.oop_quiz import ChoiceQuestion
from quiz.opsi import Opsi

DATA_FILE = Path("quiz_data.json")

QUESTIONS = [
    ChoiceQuestion(
        text="Apa output dari print(2 ** 3)?",
        options=["a. 6", "b. 8", "c. 9", "d. 16"],
        answer=Opsi.B,
    ),
    ChoiceQuestion(
        text="Tipe data apa hasil dari len('halo')?",
        options=["a. str", "b. list", "c. int", "d. bool"],
        answer=Opsi.C,
    ),
    ChoiceQuestion(
        text="Keyword apa untuk bikin fungsi di Python?",
        options=["a. func", "b. def", "c. function", "d. lambda()"],
        answer=Opsi.B,
    ),
    ChoiceQuestion(
        text="Apa guna if __name__ == '__main__': ?",
        options=[
            "a. Biar file cuma jalan saat dieksekusi langsung",
            "b. Biar error hilang",
            "c. Biar loop berhenti",
            "d. Biar class ke-import",
        ],
        answer=Opsi.A,
    ),
]


@dataclass
class UserInfo:
    name: str = ""
    score: int = 0
    best_score: int = 0

    def reset_score(self):
        self.score = 0

    def add_point(self):
        self.score += 1

    def update_best(self):
        if self.score > self.best_score:
            self.best_score = self.score

    def save(self):
        data = {}
        if DATA_FILE.exists():
            try:
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = {}
        data[self.name] = self.best_score
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, name: str) -> "UserInfo":
        user = cls(name)
        if DATA_FILE.exists():
            try:
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                user.best_score = int(data.get(name, 0))
            except (json.JSONDecodeError, ValueError, AttributeError):
                pass
        return user


def get_user_name() -> str:
    while True:
        input_name = input("Hello, what's your name? ").strip()
        if len(input_name) == 0:
            print("Please input name")
        elif len(input_name) < 3:
            print("Minimum 3 characters")
        else:
            return input_name


def ask_yes_no(prompt: str) -> bool:
    while True:
        input_ask = input(prompt).lower().strip()
        if input_ask in ("yes", "y"):
            return True
        elif input_ask in ("no", "n"):
            return False
        else:
            print("Pilih jawaban yes/no")


def run_quiz(user: UserInfo) -> None:
    user.reset_score()
    soal = QUESTIONS[:]
    random.shuffle(soal)

    for i, q in enumerate(soal, start=1):
        if q.ask(i):
            user.add_point()


def show_result(user: UserInfo) -> None:
    total = len(QUESTIONS)
    print(f"\nHELLO {user.name}, skor: {user.score}/{total} | terbaik: {user.best_score}/{total}")
    if user.score == total:
        print("Sempurna! GG")
    elif user.score >= total // 2 + 1:
        print("Bagus, dikit lagi sempurna!")
    else:
        print("Belajar lagi yuk!")


def main() -> None:
    if not ask_yes_no("Do you want to register? (yes/no) "):
        print("Oke thank you")
        return

    user = UserInfo.load(get_user_name())

    while True:
        run_quiz(user)
        user.update_best()
        user.save()
        show_result(user)

        if not ask_yes_no("Main lagi? (yes/no): "):
            print(f"Oke bye {user.name}!")
            break


if __name__ == "__main__":
    main()