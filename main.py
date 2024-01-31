from scripts.menu import Menu

def main ():
  print("=====================================")
  print("# Horários das turmas no JupiterWeb #")
  print("=====================================")
  
  M = Menu()
  acao = M.escolha_acao()

  # Caso deseje sair
  if acao == M.acoes[2]: return
  
  # Baixar do JupiterWeb
  elif acao == M.acoes[0]: 
    # Precisa chamar a escolha de instituto
    cod_instituto = M.escolha_instituto()
    # Agora captura os dados
    M.capturar_dados(cod_instituto)
    return

  # Gerar os graficos
  elif acao == M.acoes[1]:
    # Precisa chamar a escolha de instituto
    cod_instituto = M.escolha_instituto_data()
    # Chama a geracao de grafico
    M.gerar_grafico(cod_instituto, True)
    return

if __name__ == "__main__":
  main()