import numpy as np
import pandas as pd

# Relação de marchas para o HB20 (aproximado)
relacao_marchas = {1: 3.909, 2: 2.136, 3: 1.481, 4: 1.179, 5: 0.861}

# Relação final do diferencial do HB20
relacao_final = 4.18

# Circunferência aproximada do pneu em metros
circunferencia_pneu = 1.98  # valor típico para carros de corrida
raio_roda = circunferencia_pneu / (2 * np.pi)  # Raio da roda em metros

# Torque máximo do motor (aproximado para o HB20 de competição)
torque_maximo_motor = 178  # em Nm

# Massa do veículo (aproximada)
massa_veiculo = 1100  # em kg

# Função para calcular o RPM com base na marcha e na velocidade
def calcular_rpm(velocidade_kmh, marcha):
    relacao = relacao_marchas[marcha] if marcha in relacao_marchas else relacao_marchas[5]
    # Cálculo do RPM com relação final e circunferência da roda
    rpm = (velocidade_kmh * 1000 * relacao * relacao_final) / (circunferencia_pneu * 60)
    return max(4500, min(rpm, 7000))  # Garantindo que o RPM fique entre 4500 e 7000

# Função para calcular a aceleração longitudinal durante a aceleração
def calcular_aceleracao_longitudinal(marcha, torque_motor, massa_veiculo, posicao_acelerador):
    # Posicao_acelerador varia de 0 (sem aceleração) a 1 (aceleração total)
    relacao_marcha = relacao_marchas[marcha] if marcha in relacao_marchas else relacao_marchas[5]
    forca_rodas = (torque_motor * relacao_marcha * relacao_final * posicao_acelerador) / raio_roda
    aceleracao_longitudinal = forca_rodas / massa_veiculo
    return aceleracao_longitudinal

# Função para calcular a ação do freio necessária para uma desaceleração desejada
def calcular_acao_freio(velocidade_anterior, velocidade_atual, massa_veiculo, distancia_frenagem):
    v_i = velocidade_anterior / 3.6  # Convertendo para m/s
    v_f = velocidade_atual / 3.6     # Convertendo para m/s
    # Cálculo da desaceleração necessária
    a = (v_f ** 2 - v_i ** 2) / (2 * distancia_frenagem)
    
    # Cálculo da força de frenagem
    forca_frenagem = abs(massa_veiculo * a)
    
    # Estimativa da ação no freio com base em uma força máxima de 8000 N
    acao_freio = min(100, (forca_frenagem / 8000) * 100)
    return round(acao_freio, 2)

# Função para calcular a aceleração lateral em G com base na velocidade e no raio da curva
def calcular_aceleracao_lateral(velocidade_kmh, raio_curva):
    velocidade_ms = velocidade_kmh / 3.6  # Convertendo km/h para m/s
    aceleracao_lateral = (velocidade_ms ** 2) / raio_curva  # Aceleração lateral em m/s²
    aceleracao_lateral_g = aceleracao_lateral / 9.81  # Convertendo para força G
    return round(aceleracao_lateral_g, 2)

# Função para calcular a aceleração total (longitudinal + lateral)
def calcular_aceleracao_total(aceleracao_longitudinal, aceleracao_lateral):
    return np.sqrt(aceleracao_longitudinal**2 + aceleracao_lateral**2)

# Simulação do trail braking e aceleração nas curvas
for i in range(n_dados):
    t = tempo[i]
    
    # Primeira curva: frenagem de 120 km/h para 70 km/h
    if i < curva_1_duracao * n_dados:
        vel_anterior = velocidade[i-1] if i > 0 else velocidade_inicial  # Velocidade inicial no S do Senna
        delta_v = (velocidade_minima - vel_anterior) / (curva_1_duracao * n_dados)  # Desaceleração
        velocidade[i] = vel_anterior + delta_v
        frenagem[i] = calcular_acao_freio(vel_anterior, velocidade[i], massa_veiculo, distancia_frenagem)  # Ação no freio
        aceleracao_flag[i] = "N"  # Não está acelerando durante a frenagem
        aceleracao_longitudinal[i] = delta_v / intervalo_tempo  # Aceleração longitudinal em m/s²
        aceleracao_lateral[i] = calcular_aceleracao_lateral(velocidade[i], raio_curva_1)  # Aceleração lateral com base no raio da curva 1
    
    # Segunda curva: transição
    elif i < (curva_1_duracao + curva_2_duracao) * n_dados:
        vel_anterior = velocidade[i-1]
        delta_v = (80 - vel_anterior) / (curva_2_duracao * n_dados)  # Aceleração leve até 80 km/h
        velocidade[i] = vel_anterior + delta_v
        frenagem[i] = 0  # Sem frenagem
        aceleracao_flag[i] = "S"  # Está acelerando
        # Aplicando aceleração gradual na transição, simulando ação progressiva do piloto
        posicao_acelerador = min(1, (i - curva_1_duracao * n_dados) / (curva_2_duracao * n_dados))
        aceleracao_longitudinal[i] = calcular_aceleracao_longitudinal(marcha[i-1], torque_maximo_motor, massa_veiculo, posicao_acelerador)  # Calculando a aceleração longitudinal com base no torque
        aceleracao_lateral[i] = calcular_aceleracao_lateral(velocidade[i], raio_curva_2)  # Aceleração lateral com base no raio da curva 2
    
    # Terceira curva: aceleração até 110 km/h
    else:
        vel_anterior = velocidade[i-1]
        delta_v = (velocidade_final - vel_anterior) / (curva_3_duracao * n_dados)  # Aceleração até 110 km/h
        velocidade[i] = vel_anterior + delta_v
        frenagem[i] = 0  # Sem frenagem
        aceleracao_flag[i] = "S"  # Está acelerando
        # Acelerador já próximo de 100% na saída do S do Senna
        posicao_acelerador = 1
        aceleracao_longitudinal[i] = calcular_aceleracao_longitudinal(marcha[i-1], torque_maximo_motor, massa_veiculo, posicao_acelerador)  # Calculando a aceleração longitudinal com base no torque
        aceleracao_lateral[i] = calcular_aceleracao_lateral(velocidade[i], raio_curva_3)  # Aceleração lateral com base no raio da curva 3
    
    # Cálculo da aceleração total
    aceleracao_total[i] = calcular_aceleracao_total(aceleracao_longitudinal[i], aceleracao_lateral[i])
    
    # Definir marcha com base na velocidade
    if velocidade[i] < 40:
        marcha[i] = 1
    elif velocidade[i] < 90:
        marcha[i] = 2
    elif velocidade[i] < 120:
        marcha[i] = 3
    elif velocidade[i] < 160:
        marcha[i] = 4
    else:
        marcha[i] = 5
    
    # Cálculo do RPM com base na marcha e velocidade
    rpm[i] = calcular_rpm(velocidade[i], marcha[i])

# Criando o DataFrame com os dados simulados para o S do Senna
dados_s_do_senna = pd.DataFrame({
    "Tempo (s)": tempo,
    "Velocidade (km/h)": np.round(velocidade, 2),
    "Aceleração Longitudinal (m/s²)": np.round(aceleracao_longitudinal, 2),
    "Aceleração Lateral (g)": np.round(aceleracao_lateral, 2),  # Aceleração lateral em G
    "Aceleração Total (m/s²)": np.round(aceleracao_total, 2),
    "RPM": np.round(rpm, 2),
    "Marcha": marcha,
    "Frenagem (%)": np.round(frenagem, 2),
    "Aceleração": aceleracao_flag,
    "Local do Autódromo": posicao_pista
})

# Ajustando para "," como delimitador decimal e ";" como delimitador CSV
dados_s_do_senna["Frenagem (%)"] = dados_s_do_senna["Frenagem (%)"].astype(str).str.replace('.', ',')
dados_s_do_senna["RPM"] = dados_s_do_senna["RPM"].astype(str).str.replace('.', ',')
dados_s_do_senna["Aceleração Longitudinal (m/s²)"] = dados_s_do_senna["Aceleração Longitudinal (m/s²)"].astype(str).str.replace('.', ',')
dados_s_do_senna["Aceleração Lateral (g)"] = dados_s_do_senna["Aceleração Lateral (g)"].astype(str).str.replace('.', ',')
dados_s_do_senna["Aceleração Total (m/s²)"] = dados_s_do_senna["Aceleração Total (m/s²)"].astype(str).str.replace('.', ',')
dados_s_do_senna["Velocidade (km/h)"] = dados_s_do_senna["Velocidade (km/h)"].astype(str).str.replace('.', ',')
dados_s_do_senna["Tempo (s)"] = dados_s_do_senna["Tempo (s)"].astype(str).str.replace('.', ',')

# Salvando o trecho do S do Senna em um arquivo CSV separado com delimitador ";"
dados_s_do_senna.to_csv("simulacao_s_do_senna_corrigido.csv", sep=';', index=False)

# Exibindo os dados do trecho S do Senna
print(dados_s_do_senna) 
