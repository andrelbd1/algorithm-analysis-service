from src.codes import Codes
from src.codes.base import BaseCode

from tests import BaseTestClass

class TestCodes(BaseTestClass):

    @property
    def __codes(self):
        return Codes()
    
    def test_get_codes_null(self):
        with self.assertRaises(NotImplementedError):
            code = self.__codes.get_instance(None)

    def test_get_codes_not_exist(self):
        with self.assertRaises(NotImplementedError):
            code = self.__codes.get_instance("not_exist")

    def test_get_base_code_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseCode().run({})

    def test_get_dijkstra(self):
        code = self.__codes.get_instance("Dijkstra")
        self.assertIsInstance(code, BaseCode)

    def test_get_factorial(self):
        code = self.__codes.get_instance("Factorial")
        self.assertIsInstance(code, BaseCode)
        
    def test_get_fibonacci_sequence(self):
        code = self.__codes.get_instance("Fibonacci sequence")
        self.assertIsInstance(code, BaseCode)

    def test_run_dijkstra(self):
        code = self.__codes.get_instance("Dijkstra")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                     'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'input_type': 'integer',
                         }, 
                     'input_value': '10'}]
        source = 0
        target = 4
        graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                 [4, 0, 8, 0, 0, 0, 0, 11, 0],
                 [0, 8, 0, 7, 0, 4, 0, 0, 2],
                 [0, 0, 7, 0, 9, 14, 0, 0, 0],
                 [0, 0, 0, 9, 0, 10, 0, 0, 0],
                 [0, 0, 4, 14, 10, 0, 2, 0, 0],
                 [0, 0, 0, 0, 0, 2, 0, 1, 6],
                 [8, 11, 0, 0, 0, 0, 1, 0, 7],
                 [0, 0, 2, 0, 0, 0, 6, 7, 0]]
        params = {
            "source": source,
            "target": target,
            "graph": graph
        }
        code.setup(payload)
        res = code.run(params)
        self.assertIsInstance(code, BaseCode)
        self.assertIsInstance(res, int)
        self.assertEqual(res, 21)

    def test_run_factorial(self):
        code = self.__codes.get_instance("Factorial")
        code.setup([])
        res = code.run({"factorial number": 5})
        self.assertIsInstance(code, BaseCode)
        self.assertIsInstance(res, int)
        self.assertEqual(res, 5 * 4 * 3 * 2 * 1)

    def test_run_fibonacci_sequence(self):
        code = self.__codes.get_instance("Fibonacci sequence")
        code.setup([])
        res = code.run({"fibonacci number": 6})
        self.assertIsInstance(code, BaseCode)
        self.assertIsInstance(res, int)
        self.assertEqual(res, 8)
