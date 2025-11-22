#!/usr/bin/env python3.13
import sys
import json

# JSON para criar a classe Sala
# {
#     "acao": "criar_sala",
#     "sala": {
#         "nome": String,
#         "alunos": [
#                 { "nome": String,
#                  "cadastro": Integer
#                 }
#             ]
#         "materia": String
#     }
# }

# Json para executar um comando
# {
#     "acao": "adicionar_aluno",
#     "sala": String,
#     "aluno": {
#         "nome": String,
#         "cadastro": Integer
#     }
# }

# Json para adicionar PDF
# {
#     "sala": String,
#     "pdf": {
#         "nome": String,
#         "url": String
#     }
# }


if __name__ == "__main__":
    # Recieve json from stdin
    input_data = sys.stdin.read()
    data = json.loads(input_data)

    print(json.dumps(data, indent=4))
