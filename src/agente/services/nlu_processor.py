import re
import unicodedata

class NLUProcessor:
    def __init__(self):
        # Definição de padrões (Patterns)
        # Prioridade: Padrões mais específicos primeiro
        self.patterns = [
            # --- GESTÃO DE TURMAS ---
            {
                "intent": "criar_turma",
                "regex": [
                    r"criar (?:uma )?turma (?:de )?(.+)",  # Ex: Criar turma de Matemática
                    r"nova turma (?:de )?(.+)",            # Ex: Nova turma de História
                    r"cadastrar (?:a )?disciplina (.+)"
                ],
                "entity_key": "nome_turma"
            },
            {
                "intent": "listar_turmas",
                "regex": [
                    r"quais (?:são )?(?:as )?minhas turmas",
                    r"listar turmas",
                    r"ver salas"
                ]
            },
            
            # --- GESTÃO DE ALUNOS ---
            {
                "intent": "adicionar_aluno",
                "regex": [
                    r"adicionar (?:o )?aluno (.+) na turma (.+)", # Ex: Adicionar aluno João na turma 3B
                    r"cadastrar (.+) em (.+)",
                    r"novo aluno (.+)" # Contexto implícito (usa active_class_id depois)
                ],
                "entity_keys": ["nome_aluno", "nome_turma"] # Mapeia grupos do regex
            },
            
            # --- GESTÃO DE ATIVIDADES ---
            {
                "intent": "criar_atividade",
                "regex": [
                    r"criar atividade (.+)",
                    r"nova tarefa (.+)",
                    r"agendar prova (?:de )?(.+)"
                ],
                "entity_key": "titulo_atividade"
            },
            
            # --- TRACKING / DESEMPENHO ---
            {
                "intent": "ver_desempenho_turma",
                "regex": [
                    r"como est(?:á|a) a turma(?: de)? ?(.+)?", # O nome da turma é opcional aqui
                    r"ver desempenho(?: da)? ?(.+)?",
                    r"relat(?:ó|o)rio geral"
                ],
                "entity_key": "nome_turma"
            },
             {
                "intent": "ver_desempenho_aluno",
                "regex": [
                    r"notas do aluno (.+)",
                    r"ver nota d(?:o|a) (.+)",
                    r"como est(?:á|a) o (.+)"
                ],
                "entity_key": "nome_aluno"
            }
        ]

    def _normalize_text(self, text):
        """Remove acentos e coloca em minúsculas para facilitar o match."""
        text = text.lower().strip()
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        return text

    def process_message(self, message):
        """
        Entrada: String da mensagem (ex: 'Criar turma de Robótica')
        Saída: Dicionário {'intent': '...', 'entities': {...}, 'confidence': float}
        """
        clean_text = self._normalize_text(message)
        
        # 1. Tenta encontrar via Regex (Rápido e Barato)
        for pattern in self.patterns:
            for regex_str in pattern["regex"]:
                match = re.search(regex_str, clean_text)
                if match:
                    result = {
                        "intent": pattern["intent"],
                        "entities": {},
                        "confidence": 1.0, # Regex é exato
                        "original_text": message
                    }
                    
                    # Extração de Entidades
                    if "entity_key" in pattern and match.groups():
                        # Caso de 1 entidade (ex: nome da turma)
                        # .strip().title() formata para "Matemática" bonitinho
                        result["entities"][pattern["entity_key"]] = match.group(1).strip().title()
                        
                    elif "entity_keys" in pattern and match.groups():
                        # Caso de múltiplas entidades (ex: aluno E turma)
                        groups = match.groups()
                        for i, key in enumerate(pattern["entity_keys"]):
                            if i < len(groups):
                                result["entities"][key] = groups[i].strip().title()
                                
                    return result

        # 2. Se falhar o Regex, retorna Fallback (ou aqui você chamaria o LLM)
        return {
            "intent": "unknown", # O Policy Planner vai lidar com isso
            "entities": {},
            "confidence": 0.0,
            "original_text": message
        }

# --- TESTE RÁPIDO (Para rodar no terminal) ---
if __name__ == "__main__":
    nlu = NLUProcessor()
    
    testes = [
        "Criar turma de Matemática Avançada",
        "Adicionar o aluno Carlos Silva na turma Matemática Avançada",
        "Como está a turma?",
        "Notas do aluno Pedro",
        "Abobrinha frita" # Caso desconhecido
    ]
    
    for t in testes:
        print(f"Input: '{t}'")
        print(f"Output: {nlu.process_message(t)}")
        print("-" * 30)