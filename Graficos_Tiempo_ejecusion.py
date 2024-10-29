import pandas as pd
import matplotlib.pyplot as plt

# Datos proporcionados en un DataFrame
data = {
    'folder': [
        "hjgpdecResult_l21MB_l316MB_nfu1_intALU2", "mp3decResult_l22MB_l34MB_nfu1_intALU2",
        "h264decResult_l21MB_l34MB_nfu1_intALU2", "hjgpdecResult_l21MB_l34MB_nfu1_intALU2",
        "mp3decResult_l2512kB_l316MB_nfu1_intALU2", "h264decResult_l22MB_l316MB_nfu1_intALU2",
        "h264decResult_l22MB_l34MB_nfu1_intALU2", "hjgpdecResult_l21MB_l38MB_nfu1_intALU2",
        "mp3decResult_l2512kB_l34MB_nfu1_intALU2", "h264decResult_l22MB_l38MB_nfu1_intALU2",
        "hjgpdecResult_l21MB_l38MB_nfu2_intALU2", "mp3decResult_l2512kB_l34MB_nfu2_intALU2",
        "h264decResult_l22MB_l38MB_nfu1_intALU2", "hjgpdecResult_l21MB_l38MB_nfu2_intALU4",
        "mp3decResult_l2512kB_l34MB_nfu4_intALU2", "h264decResult_l22MB_l38MB_nfu2_intALU2",
        "hjgpdecResult_l21MB_l38MB_nfu4_intALU2", "mp3decResult_l2512kB_l34MB_nfu4_intALU4",
        "h264decResult_l22MB_l38MB_nfu4_intALU4", "hjgpdecResult_l22MB_l34MB_nfu1_intALU2",
        "mp3decResult_l2512kB_l38MB_nfu1_intALU2", "h264decResult_l2512kB_l34MB_nfu1_intALU2",
        "hjgpencResult_l21MB_l34MB_nfu1_intALU2", "mp3encResult_l21MB_l34MB_nfu1_intALU2",
        "h264encResult_l21MB_l34MB_nfu1_intALU2", "hjgpencResult_l22MB_l316MB_nfu1_intALU2",
        "mp3encResult_l22MB_l34MB_nfu1_intALU2", "h264encResult_l22MB_l316MB_nfu1_intALU2",
        "hjgpencResult_l22MB_l34MB_nfu1_intALU2", "mp3encResult_l22MB_l34MB_nfu2_intALU2",
        "h264encResult_l22MB_l34MB_nfu2_intALU2", "hjgpencResult_l22MB_l38MB_nfu1_intALU2",
        "mp3encResult_l22MB_l34MB_nfu4_intALU2", "h264encResult_l22MB_l34MB_nfu4_intALU2",
        "hjgpencResult_l22MB_l38MB_nfu2_intALU2", "mp3encResult_l22MB_l34MB_nfu4_intALU4",
        "h264encResult_l22MB_l34MB_nfu4_intALU4", "hjgpencResult_l22MB_l38MB_nfu4_intALU4",
        "mp3encResult_l22MB_l38MB_nfu1_intALU2", "h264encResult_l22MB_l34MB_nfu4_intALU8",
        "hjgpencResult_l22MB_l38MB_nfu4_intALU8", "mp3encResult_l2512kB_l34MB_nfu1_intALU2",
        "h264encResult_l22MB_l38MB_nfu1_intALU2", "hjgpencResult_l2512kB_l34MB_nfu1_intALU2",
        "h264encResult_l2512kB_l34MB_nfu1_intALU2", "mp3decResult_l21MB_l34MB_nfu1_intALU2"
    ],
    'sim_seconds': [
        0.22194, 0.103578, 0.113, 0.221958, 0.103578, 0.112517,
        0.112527, 0.22194, 0.103578, 0.112517,
        0.219413, 0.100953, 0.112517, 0.219315,
        0.099432, 0.110706, 0.219425, 0.099257,
        0.110477, 0.221996, 0.103578, 0.114913,
        0.170297, 0.140733, 0.143866, 0.169514,
        0.140661, 0.14138, 0.170003, 0.136016,
        0.139557, 0.169489, 0.135607, 0.139381,
        0.167661, 0.135569, 0.139339, 0.16739,
        0.140661, 0.139357, 0.167392, 0.140811,
        0.14138, 0.170533, 0.149187, 0.103579
    ]
}

df = pd.DataFrame(data)

# Dividir los datos en dos subconjuntos
df1 = df.iloc[:len(df)//2]
df2 = df.iloc[len(df)//2:]

# Crear el primer gráfico
plt.figure(figsize=(12, 10))
bars1 = plt.barh(df1['folder'], df1['sim_seconds'], color='skyblue')
plt.xlabel('Execution Time (sim_seconds)')
plt.ylabel('Simulation Configurations')
plt.title('Execution Time por simulacion - Parte 1')
for bar, value in zip(bars1, df1['sim_seconds']):
    plt.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, f"{value:.4f}", va='center')
plt.tight_layout()
plt.show()

# Crear el segundo gráfico
plt.figure(figsize=(12, 10))
bars2 = plt.barh(df2['folder'], df2['sim_seconds'], color='salmon')
plt.xlabel('Execution Time (sim_seconds)')
plt.ylabel('Simulation Configurations')
plt.title('Execution Time por simulacion - Parte 2')
for bar, value in zip(bars2, df2['sim_seconds']):
    plt.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, f"{value:.4f}", va='center')
plt.tight_layout()
plt.show()
