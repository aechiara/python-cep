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

    # url = 'https://buscacepinter.correios.com.br/app/endereco/carrega-cep-endereco.php'
    url = 'https://buscacepinter.correios.com.br/app/consulta/html/consulta-detalhes-cep.php'
    payload = {
        'endereco': cep,
        'tipoCEP': 'ALL',
        'cepaux': '',
        'mensagem_alerta': '',
        'pagina': '/app/endereco/index.php',
        'cep': cep,
    }

    resp = requests.post(url, data=payload)

    if resp.status_code != 200:
        raise Exception("Erro acessando site dos correios!", resp.status_code)

    j = resp.json()

    if j.get('erro'):
        return None

    # if j.get('Total') == 0:
    #     return None

    logradouro = Logradouro(
        (
            j.get('dados')[0].get('logradouroDNEC'),
            j.get('dados')[0].get('bairro'),
            j.get('dados')[0].get('localidade'),
            j.get('dados')[0].get('cep')
        )
    )

    return logradouro

def busca_cep_correios_as_dict(cep):
    return busca_cep_correios(cep).as_dict()


