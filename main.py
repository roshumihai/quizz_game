import json
import datetime
import time
from database import update_players_table
import caeser

MENU = '''
Hello admin. What whould you like to do?
1. Add question
2. Remove question
3. Play
4. Add player
5. View high scorers
6. Exit
7. Edit questions'''
USER_MENU = '''
Welcome to quiz game!
1.Rules
2.Play
3.View high scorers
4.Quit'''
RULES = '''
You have 12 questions.
Each question come with 4 answer options.
Only one is correct.
Good luck! '''
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def edit_question():
    with open("questions.json", "r") as f:
        file = f.read()
        file = json.loads(file)
    questions = file["questions"]
    for index, question in enumerate(questions):
        print(f"{str(index)}. {question['question']}")
    question_id = input("Choose which question would you like to change> ")
    new_question = input("Edit question> ")
    new_answers = input("Answers> ").split("~")
    correct_answer = input("Corect answer is> ")
    for index, question in enumerate(questions):
        if index == int(question_id):
            question['question'] = new_question
            question['answers'] = new_answers
            question['correctIndex'] = int(correct_answer)
    with open("questions.json", 'w') as f:
        new_json_string = json.dumps(file, indent=4)
        f.write(new_json_string)


def add_question(intrebare, variante, index):
    with open("questions.json", "r+") as f:
        file = json.load(f)
        file["questions"].append({"question": intrebare, "answers": variante, "correctIndex": index})
        f.seek(0)
        f.truncate()
        json.dump(file, f, indent=1)

# def add_question(users):
#     file = read_file(users)
#     question = input("Question: ")
#     answer = input("Variante: ")
#     variante = answer.split(" ")
#     index = int(input("Correct index: "))
#     file["questions"].append({"question": question, "answers": variante, "correctIndex": index})


def read_file(path):
    with open(path, "r") as f:
        try:
            config_dict = f.read()
            config_dict = json.loads(config_dict)
        except Exception as e:
            print(f"error: {e}")
    return config_dict


def del_question(index):
    with open("questions.json", "r") as f:
        file = json.load(f)
    del file["questions"][index]
    with open("questions.json", "w") as f:
        json.dump(file, f, indent=2)


def highscorers():
    high_scores = []

    with open("users.json", "r") as f:
        file = f.read()
        file = json.loads(file)

    for username, values in file.items():
        high_scores.append([username, values["high_score"]])
        high_scores = sorted(high_scores, key=lambda x: x[1], reverse=True)
    print(f"3rd place: {high_scores[2][0]} - {high_scores[2][1]} puncte \n2nd place: {high_scores[1][0]} - {high_scores[1][1]} puncte \n1st place: {high_scores[0][0]} - {high_scores[0][1]} puncte")


def play(users, username):
    while True:
        high_score = users[username]["high_score"]
        score = 0
        with open("questions.json", 'r') as f:
            try:
                file = f.read()
                dict_file = json.loads(file)
            except Exception as e:
                print(f"Error: {e}")

        for questions in dict_file.values():
            for question in questions:
                print(question["question"])

                for num, variante in enumerate(question["answers"]):
                    print(f"{num + 1}. {variante}")
                answer = input("> ")
                if answer.isdigit():
                    answer = int(answer)
                elif answer == "quit":
                    quit()
                if answer == question["correctIndex"]:
                    score += 1
                    if score == 1:
                        print(OKGREEN+"Felicitari raspuns corect! Ai un punct."+ENDC)
                    else:
                        print(OKGREEN + f"Felicitari raspuns corect! Ai {score} puncte" + ENDC)
                elif answer != question["correctIndex"] and question["correctIndex"] == 0:
                    print(FAIL + f'Raspuns gresit! \nRaspunsul corect era: {question["correctIndex"]}. niciuna' + ENDC)
                else:
                    print(
                        FAIL + f'Raspuns gresit! \nRaspunsul corect era: {question["correctIndex"]}. {question["answers"][question["correctIndex"] - 1]} \nAi {score} puncte.' + ENDC)
                print("")
                # time.sleep(2)
        if score > high_score:
            users[username]["high_score"] = score
            json_data = json.dumps(users, indent=4)
            with open("users.json", "w") as f:
                f.write(json_data)
            print(f"New high score: {score}")
            update_players_table(username, score)
        elif score == 1:
            print(f"Felicitari, ai obtinut {score} punct.")
            # time.sleep(2)
        else:
            print(f"Felicitari, ai obtinut {score} puncte.")
            # time.sleep(2)
        play_again = input("Wanna play again? y/n> ")
        while play_again != "n" and play_again != "y":
            play_again = input(f"'{play_again}' not a command. y/n> ")
        if play_again == "n":
            break



def add_player(users):
    username = input("Adauga un nou jucator: ")
    while username in users.keys():
        print("Username already exist!")
        username = input("Adauga un nou jucator: ")
        if username == "exit":
            break
    if username == "exit":
        return
    password = input("Adauga parola: ")
    now = datetime.datetime.now()
    key = now.second % 10
    while key == 0:
        time.sleep(1)
        now = datetime.datetime.now()
        key = now.second % 10
    password = caeser.encrypt(password, key)
    users[username] = {"password": password, "high_score": 0, "date": str(now)}

    with open("users.json", 'w') as f:
        new_json_string = json.dumps(users, indent=4)
        f.write(new_json_string)
    print("Jucatorul a fost adaugat.")
    update_players_table(username, 0)


def check_user_pass(users, username, password):
    key = 0
    if username in users.keys():
        user_obj = users[username]
        if username != "admin":
            user_key = user_obj["date"].split(":")
            user_key = user_key[2].split(".")
            key = int(user_key[0]) % 10
        if password == user_obj["password"]:
            return True
        elif password == caeser.decrypt(user_obj["password"], key):
            return True
        else:
            print("Parola este gresita")
            return False
    else:
        print("Username incorect!")
        return False


if __name__ == "__main__":
    with open("users.json", "r") as f:
        try:
            users = f.read()
            users = json.loads(users)
        except Exception as e:
            print(f"Error: ({e})")

    user = input("Introduceti username: ")
    passwd = input("Introduceti parola: ")

    if check_user_pass(users, user, passwd):
        if user == 'admin':
            while True:
                print(MENU)
                command = input("> ")
                match command:
                    case "1":
                        list_of_answers = []
                        question = input("Inrebare de adaugat: ")
                        answer1 = input("Prima varianta de raspuns: ")
                        list_of_answers.append(answer1)
                        answer2 = input("A doua varianta de raspuns: ")
                        list_of_answers.append(answer2)
                        answer3 = input("A treia varianta de raspuns: ")
                        list_of_answers.append(answer3)
                        answer4 = input("A patra varianta de raspuns: ")
                        list_of_answers.append(answer4)
                        correct_answer = int(input("Varianta corecta de raspuns: "))
                        add_question(question, list_of_answers, correct_answer)
                    case "2":
                        question_to_remove = int(input("A cata intrebare doriti sa o stergeti?> "))
                        del_question(question_to_remove)
                    case "3":
                        play(users, user)
                    case "4":
                        add_player(users)
                    case "5":
                        highscorers()
                    case "6":
                        print("adminul a parasit pagina")
                        break
                    case "7":
                        edit_question()
        else:
            while True:
                print(USER_MENU)
                command = input("> ")
                match command:
                    case "1":
                        print(RULES)
                        time.sleep(2)
                    case "2":
                        play(users, user)
                    case "3":
                        highscorers()
                        time.sleep(2)
                    case "4":
                        quit()
    else:
        print("Authentication failed.")


