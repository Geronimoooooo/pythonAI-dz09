import sys
from random import randint
import lotoModul

def menu_loto():
    user_username = input('Прежде чем начнем, как тебя зовут?\n')
    while True:
        print(f'{user_username}, выбери пункт меню:')
        print('1. Начать игру')
        print('2. Выход')
        user_choice = input('Впиши пункт сюда:\n')

        if user_choice == '1':
            while True:
                user_regime = int(input('Как будешь играть?\nС Компьютером или игроком?\nВведи 1, если с компьютером, 2 если с игроком\n'))
                if user_regime in (1, 2):
                    user_rounds = int(input('Сколько раундов хотите играть?\n'))
                    user_boxes = input('Настроишь сам числа или будем играть по дефолту?\n Введи "default", если по дефолту или "my" если сам\n')
                    if user_boxes == 'my':
                        user_count = int(input('Введи кол-во бочонков'))
                        user_minbound = int(input('Введи мин. границу чисел для бочонков'))
                        user_maxbound = int(input('Введи макс. границу чисел для бочонков'))
                        user_numbers = generate_unique_numbers(user_count, user_minbound, user_maxbound)
                    elif user_boxes == 'default':
                        user_numbers = generate_unique_numbers(15)
                    game = lotoModul.Game(user_regime, user_numbers)
                    scores = []
                    for i in range(user_rounds):
                        result = game.play_round()
                        scores.append(result)
                        #print(result)
                    #print(scores)
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
    if user1count == user2count or user1count == compcount:
        return "Пока никто не победил. Попробуй еще раз!"
    if user1count and compcount:
        if user1count > compcount:
            return (f'Баллы игрока 1: {user1count}'), (f'Баллы компьютера: {compcount}, Игрок победил!')
        elif user1count == compcount:
            return ('Ничья!')
        else:
            return (f'Баллы игрока 1: {user1count}'), (f'Баллы компьютера: {compcount}, Компьютер победил!')
    elif user1count and user2count:
        if user1count > user2count:
            return (f'Баллы игрока 1: {user1count}'), (f'Баллы игрока 2: {user2count}, Игрок 1 победил!')
        elif user1count == user2count:
            return ('Ничья!')
        else:
            return (f'Баллы игрока 1: {user1count}'), (f'Баллы игрока 2: {user2count}, Игрок 2 победил!')
    return 'Баг, неожиданное состояние'