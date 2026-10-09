from dataclasses import dataclass
from quiz.opsi import Opsi

@dataclass
class Question:
    text: str
    options: list[str]
    answer: Opsi

    def check(self, jawab: str) -> bool:
        return jawab.lower().strip() == self.answer.value

@dataclass
class ChoiceQuestion(Question):
    def ask(self, nomor: int) -> bool:
        print(f"\n{nomor}. {self.text}")
        for opt in self.options:
            print(f"   {opt}")
        while True:
            jawab = input("Input jawabannya? (a/b/c/d) ").lower().strip()
            if jawab in ("a", "b", "c", "d"):
                break
            print("Input cuma a/b/c/d")
        ok = self.check(jawab)
        if ok:
            print("Jawaban anda benar +1")
        else:
            print(f"Salah, jawaban benar: {self.answer.value}")
        return ok
