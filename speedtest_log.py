import os
import pandas as pd
import time
import speedtest
from datetime import datetime

def verficar_internet(repeticoes, intervalo):
    arquivo = 'dados.csv'

    if os.path.isfile(arquivo):
        df = pd.read_csv(arquivo)
    else:
        dados = {'Horário': [],
                 'Download': [],
                 'Upload': []}
        df = pd.DataFrame(dados, columns=['Horário', 'Download', 'Upload'])

    st = speedtest.Speedtest()

    for n in range(1, repeticoes + 1):
        if n > 1:
            time.sleep(intervalo*3600)
            
        print(f'----- Executando o {n}º teste -----')
        horario = datetime.now().strftime('%d-%m-%Y %H:%M')
        print('Data:', horario)
        download = st.download()*(10**-6)
        print('Velocidade de Download:', round(download, 2))
        upload = st.upload()*(10**-6)
        print('Velocidade de Upload:', round(upload, 2))

        novos_dados = {'Horário': horario,
                       'Download': round(download, 4),
                       'Upload': round(upload, 4)}
        df = df.append(novos_dados, ignore_index=True)
        df.to_csv(arquivo, index=False)

    resultado = df.tail(repeticoes).reset_index(drop=True)
    resultado.index += 1

    return resultado

if __name__ == '__main__':

    vezes = int(input('Informe a quantidade de testes: '))
    tempo = float(input('Informe o intervalo de tempo em horas: '))
    resultado = verficar_internet(vezes, tempo)
    print('-'*8, 'Resumo dos Resultados', '-'*8)
    print(resultado)
