#!/usr/bin/env python3.13
import sys
import json

import sala

# JSON para criar a classe Sala
# {
#     "acao": "criar_sala",
#     "dado": "{
#         "sala": {
#         "ano": String,
#         "alunos": [
#                 { "nome": String,
#                  "cadastro": Integer
#                 }
#             ]
#         "materia": String
#     }"
# }

# Json para executar um comando
# {
#     "acao": "adicionar_aluno",
#     "dado": "{
#        "sala": String,
#        "aluno": {
#            "nome": String,
#            "cadastro": Integer
#        }
#     }"
# }

salas = []

if __name__ == "__main__":
    # Recieve json from stdin
    input_data = sys.stdin.read()
    data = json.loads(input_data)

    if data["acao"] == "criar_sala":
        prompt = "prompt da sla"

    elif data["acao"] == "adicionar_aluno":
        # Find the Sala
        for s in salas:
            if s.nome == data["sala"]:
                s.adicionar_aluno(data["aluno"])
                data["sala"] = s
                break

    elif data["acao"] == "adicionar_pdf":
        # Find the Sala
        for s in salas:
            if s.nome == data["sala"]:
                s.adicionar_pdf(data["pdf"])
                data["sala"] = s
                break
