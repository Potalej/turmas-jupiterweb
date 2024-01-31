import pandas as pd
import matplotlib.pyplot as plt

class Analise:

  dias_semana = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
  horarios_xticks = [8,10,12,14,16,18,20,22]

  def __init__ (self, arquivo:str)->None:
    self.csv = pd.read_csv(arquivo,skiprows=0,header=1)
    self.hora = pd.read_csv(arquivo,nrows=1,header=None)

  def gerar_lista_horarios (self):
    h_inicio, h_fim = 7, 23
    min_inicio, min_fim = 0, 59
    horas = {}
    for h in range(h_inicio, h_fim+1):
      for m in range(min_inicio, min_fim+1, 10):
        horas[h*60+m] = 0
    return horas

  def horas_por_dia (self):
    # Dicionario de dias e horas
    dias = {dia:dict() for dia in self.dias_semana}
    for dia in dias: dias[dia] = self.gerar_lista_horarios()

    # Percorre as turmas e salva
    for i,turma in self.csv.iterrows():
      h_0, m_0 = [int(x) for x in turma['Inicio'].split(':')]
      h_f, m_f = [int(x) for x in turma['Fim'].split(':')]
      for h in range(h_0, h_f+1):
        for m in range(m_0, m_f+1, 10):
          dias[turma['Dia']][60*h+m] += 1
    
    return dias

  def plota (self, dias:dict):
    # Separa os dicts em listas
    listas_dias = dict()
    fig, axs = plt.subplots(2,3,sharey=True)
    
    ticks_num = [h*60 for h in self.horarios_xticks]
    ticks_lab = ["%02d:00" % h for h in self.horarios_xticks]  

    for num, dia in enumerate(self.dias_semana[:-1]):
      x = [*dias[dia].keys()]
      y = [*dias[dia].values()]
      i,j = num,0
      if num >= 3: i,j = num-3,1
      axs[j,i].set_title(dia)
      axs[j,i].bar(x,y,width=60)
      axs[j,i].set_xticks(ticks_num)
      axs[j,i].set_xticklabels(ticks_lab)

    plt.show()