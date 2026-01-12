import sys
from random import randint
import lotoModul

def menu_loto():
    user_username = input('Прежде чем начнем, как тебя зовут?\n')
    while True:
        print(f'{user_username}, Меню:')
        print('1. Начать игру')
        print('2. Выход')
        user_choice = input('Выбирай пункт:\n')

        if user_choice == '1':
            while True:
                user_regime = input('Как будешь играть?\nС Компьютером или игроком?\nВведи 1, если с компьютером, 2 если с игроком\n')
                if user_regime in ('1', '2'):
                    user_rounds = int(input('Сколько раундов хотите играть?\n'))
                    user_boxes = input('Настроишь сам числа или будем играть по дефолту?\n Введи "default", если по дефолту или "my" если сам\n')
                    if user_boxes == 'my':
                        user_count = int(input('Введи кол-во бочонков'))
                        user_minbound = int(input('Введи мин. границу чисел для бочонков'))
                        user_maxbound = int(input('Введи макс. границу чисел для бочонков'))
                        user_numbers = generate_unique_numbers(user_count, user_minbound, user_maxbound)
                    elif user_boxes == 'default':
                        user_numbers = generate_unique_numbers(15)
                    for round_num in range(user_rounds):
                        game = lotoModul.Game(user_regime, user_numbers)
                        scores = []
                        for _ in range(user_rounds):
                            result = game.play_round()
                            scores.append(result)
                        total = count_scores(scores)
                        print(total)
                    break
                else:
                    print('Ты ввел что-то другое. Попробуй еще раз.')
        elif user_choice == '2':
            sys.exit()
        else:
            print('Неверный пункт меню')


"""def game_level(username):
    print(f'Здравствуй, {username}! Выбери, пожалуйста, уровень сложности для игры:\n')
    while True:
        user_choice = input('1. Легкий \n2. Сложный\n').strip()
        if user_choice == '1':
            return 'easy' 
        elif user_choice == '2':
            return 'hard'
        else:
            print('Вы ввели что-то несвязанное с уровнем сложности, выберите уровень сложности из меню')"""

def generate_unique_numbers(count, minbound=1, maxbound=90):
    if count > maxbound - minbound +1:
        raise ValueError('Кол-во чисел для генерации уникальных чисел слишком большое. Кол-во должно быть меньше, чтобы были только уникальные числа.')
    numbers =[]
    while len(numbers) < count:
        number = randint(minbound, maxbound)
        if number not in numbers:
            numbers.append(number)
    return numbers

def count_scores(scores):
    user1count = scores.count(1)
    user2count = scores.count(4)
    compcount = scores.count(2)
    if user1count and compcount:
        user1_scores = sum(user1count)
        comp_scores = sum(compcount)
        if user1_scores > comp_scores:
            return (f'Баллы игрока 1: {user1_scores}'), (f'Баллы компьютера: {comp_scores}, Игрок победил!')
        else:
            return (f'Баллы игрока 1: {user1_scores}'), (f'Баллы компьютера: {comp_scores}, Компьютер победил!')
    elif user1count and user2count:
        user1_scores = sum(user1count)
        user2_scores = sum(user2count)
        if user1_scores > user2_scores:
            return (f'Баллы игрока 1: {user1_scores}'), (f'Баллы игрока 2: {user2_scores}, Игрок 1 победил!')
        else:
            return (f'Баллы игрока 1: {user1_scores}'), (f'Баллы игрока 2: {user2_scores}, Игрок 2 победил!')