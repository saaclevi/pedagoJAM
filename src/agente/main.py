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
    
    resposta = {"resposta": ""}

    if data["acao"] == "criar_sala":
        resposta["resposta"] = "Sala criada com sucesso"

    elif data["acao"] == "adicionar_aluno":
        # Find the Sala
        sala_encontrada = False
        for s in salas:
            if s.nome == data["sala"]:
                s.adicionar_aluno(data["aluno"])
                sala_encontrada = True
                resposta["resposta"] = f"Aluno adicionado à sala {s.nome}"
                break
        
        if not sala_encontrada:
            resposta["resposta"] = f"Sala {data['sala']} não encontrada"

    elif data["acao"] == "adicionar_pdf":
        # Find the Sala
        sala_encontrada = False
        for s in salas:
            if s.nome == data["sala"]:
                s.adicionar_pdf(data["pdf"])
                sala_encontrada = True
                resposta["resposta"] = f"PDF adicionado à sala {s.nome}"
                break
        
        if not sala_encontrada:
            resposta["resposta"] = f"Sala {data['sala']} não encontrada"
    
    # Output JSON response to stdout
    print(json.dumps(resposta))
