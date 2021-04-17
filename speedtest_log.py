import os
import pandas as pd
import time
import speedtest
import matplotlib.pyplot as plt
from datetime import datetime

def verficar_internet(repeticoes, intervalo):
    arquivo = 'dados.csv'

    if os.path.exists(arquivo):
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

def gerar_grafico(df):
    labels = df['Horário']
    width = 0.35
    x = [x for x in range(len(labels))]
    x1 = [x - width/2 for x in range(len(labels))]
    x2 = [x + width/2 for x in range(len(labels))]
    y1 = list(map(int, df['Download']))
    y2 = list(map(int, df['Upload']))

    plt.style.use('seaborn')
    fig, ax = plt.subplots(dpi=144)
    download = ax.bar(x1, y1, width, label='Download')
    upload = ax.bar(x2, y2, width, label='Upload')

    ax.set_ylabel('Velocidade')
    ax.set_title('Velocidade Medida')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=5)
    ax.legend(fontsize=5)

    ax.bar_label(download)
    ax.bar_label(upload)

    fig.tight_layout()

    return plt.show()

if __name__ == '__main__':

    vezes = int(input('Informe a quantidade de testes: '))
    tempo = float(input('Informe o intervalo de tempo em horas: '))
    resultado = verficar_internet(vezes, tempo)
    print('-'*8, 'Resumo dos Resultados', '-'*8)
    print(resultado)

    exibe_grafico = str(input('Deseja exibir um gráfico com os resultados? [S/N] '))[0].upper()

    if exibe_grafico == 'S':
        gerar_grafico(resultado)
