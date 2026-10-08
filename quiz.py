import random

question = [
    {
        "question": "Apa output dari print(2 ** 3)?",
        "options": ["a. 6", "b. 8", "c. 9", "d. 16"],
        "answer": "b",
    },
    {
        "question": "Tipe data apa hasil dari len('halo')?",
        "options": ["a. str", "b. list", "c. int", "d. bool"],
        "answer": "c",
    },
    {
        "question": "Keyword apa untuk bikin fungsi di Python?",
        "options": ["a. func", "b. def", "c. function", "d. lambda()"],
        "answer": "b",
    },
    {
        "question": "Apa guna if __name__ == '__main__': ?",
        "options": [
            "a. Biar file cuma jalan saat dieksekusi langsung",
            "b. Biar error hilang",
            "c. Biar loop berhenti",
            "d. Biar class ke-import",
        ],
        "answer": "a",
    },
]
class UserInfo: 
    def __init__(self, name = ""): 
        self.name = name
        self.score = 0
        self.best_score = 0

    def reset_score(self):
        self.score = 0

    def add_point(self):
        self.score += 1

    def update_best(self):
        if self.score > self.best_score:
            self.best_score = self.score


def getUserName() -> str:
    while True:
        input_name = input("Hello What's your name?").strip()
        if len(input_name) == 0:
            print('Please Input Name')
        elif len(input_name) < 3:
            print('Minimum 3 character')
        else:
            return input_name

def askRegister() -> bool: 
    while True:
        register = input('Do you want a register? (yes/no)').lower().strip()

        if register in ('yes', 'y'): 
            return True
        elif register in ('no', 'n'):
            return False
        else:
            print('Pilih Jawaban yes / no')

def runQuiz(user: UserInfo) -> None:
    user.reset_score()
    soal = question[:]
    random.shuffle(soal)

    for i, q in enumerate(soal, start=1):
        print(f"\n{i}. {q['question']}")
        for opt in q["options"]:
            print(f"   {opt}")
        while True:
            jawab = input("Input Jawabanya? (a/b/c/d)").lower().strip()
            if jawab in ('a', 'b', 'c', 'd'): 
                break
        if jawab == q['answer']:
            print('Jawaban anda benar')
            user.add_point()
        else: 
            print(f"Salah, jawaban benar: {q['answer']}")


def showResult(user: UserInfo) -> None:
    total = len(question)
    user.update_best()
    print(f"\nHELLO {user.name}, skor: {user.score}/{total} | terbaik: {user.best_score}/{total}")
    if user.score == total:
        print("Sempurna! GG")
    elif user.score >= total // 2 + 1:
        print("Bagus, dikit lagi sempurna!")
    else:
        print("Belajar lagi yuk!")


def startGame(user: UserInfo) -> None:    
    print(f'HELLO {user.name} do you ready to playing?')    


def __main__() -> None: 
    if not askRegister():
        print('Oke Thank you')
        return

    user = UserInfo(getUserName())

    while True:
        runQuiz(user)
        showResult(user)
        lagi = input("Main lagi? (yes/no): ").lower().strip()
        if lagi not in ("yes", "y", "no", "n"):
            print("Anggap selesai ya")
            break
        if lagi in ("no", "n"):
            print(f"Oke bye {user.name}!")
            break


if __name__ == "__main__":
    __main__()
