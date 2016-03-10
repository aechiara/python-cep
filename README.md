Build Status: ![alt build](https://circleci.com/gh/aechiara/python-cep.svg?style=shield&circle-token=3218c0a6295dbf94869c7106b2f06a14badc936a)

Busca endereço a partir de um CEP no site dos Correios

```
pip install python-cep

import buscacep

res = buscacep.busca_cep_correios('01310000')

# as dict (and convert to json if needed)
res = buscacep.busca_cep_correios_as_dict('01310000')

```
