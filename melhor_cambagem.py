import numpy as np
import pandas as pd

# Dados do HB20
massa_carro = 1040  # kg
g = 9.81  # aceleração da gravidade em m/s^2
h = 0.55  # altura do centro de gravidade em metros
w = 1.47  # bitola em metros
mu = 1.0  # coeficiente de atrito
velocidade = 30  # velocidade longitudinal em m/s
raio_curva = 75  # raio da curva em metros
k = -0.03  # fator de cambagem

# Função para calcular a aceleração lateral
def calcular_aceleracao_lateral(v, r):
    return v**2 / r

# Função para calcular a força normal em cada roda
def calcular_forca_normal(m, a_lateral, h, w):
    delta_Fz = (m * a_lateral * h) / (2 * w)
    Fz_interno = (m * g) / 4 - delta_Fz
    Fz_externo = (m * g) / 4 + delta_Fz
    return Fz_interno, Fz_externo

# Função para calcular a força lateral em uma roda
def calcular_forca_lateral(Fz, mu, cambagem):
    f_alpha = 1 + k * cambagem
    return mu * Fz * f_alpha

# Preparar a tabela de combinações de cambagem
cambagens = np.arange(0, -3.5, -0.5)  # Variando de 0 a -3 com steps de 0.5
combinacoes = []

# Calcular aceleração lateral
a_lateral = calcular_aceleracao_lateral(velocidade, raio_curva)

# Gerar todas as combinações de cambagem para as quatro rodas
for cambagem_1 in cambagens:
    for cambagem_2 in cambagens:
        for cambagem_3 in cambagens:
            for cambagem_4 in cambagens:
                # Calcular a força normal nas rodas internas e externas
                Fz_interno, Fz_externo = calcular_forca_normal(massa_carro, a_lateral, h, w)
                
                # Calcular as forças laterais para as quatro rodas
                F_L1 = calcular_forca_lateral(Fz_externo, mu, cambagem_1)  # Roda externa dianteira esquerda
                F_L2 = calcular_forca_lateral(Fz_interno, mu, cambagem_2)  # Roda interna dianteira direita
                F_L3 = calcular_forca_lateral(Fz_externo, mu, cambagem_3)  # Roda externa traseira esquerda
                F_L4 = calcular_forca_lateral(Fz_interno, mu, cambagem_4)  # Roda interna traseira direita
                
                # Somar as forças laterais
                soma_forcas_laterais = F_L1 + F_L2 + F_L3 + F_L4
                
                # Calcular a força g (a_lateral_max)
                a_lateral_max = soma_forcas_laterais / (massa_carro * g)
                
                # Adicionar a combinação e o valor de g na lista
                combinacoes.append({
                    'Cambagem Roda 1': cambagem_1,
                    'Cambagem Roda 2': cambagem_2,
                    'Cambagem Roda 3': cambagem_3,
                    'Cambagem Roda 4': cambagem_4,
                    'Força G': a_lateral_max
                })

# Converter a lista de combinações em um DataFrame
df_combinacoes = pd.DataFrame(combinacoes)

# Encontrar a combinação que maximiza a força G
melhor_combinacao = df_combinacoes.loc[df_combinacoes['Força G'].idxmax()]

# Exibir a melhor combinação de cambagem e a força g correspondente
print("Melhor combinação de cambagem:")
print(melhor_combinacao)
