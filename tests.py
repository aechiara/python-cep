# coding: utf-8
import unittest
# from unittest.mock import MagicMock
import buscacep as busca


class TestBuscaCep(unittest.TestCase):
    def setUp(self):
        pass
        # self.resp = {'bairro': 'Bela Vista', 'cep': '01310-000', 'localidade': 'São Paulo/SP', 'logradouro': 'Avenida Paulista - até 610 - lado par'}

    def test_cep_not_none(self):
        with self.assertRaises(AttributeError):
            busca.busca_cep_correios(None)

    def test_cep_is_digit(self):
        with self.assertRaises(AttributeError):
            busca.busca_cep_correios(12345678)


if __name__ == '__main__':
    unittest.main()
