from bs4 import BeautifulSoup
import requests
from jupiterweb import JupiterWeb
from datetime import datetime

class Base:
  jupiter = JupiterWeb()
  url = "https://uspdigital.usp.br/jupiterweb/jupDisciplinaLista?codcg=$CODCG$&tipo=T"
  
  def html_turmas_instituto (self,codcg:str)->str:
    """
    Captura o HTML da lista de turmas das disciplinas oferecidas em um determinado instituto.
    Retorna uma string com todo o HTML da página do JupiterWeb.
    """
    return requests.get(self.url.replace("$CODCG$",str(codcg))).content
  
  def captura_turmas (self,html:str)->list:
    """
    Captura as turmas a partir do HTML de uma página do JupiterWeb.
    Retorna uma lista com os códigos das turmas.
    """
    soup = BeautifulSoup(html, 'html.parser')
    spans = soup.find_all('span', class_="txt_arial_8pt_gray")
    turmas = [
      span.string.strip()    # Remove os espacos em branco
      for span in spans      # Para cada tag span capturada
      if span.string != None # Se o conteudo não for vazio
    ]
    return turmas

  def salva_turmas_horarios (self,turmas:list,arquivo:str="base.csv")->None:
    """
    Salva as turmas e os respectivos horários em um arquivo .txt, para não precisar fazer o
    scrapy novamente.
    """
    string = f"{datetime.now()}\nDisciplina,Dia,Inicio,Fim\n"
    for i, turma in enumerate(turmas):
      print(f"{turma} ({i+1}/{len(turmas)})")
      disc = self.jupiter.disciplina_codigo(turma) # Captura as infos da turma no JupiterWeb
      for oferecimento in disc.oferecimento:
        for horario in oferecimento['Horários']:
          hora = horario['Horário']
          try:
            dia, inicio, fim = hora.split()
            if dia not in ['seg','ter','qua','qui','sex','sab','dom']: continue
            string += f"{turma},{dia},{inicio},{fim}\n"
          except:
            continue # Sem tratamento pois é um erro da biblioteca jupiterweb
    with open(arquivo, 'w') as arq:
      arq.write(string)