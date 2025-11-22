class Sala:
    def __init__(self, nome, alunos=None, materia=None):
        self.nome = nome
        self.alunos = []
        self.materia = None
        self.pdfs = []

    def __str__(self):
        return f"""Sala: {self.nome}, Capacidade: {self.capacidade},
               Alunos: {len(self.alunos)}, Matéria: {self.materia}"""

    def adicionar_aluno(self, aluno):
