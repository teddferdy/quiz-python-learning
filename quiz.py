class UserInfo: 
    def __init__(self, name = ""): 
        self.name = name
        self.score = 0

    def reset_score(self):
        self.score = 0

    def add_point(self):
        self.score += 1

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

def getUserName():
    while True:
        input_name = input("Hello What's your name?").strip()
        if len(input_name) == 0:
            print('Please Input Name')
        elif len(input_name) < 3:
            print('Minimum 3 character')
        else:
            return input_name

def askRegister(): 
    while True:
        register = input('Do you want a register? (yes/no)').lower().strip()

        if register in ('yes', 'y'): 
            return True
        elif register in ('no', 'n'):
            return False
        else:
            print('Pilih Jawaban yes / no')

def runQuiz(user):
    user.reset_score()

    for i, q in enumerate(question, start=1):
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


def showResult(user):
    total = len(question)
    print(f"\nHELLO {user.name}, skor kamu: {user.score}/{total}")

def startGame(user):    
    print(f'HELLO {user.name} do you ready to playing?')    


def __main__(): 
    if not askRegister():
        print('Oke Thank you')
        return

    user = UserInfo(getUserName())

    while True:
        runQuiz(user)
        showResult(user)
        again = input('Do You want to play again?').lower().strip()

        if again not in ('yes', 'y'):
            print(f'Oke Bye {user.name}')
            break

if __name__ == "__main__":
    __main__()
    
        
