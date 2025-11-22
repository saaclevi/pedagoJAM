class PolicyEngine:
    def __init__(self): # Inicializa o motor de políticas
        # Mapeamento simples de ações padrão
        self.default_actions = {
            "saudacao": "action_greet_user",
            "ajuda": "action_show_help",
            "listar_turmas": "action_list_classes",
            "cancelar_acao": "action_cancel_current_flow"
        }

    def decide(self, intent, entities, state):
        """
        Recebe:
        - intent (str): Intenção detectada pelo NLU
        - entities (dict): Dados extraídos (ex: {'nome_turma': 'Math'})
        - state (dict): Estado atual do usuário (memória)
        
        Retorna:
        - action_name (str): O nome da função a ser executada
        """
        
        # ---------------------------------------------------------
        # 1. PRIORIDADE ALTA: INTERACTION STAGE (Fluxos em andamento)
        # Se o bot fez uma pergunta, a resposta do usuário é tratada aqui.
        # ---------------------------------------------------------
        stage = state.get("interaction_stage")

        if stage == "WAITING_CLASS_NAME":
            if intent == "cancelar_acao":
                return "action_cancel_current_flow"
            # Se o usuário mandou qualquer texto, assumimos que é o nome
            return "action_finalize_create_class"

        if stage == "WAITING_STUDENT_INFO":
            if intent == "cancelar_acao":
                return "action_cancel_current_flow"
            return "action_finalize_add_student"

        if stage == "WAITING_ACTIVITY_TITLE":
            return "action_finalize_create_activity"

        # ---------------------------------------------------------
        # 2. FLUXOS DE GESTÃO (Novos Comandos)
        # ---------------------------------------------------------
        
        # --- CENÁRIO: CRIAR TURMA ---
        if intent == "criar_turma":
            # Se o NLU já pegou o nome (Ex: "Criar turma de Artes")
            if entities.get("nome_turma"):
                return "action_create_class_direct" # Cria direto
            else:
                return "action_ask_class_name" # Pergunta o nome

        # --- CENÁRIO: ADICIONAR ALUNO ---
        if intent == "adicionar_aluno":
            # Lógica: Precisamos da Turma E do Aluno
            turma_alvo = entities.get("nome_turma") or state.get("active_class_id")
            nome_aluno = entities.get("nome_aluno")

            if not turma_alvo:
                return "action_ask_class_context" # "Em qual turma?"
            
            if not nome_aluno:
                return "action_ask_student_name" # "Qual o nome do aluno?"
            
            # Temos tudo!
            return "action_add_student_direct"

        # --- CENÁRIO: CRIAR ATIVIDADE ---
        if intent == "criar_atividade":
            turma_alvo = entities.get("nome_turma") or state.get("active_class_id")
            
            if not turma_alvo:
                # O professor quer criar atividade mas não disse onde
                return "action_ask_class_context"
            
            titulo = entities.get("titulo_atividade")
            if titulo:
                return "action_create_activity_direct"
            else:
                return "action_ask_activity_title"

        # ---------------------------------------------------------
        # 3. FLUXOS DE TRACKING (Relatórios)
        # ---------------------------------------------------------

        # --- CENÁRIO: DESEMPENHO DA TURMA ---
        if intent == "ver_desempenho_turma":
            # Tenta pegar a turma da frase OU do contexto (memória)
            turma_alvo = entities.get("nome_turma") or state.get("active_class_id")

            if turma_alvo:
                return "action_show_class_report"
            else:
                # "Ver desempenho de qual turma, professor?"
                return "action_ask_class_context_for_report"

        # --- CENÁRIO: DESEMPENHO DO ALUNO ---
        if intent == "ver_desempenho_aluno":
            aluno_nome = entities.get("nome_aluno")
            turma_alvo = entities.get("nome_turma") or state.get("active_class_id")

            if not aluno_nome:
                return "action_ask_student_name_for_report"
            
            # Aqui é uma regra de negócio: Podemos buscar o aluno em TODAS as turmas
            # ou exigir que uma turma esteja selecionada. Vamos buscar globalmente se turma for nula.
            return "action_show_student_report"

        # ---------------------------------------------------------
        # 4. AÇÕES PADRÃO E FALLBACK
        # ---------------------------------------------------------
        
        # Verifica se a intenção está no dicionário simples
        if intent in self.default_actions:
            return self.default_actions[intent]

        # Se chegou até aqui e não sabemos o que fazer:
        return "action_default_fallback"