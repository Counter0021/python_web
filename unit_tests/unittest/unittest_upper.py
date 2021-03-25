# Юнит тесты - тестируется кусочек кода
# Тест
import unittest
from upper import upper_text, upper_text_word


class TestUpper(unittest.TestCase):
    def test_one_word(self):
        text = 'hello!'
        result = upper_text(text)
        self.assertEqual(result, 'Hello!')
        self.assertNotEqual(result, 'hello!')

    def test_multiple_words(self):
        text = 'hello world!'
        result = upper_text_word(text)
        self.assertEqual(result, 'Hello World!')


if __name__ == '__main__':
    unittest.main()
