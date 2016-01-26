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


def busca_cep_correios(cep):
    ''' Pesquisa o CEP informado no site dos correios '''

    if cep is None or not isinstance(cep, str):
        raise AttributeError("O CEP deve ser do tipo string!")
    elif not cep.isdigit() or len(cep) != 8:
        raise AttributeError("O CEP deve conter apenas 8 dígitos!")

    url = 'http://www.buscacep.correios.com.br/servicos/dnec/consultaEnderecoAction.do?&relaxation={0}&TipoCep=ALL&semelhante=N&cfm=1&Metodo=listaLogradouro&TipoConsulta=relaxation&StartRow=1&EndRow=10'.format(cep)

    resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception("Erro acessando site dos correios!", resp.status_code)

    url2 = 'http://www.buscacep.correios.com.br/servicos/dnec/detalheCEPAction.do?&Metodo=detalhe&Posicao=1&TipoCep=2&CEP='

    resp2 = requests.get(url2, cookies=resp.cookies)

    if resp2.status_code != 200:
        raise Exception("Erro acessando site dos correios!", resp.status_code)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp2.text)
    value_cells = soup.findAll('td', attrs={'class': 'value'})

    texto_clean = clean_html_list(value_cells)
    logradouro = Logradouro(texto_clean)

    #return logradouro.as_dict()
    return logradouro

def busca_cep_correios_as_dict(cep):
    return busca_cep_correios(cep).as_dict()

