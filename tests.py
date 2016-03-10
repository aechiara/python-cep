# coding: utf-8
import unittest
import buscacep as busca


class TestBuscaCep(unittest.TestCase):
    def setUp(self):
        self.resp = {'bairro': 'Bela Vista', 'cep': '01310-000', 'localidade': 'São Paulo/SP', 'logradouro': 'Avenida Paulista - até 610 - lado par'}

    def test_cep_not_none(self):
        with self.assertRaises(AttributeError):
            busca.busca_cep_correios(None)

    def test_cep_is_digit(self):
        with self.assertRaises(AttributeError):
            busca.busca_cep_correios(12345678)

    def test_cep_match(self):
        self.r = busca.busca_cep_correios('01310000').as_dict()
        self.resultado = set(self.resp.items()) ^ set(self.r.items())
        self.assertEqual(0, len(self.resultado))

if __name__ == '__main__':
    unittest.main()
