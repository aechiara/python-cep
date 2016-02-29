#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re

TAG_RE = re.compile(r'<[^>]+>')


class Logradouro:
    header = ('logradouro', 'bairro', 'localidade', 'cep',)

    def __init__(self, args):
        self.logradouro, self.bairro, self.localidade, self.cep = tuple(args)

    def as_dict(self):
        lista = [self.logradouro, self.bairro, self.localidade, self.cep, ]
        return dict(zip(Logradouro.header, lista))

    def __repr__(self):
        return 'Logradouro: {0} - Bairro: {1} - Localidade: {2} - CEP: {3}'.format(self.logradouro, self.bairro, self.localidade, self.cep)


def clean_html(html=None):
    ''' Remove as TAGs HTML '''
    return TAG_RE.sub("", html)


def clean_html_list(html_list=None):
    ''' Retorna uma lista, com cada linha, dos dados sem as TAGs HTML '''
    lista = []
    for i in html_list:
        lista.append(clean_html(str(i)))

    return lista

def get_info(resultado):
    info = []

    for i in resultado.split("\n"):
        if len(i.strip()) > 0:
            info.append(i.strip())

    return Logradouro(info)

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

    texto_clean = clean_html(str(values[1]))
    logradouro = get_info(texto_clean)

    #return logradouro.as_dict()
    return logradouro

def busca_cep_correios_as_dict(cep):
    return busca_cep_correios(cep).as_dict()


