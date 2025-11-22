import json


class Sala:
    def __init__(self, nome, alunos=None, materia=None):
        self.nome = nome
        self.alunos = []
        self.materia = None
        self.pdfs = []

    def __str__(self):
        json.dumps({
            "nome": self.nome,
            "alunos": [str(aluno) for aluno in self.alunos],
            "materia": self.materia,
            "pdfs": [str(pdf) for pdf in self.pdfs]
            }, indent=4)

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)

    def adicionar_pdf(self, pdf):
        self.pdfs.append(pdf)
