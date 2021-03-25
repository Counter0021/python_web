# setUp() - установить, запускается до каждого тестового метода
# tearDown() - уничтожить, запускается после каждого тестового метода

import unittest
from shooter import Shooter


class ShooterTest(unittest.TestCase):
    mock_data = []

    # Создаём для всех методов объект класса Shooter
    def setUp(self):
        self.counter = Shooter('Counter')
        print(self.mock_data)
        # Фейк данные
        self.mock_data = [1, 2, 3, 4, 5]

    # Уборка данных из памяти
    def tearDown(self):
        self.mock_data = []

    def test_get_cash(self):
        # counter = Shooter('Counter')
        self.counter.get_cash(500)
        self.assertEqual(self.counter.money, 1500)
        print(self.mock_data)

    def test_greet(self):
        # counter = Shooter('Counter')
        self.assertEqual(self.counter.greet(), 'Hello! How are you?')
        self.counter.money = 50
        self.assertEqual(self.counter.greet(), 'Hello! I need cash!')


if __name__ == '__main__':
    unittest.main()
