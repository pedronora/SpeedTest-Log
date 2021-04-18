import os
import pandas as pd
import time
import speedtest
import matplotlib.pyplot as plt
from datetime import datetime

def verficar_internet(repeticoes, intervalo):
    """[Função para realizar medições periódicas das velocidades de download e upload da conexão de internet local. Utiliza a biblioteca 'speedtet-cli'.]

    Args:
        repeticoes ([int]): [Número de medições a serem realizadas]
        intervalo ([float]): [Periodicidade das medições em horas]

    Returns:
        [pandas Dataframe]: [columns=['Horário', 'Download', 'Upload']]
    """
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

def gerar_grafico(df, intervalo):
    """[Função para gerar a representação gráfica do DataFrame retornado pela função verificar_internet]

    Args:
        df [pandas Dataframe]]): [Pandas DataFrame retornado da função verificar_internet]
        intervalo ([int]): [Periodicidade das medições em horas. Deve ser a mesma que a indicada na função verificar_internet]
    """
    df['Horário'] = pd.to_datetime(df['Horário'])
    shift = pd.to_timedelta(intervalo*0.35, unit='h')
    x = df['Horário']
    y1 = list(map(int, df['Download']))
    y2 = list(map(int, df['Upload']))

    plt.style.use('seaborn')
    fig, ax = plt.subplots(dpi=144)
    download = ax.bar(x - shift/2, y1, width=shift, label='Download')
    upload = ax.bar(x + shift/2, y2, width=shift, label='Upload')

    ax.set_ylabel('Velocidade')
    ax.set_title('Velocidade Medida')
    ax.legend(fontsize=7)

    ax.bar_label(download)
    ax.bar_label(upload)

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':

    vezes = int(input('Informe a quantidade de testes: '))
    tempo = float(input('Informe o intervalo de tempo em horas: '))
    resultado = verficar_internet(vezes, tempo)
    print('-'*8, 'Resumo dos Resultados', '-'*8)
    print(resultado)

    exibe_grafico = str(input('Deseja exibir um gráfico com os resultados? [S/N] '))[0].upper()
    while exibe_grafico not in 'SN':
        exibe_grafico = str(input('Deseja exibir um gráfico com os resultados? [S/N] '))[0].upper()

    if exibe_grafico == 'S':
        gerar_grafico(resultado, tempo)
