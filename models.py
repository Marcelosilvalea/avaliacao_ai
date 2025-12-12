from dataclasses import dataclass

@dataclass
class Interacao:
    usuario_input: str
    ia_resposta: str
    categoria: str


class HistoricoInteracoes:
    def __init__(self, limite=50):
        self.interacoes = []
        self.limite = limite

    def adicionar(self, interacao: Interacao):
        self.interacoes.append(interacao)
        if len(self.interacoes) > self.limite:
            self.interacoes.pop(0)

    def obter_todas(self):
        return list(self.interacoes)

    def limpar(self):
        self.interacoes = []

    def total(self):
        return len(self.interacoes)
from dataclasses import dataclass