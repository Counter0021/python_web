# Тесты
# python test_tdd.py -v
# Указать все функции(ОК) и вывести документацию
import unittest
from test_driven_development import greet, eat_burgers


class CoolGameFunctionsTest(unittest.TestCase):
    def test_greet(self):
        """
        greet() have to return 'How are you?' if is_enemy == False
        """
        # Равенство
        self.assertEqual(greet('Krost', False), 'Hello Krost! How are you?')

    def test_greet_enemy(self):
        self.assertEqual(greet('Acsill', True), 'Hello Acsill! I will kill you, bastard!')

    def test_eat_burgers(self):
        self.assertEqual(eat_burgers(2), 'Mmm! That was excellent!')

    def test_eat_burgers_overate(self):
        self.assertEqual(eat_burgers(5), 'Oh! I overate!')


if __name__ == '__main__':
    unittest.main()
