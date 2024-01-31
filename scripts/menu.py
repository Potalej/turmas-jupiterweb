from PyInquirer import prompt
from os import listdir
from scripts.analise import Analise
from scripts.base import Base

class Menu:

  institutos_padrao = {
    '21': 'IO',
    '43': 'IF',
    '44': 'IGc',
    '45': 'IME',
  }
  acoes = [
    'Baixar turmas do JupiterWeb',
    'Gerar os graficos',
    'Sair'
  ]
  dir_padrao = "./data/"

  def escolha_acao (self)->str:
    """
    Escolhe entre baixar os dados e fazer os gráficos.
    """
    pergunta = {
      'type': 'list',
      'name': 'escolha_acao',
      'message': 'Escolha o que fazer:',
      'choices': self.acoes
    }
    indice = prompt(pergunta).get("escolha_acao")
    return indice

  def escolha_instituto (self)->str:
    """
    Escolhe qual instituto fazer o que escolheu.
    """
    institutos = [f"{cod} - {self.institutos_padrao[cod]}" for cod in self.institutos_padrao]
    pergunta = {
      'type': 'list',
      'name': 'escolha_instituto',
      'message': 'Escolha o instituto em questão:',
      'choices': institutos
    }
    indice = prompt(pergunta).get("escolha_instituto")
    return indice.split(' ')[0]

  def listar_institutos_capturados (self)->dict:
    arquivos = listdir(self.dir_padrao)
    institutos = dict()
    for arquivo in arquivos:
      cod = arquivo.replace('base_','').replace('.csv','')
      institutos[cod]=self.institutos_padrao[cod]
    return institutos

  def escolha_instituto_data (self)->str:
    """
    Escolhe um instituto dentre os quais já tiveram a base baixada.
    """
    institutos = self.listar_institutos_capturados()
    pergunta = {
      'type': 'list',
      'name': 'escolha_instituto_data',
      'message': 'Escolha o instituto em questão:',
      'choices': [f"{cod} - {institutos[cod]}" for cod in institutos]
    }
    indice = prompt(pergunta).get("escolha_instituto_data")
    return indice.split(' ')[0]

  def gerar_grafico (self, cod:str, hora_captura:bool=False):
    """
    Gera um gráfico a partir dos dados obtidos.
    """
    arq = Analise(f"{self.dir_padrao}base_{cod}.csv")
    if hora_captura: print(f'Base capturada em: {arq.hora}')
    # Captura as horas
    dias = arq.horas_por_dia()
    # Gera os graficos
    arq.plota(dias)

  def capturar_dados (self, cod:str):
    """
    Captura os dados do JupiterWeb.
    """
    base = Base()
    html = base.html_turmas_instituto(cod)
    turmas = base.captura_turmas(html)
    base.salva_turmas_horarios(turmas, f"{self.dir_padrao}base_{cod}.csv")
