# -*- coding: utf8 -*-
'''
Created on 04.07.2011

@author: Sergey Prokhorov <me@seriyps.ru>
'''
import decimal

units = (
    u'ноль',

    (u'один', u'одна'),
    (u'два', u'две'),

    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

orders = (# plural forms and gender
    #((u'', u'', u''), 'm'), # ((u'рубль', u'рубля', u'рублей'), 'm'), # ((u'копейка', u'копейки', u'копеек'), 'f')
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)


def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = ((rest - prev) % x) * 10 / x
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur - 1])
    return plural, name


def num2text(num, main_units=((u'', u'', u''), 'm')):
    """
    http://ru.wikipedia.org/wiki/Gettext#.D0.9C.D0.BD.D0.BE.D0.B6.D0.B5.D1.81.\
    D1.82.D0.B2.D0.B5.D0.BD.D0.BD.D1.8B.D0.B5_.D1.87.D0.B8.D1.81.D0.BB.D0.B0_2
    """
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip() # ноль

    rest = num
    ord = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest /= 1000
        ord += 1
    name.reverse()
    return ' '.join(name).strip()


def decimal2text(value, places=2,
                 int_units=(('', '', ''), 'm'),
                 exp_units=(('', '', ''), 'm')):
    q = decimal.Decimal(10) ** -places
    integral, exp = str(value.quantize(q)).split('.')
    return u'{} {}'.format(
        num2text(int(integral), int_units),
        num2text(int(exp), exp_units))


import unittest


class TestStrToText(unittest.TestCase):

    def test_units(self):
        self.assertEqual(num2text(0), u'ноль')
        self.assertEqual(num2text(1), u'один')
        self.assertEqual(num2text(9), u'девять')

    def test_gender(self):
        self.assertEqual(num2text(1000), u'одна тысяча')
        self.assertEqual(num2text(2000), u'две тысячи')
        self.assertEqual(num2text(1000000), u'один миллион')
        self.assertEqual(num2text(2000000), u'два миллиона')

    def test_teens(self):
        self.assertEqual(num2text(10), u'десять')
        self.assertEqual(num2text(11), u'одиннадцать')
        self.assertEqual(num2text(19), u'девятнадцать')

    def test_tens(self):
        self.assertEqual(num2text(20), u'двадцать')
        self.assertEqual(num2text(90), u'девяносто')

    def test_hundreeds(self):
        self.assertEqual(num2text(100), u'сто')
        self.assertEqual(num2text(900), u'девятьсот')

    def test_orders(self):
        self.assertEqual(num2text(1000), u'одна тысяча')
        self.assertEqual(num2text(2000), u'две тысячи')
        self.assertEqual(num2text(5000), u'пять тысяч')
        self.assertEqual(num2text(1000000), u'один миллион')
        self.assertEqual(num2text(2000000), u'два миллиона')
        self.assertEqual(num2text(5000000), u'пять миллионов')
        self.assertEqual(num2text(1000000000), u'один миллиард')
        self.assertEqual(num2text(2000000000), u'два миллиарда')
        self.assertEqual(num2text(5000000000), u'пять миллиардов')

    def test_inter_oreders(self):
        self.assertEqual(num2text(1100), u'одна тысяча сто')
        self.assertEqual(num2text(2001), u'две тысячи один')
        self.assertEqual(num2text(5011), u'пять тысяч одиннадцать')
        self.assertEqual(num2text(1002000), u'один миллион две тысячи')
        self.assertEqual(num2text(2020000), u'два миллиона двадцать тысяч')
        self.assertEqual(num2text(5300600), u'пять миллионов триста тысяч шестьсот')
        self.assertEqual(num2text(1002000000), u'один миллиард два миллиона')
        self.assertEqual(num2text(2030000000), u'два миллиарда тридцать миллионов')
        self.assertEqual(num2text(1234567891),
                         u'один миллиард двести тридцать четыре миллиона '
                         u'пятьсот шестьдесят семь тысяч '
                         u'восемьсот девяносто один')

    def test_main_units(self):
        male_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        female_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        self.assertEqual(num2text(101, male_units), u'сто один рубль')
        self.assertEqual(num2text(102, male_units), u'сто два рубля')
        self.assertEqual(num2text(105, male_units), u'сто пять рублей')

        self.assertEqual(num2text(101, female_units), u'сто одна копейка')
        self.assertEqual(num2text(102, female_units), u'сто две копейки')
        self.assertEqual(num2text(105, female_units), u'сто пять копеек')

        self.assertEqual(num2text(0, male_units), u'ноль рублей')
        self.assertEqual(num2text(0, female_units), u'ноль копеек')

        self.assertEqual(num2text(3000, male_units), u'три тысячи рублей')

    def test_decimal2text(self):
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        self.assertEqual(
            decimal2text(
                decimal.Decimal('105.245'),
                int_units=int_units,
                exp_units=exp_units),
            u'сто пять рублей двадцать четыре копейки')
        self.assertEqual(
            decimal2text(
                decimal.Decimal('101.26'),
                int_units=int_units,
                exp_units=exp_units),
            u'сто один рубль двадцать шесть копеек')
        self.assertEqual(
            decimal2text(
                decimal.Decimal('102.2450'),
                places=4,
                int_units=int_units,
                exp_units=exp_units),
            u'сто два рубля две тысячи четыреста пятьдесят копеек')  # xD
        self.assertEqual(
            decimal2text(
                decimal.Decimal('111'),
                int_units=int_units,
                exp_units=exp_units),
            u'сто одиннадцать рублей ноль копеек')
        self.assertEqual(
            decimal2text(
                decimal.Decimal('3000.00'),
                int_units=int_units,
                exp_units=exp_units),
            u'три тысячи рублей ноль копеек')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        try:
            num = sys.argv[1]
            if '.' in num:
                print decimal2text(
                    decimal.Decimal(num),
                    int_units=((u'штука', u'штуки', u'штук'), 'f'),
                    exp_units=((u'кусок', u'куска', u'кусков'), 'f'))
            else:
                print num2text(
                    int(num),
                    main_units=((u'штука', u'штуки', u'штук'), 'f'))
        except ValueError:
            print >> sys.stderr, "Invalid argument {}".format(sys.argv[1])
        sys.exit()
    unittest.main()
