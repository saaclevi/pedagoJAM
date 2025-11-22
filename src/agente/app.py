from flask import Flask, request, jsonify
from services.nlu_processor import NLUProcessor
from services.policy_engine import PolicyEngine
from services.state_tracker import StateTracker
# Importe sua classe Sala (supondo que você tenha o arquivo sala.py)
# from sala import Sala 

app = Flask(__name__)

# --- PERSISTÊNCIA EM MEMÓRIA (Enquanto o servidor roda) ---
salas_db = []  # Substitui o "salas = []" do main.py
nlu = NLUProcessor()
policy = PolicyEngine()
tracker = StateTracker()

@app.route("/chat", methods=['POST'])
def chat_endpoint():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message', '')

    # 1. Processamento Inteligente (NLU)
    # O NLU descobre que a intenção é "criar_turma" e a entidade é "Matemática"
    nlu_result = nlu.process_message(message)
    current_state = tracker.get_state(user_id)
    
    # 2. Decisão (Policy)
    action = policy.decide(nlu_result['intent'], nlu_result['entities'], current_state)
    
    response_text = ""

    # --- EXECUÇÃO DAS AÇÕES (A lógica do seu main.py entra aqui) ---
    
    if action == "action_finalize_create_class":
        # Lógica de CRIAR SALA
        nome_turma = message # ou nlu_result['entities']['nome_turma']
        
        # Verifica se já existe
        if any(s.nome == nome_turma for s in salas_db):
            response_text = f"A turma {nome_turma} já existe."
        else:
            # nova_sala = Sala(nome=nome_turma)  <-- Seu objeto Sala
            # salas_db.append(nova_sala)         <-- Salva na lista persistente
            salas_db.append({"nome": nome_turma, "alunos": []}) # Exemplo simples
            
            response_text = f"Turma {nome_turma} criada com sucesso!"
            tracker.update_slot(user_id, "active_class_id", nome_turma)
            tracker.clear_flow(user_id)

    elif action == "action_add_student_direct":
        # Lógica de ADICIONAR ALUNO
        aluno_nome = nlu_result['entities'].get('nome_aluno')
        turma_nome = current_state.get('active_class_id') # Pega do contexto "pegajoso"
        
        # Procura a sala na memória
        sala_encontrada = next((s for s in salas_db if s["nome"] == turma_nome), None)
        
        if sala_encontrada:
            sala_encontrada["alunos"].append(aluno_nome)
            response_text = f"Aluno {aluno_nome} adicionado em {turma_nome}."
        else:
            response_text = f"Erro: Não encontrei a turma {turma_nome}."

    # ... (outras ações) ...

    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
