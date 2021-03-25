# Тесты
# python test_tdd.py -v
# Указать все функции(ОК) и вывести документацию
import unittest
from test_driven_development import greet, eat_burgers, can_fly, get_arsenal


class CoolGameFunctionsTest(unittest.TestCase):
    # Приветствие положительному персонажу
    def test_greet(self):
        """
        greet() have to return 'How are you?' if is_enemy == False
        """
        # Равенство
        self.assertEqual(greet('Krost', False), 'Hello Krost! How are you?')

    # Приветствие врагу
    def test_greet_enemy(self):
        self.assertEqual(greet('Acsill', True), 'Hello Acsill! I will kill you, bastard!')

    # Возникает ли ошибка?
    def test_greet_enemy_boolean(self):
        with self.assertRaises(ValueError):
            greet('Ironside', 'XD')

    # Поедание бургеров, когда <= 3
    def test_eat_burgers(self):
        self.assertEqual(eat_burgers(2), 'Mmm! That was excellent!')

    # Поедание бургеров, когда > 3
    def test_eat_burgers_overate(self):
        self.assertEqual(eat_burgers(5), 'Oh! I overate!')

    # Бэтмен умеет летать
    def test_can_fly_batman(self):
        self.assertTrue(can_fly('Batman'), msg='Batman have to be able to fly')

    # Не бэтмен не умеет летать
    def test_can_fly_anyone_else(self):
        self.assertEqual(can_fly('Joker'), False)
        self.assertEqual(can_fly('Acsill'), False)
        self.assertEqual(can_fly('Krost'), False)
        # Лучше так не делать!
        # self.assertFalse(can_fly('Joker'), msg='Batman have to be able to fly')

    # Получить арсенал
    def test_get_arsenal(self):
        self.assertIn(get_arsenal(), ('knife', 'handgun', 'machine gun'))


if __name__ == '__main__':
    unittest.main()
