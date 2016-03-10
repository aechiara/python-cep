#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

class Logradouro:
    header = ('logradouro', 'bairro', 'localidade', 'cep',)

    def __init__(self, args):
        self.logradouro, self.bairro, self.localidade, self.cep = tuple(args)

    def as_dict(self):
        lista = [self.logradouro, self.bairro, self.localidade, self.cep, ]
        return dict(zip(Logradouro.header, lista))

    def __repr__(self):
        return 'Logradouro: {0} - Bairro: {1} - Localidade: {2} - CEP: {3}'.format(self.logradouro, self.bairro, self.localidade, self.cep)


def busca_cep_correios(cep):
    ''' Pesquisa o CEP informado no site dos correios '''

    if cep is None or not isinstance(cep, str):
        raise AttributeError("O CEP deve ser do tipo string!")
    elif not cep.isdigit() or len(cep) != 8:
        raise AttributeError("O CEP deve conter apenas 8 dígitos!")

    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'
    payload = {'relaxation': cep, 'tipoCEP': 'ALL', 'semelhante': 'N'}

    resp = requests.post(url, data=payload)

    if resp.status_code != 200:
        raise Exception("Erro acessando site dos correios!", resp.status_code)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")
    value_cells = soup.find('table', attrs={'class': 'tmptabela'})
    values = list(value_cells.findAll('tr'))

    texto_clean = []
    for value in values[1].findAll('td'):
        texto_clean.append(value.get_text().strip())

    logradouro = Logradouro(texto_clean)

    return logradouro

def busca_cep_correios_as_dict(cep):
    return busca_cep_correios(cep).as_dict()


