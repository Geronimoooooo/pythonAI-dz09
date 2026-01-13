from random import randint
import lotoMenuModul

class Keg:
    __num = None
    def __init__(self):
        self.__num = randint(1, 90)

    @property
    def num(self):
        return self.__num

    def __str__(self):
        return str(self.__num)

class Card:
    __rows = 3
    __cols = 9
    __nums_in_row = 5
    __data = None
    __emptynum = 0
    __crossednum = -1

    def __init__(self, users_numbers=None):
        uniques_count = self.__nums_in_row * self.__rows

        if users_numbers is None:
            self.uniques = lotoMenuModul.generate_unique_numbers(uniques_count, 1, 90)
        else:
            if not isinstance(users_numbers, list):
                raise TypeError("user_numbers must be a list")

            if len(users_numbers) != uniques_count:
                raise ValueError(f"Нужно {uniques_count} чисел")

            if len(set(users_numbers)) != len(users_numbers):
                raise ValueError("Числа должны быть уникальными")

            self.uniques = users_numbers

        self.__data = []
        for i in range(0, self.__rows):
            tmp = sorted(self.uniques[self.__nums_in_row * i: self.__nums_in_row * (i + 1)])
            empty_nums_count = self.__cols - self.__nums_in_row
            for j in range(0, empty_nums_count):
                index = randint(0, len(tmp))
                tmp.insert(index, self.__emptynum)
            self.__data += tmp
    
    def __str__(self):
        delimiter = '--------------------------'
        ret = delimiter + '\n'
        for index, num in enumerate(self.__data):
            if num == self.__emptynum:
                ret += '  '
            elif num == self.__crossednum:
                ret += ' -'
            elif num < 10:
                ret += f' {str(num)}'
            else:
                ret += str(num)

            if (index + 1) % self.__cols == 0:
                ret += '\n'
            else:
                ret += ' '
        return ret + delimiter

    def __contains__(self, item):
        return item in self.__data

    def cross_num(self, num):
        for index, item in enumerate(self.__data):
            if item == num:
                self.__data[index] = self.__crossednum
                return
        raise ValueError(f'Number not in card: {num}')

    def closed(self) -> bool:
        return set(self.__data) == {self.__emptynum, self.__crossednum}
    
class Game:
    __usercard = None
    __user2card = None
    __compcard = None
    __game_regime = None
    __game_level = None
    __numkegs = 90
    __kegs = []
    __gameover = False

    def __init__(self, game_regime=None, user_numbers=None):
        self.__game_regime = game_regime
        self.__usercard = Card(user_numbers)
        self.__user2card = Card(user_numbers)
        self.__compcard = Card(user_numbers)
        self.__kegs = lotoMenuModul.generate_unique_numbers(self.__numkegs, 1, 90)

    def play_round(self) -> int:
        """
        :return:
        if regime comp to user:
        0 - user loses
        1 - user wins
        2 - computer wins
        if regime user to user:
        0 - user 1 loses
        1 - user 1 wins
        3 - user 2 loses
        4 - user 2 wins
        """
        game_regime = self.__game_regime
        if game_regime == '1':
            keg = self.__kegs.pop()
            print(f'Новый бочонок: {keg} (осталось {len(self.__kegs)})')
            print(f'----- Ваша карточка ------\n{self.__usercard}')
            print(f'-- Карточка компьютера ---\n{self.__compcard}')

            useranswer = input('Зачеркнуть цифру? (y/n)').lower().strip()
            if useranswer == 'y' and not keg in self.__usercard or \
               useranswer != 'y' and keg in self.__usercard:
                return 0
            if keg in self.__usercard:
                self.__usercard.cross_num(keg)
                if self.__usercard.closed():
                    return 1
            if keg in self.__compcard:
                self.__compcard.cross_num(keg)
                if self.__compcard.closed():
                    return 2
            print("DEBUG: дошёл до конца play_round")
            return 9

        elif game_regime == '2':
            keg = self.__kegs.pop()
            print(f'Новый бочонок: {keg} (осталось {len(self.__kegs)})')
            print(f'----- Карточка 1 игрока ------\n{self.__usercard}')
            print(f'-- Карточка второго игрока ---\n{self.__user2card}')
            useranswer = input('Зачеркнуть цифру игроку? (y/n)').lower().strip()
            if useranswer == 'y' and not keg in self.__usercard or \
                    useranswer != 'y' and keg in self.__usercard:
                return 3
            if keg in self.__usercard:
                self.__usercard.cross_num(keg)
                if self.__usercard.closed():
                    return 4

            user2answer = input('Зачеркнуть цифру 2-ому игроку? (y/n)').lower().strip()
            if user2answer == 'y' and not keg in self.__user2card or \
                    user2answer != 'y' and keg in self.__user2card:
                return 3
            if keg in self.__user2card:
                self.__user2card.cross_num(keg)
                if self.__user2card.closed():
                    return 4
            print("DEBUG: дошёл до конца play_round")
            return 9