import matplotlib.pyplot as plt

# Define los datos categorizando cada simulación para darle un color distinto
energy = [4.722520, 2.624194, 3.037048, 4.189055, 2.934714, 3.507473, 3.105191, 4.371785, 2.514703, 3.242970, 4.344791, 
          2.466155, 4.341461, 2.443017, 3.207768, 4.344112, 2.441732, 3.199320, 4.280216, 2.658631, 3.018096, 4.127941, 
          2.621727, 2.738154, 4.697206, 2.716526, 3.213497, 4.209733, 2.650537, 2.765902, 4.373033, 2.641794, 2.762786, 
          4.343637, 2.641268, 2.760928, 4.346607, 2.905436, 2.761139, 4.345194, 2.573308, 2.937252, 4.086185, 2.740295, 
          2.552063]
ipc = [0.834105, 1.059257, 1.100934, 0.834039, 1.059258, 1.105657, 1.105553, 0.834105, 1.059258, 1.105657, 0.843714, 
       1.0868, 0.844089, 1.103426, 1.123739, 0.843666, 1.105379, 1.126074, 0.833896, 1.059258, 1.082602, 0.898979, 
       0.80661, 1.04034, 0.903133, 0.807024, 1.058638, 0.900538, 0.834586, 1.072461, 0.903265, 0.837098, 1.073819, 
       0.913115, 0.837333, 1.074143, 0.914592, 0.807024, 1.074006, 0.914581, 0.806164, 1.058638, 0.897737, 1.003238, 
       1.059253]

# Etiquetas de cada simulación
labels = ["jpg2k_dec", "mp3dec", "h264dec", "jpg2k_dec", "mp3dec", "h264dec", "h264dec", "jpg2k_dec", "mp3dec", "h264dec", 
          "jpg2k_dec", "mp3dec", "jpg2k_dec", "mp3dec", "h264dec", "jpg2k_dec", "mp3dec", "h264dec", "jpg2k_dec", "mp3dec", 
          "h264dec", "jpg2k_enc", "mp3enc", "h264enc", "jpg2k_enc", "mp3enc", "h264enc", "jpg2k_enc", "mp3enc", "h264enc", 
          "jpg2k_enc", "mp3enc", "h264enc", "jpg2k_enc", "mp3enc", "h264enc", "jpg2k_enc", "mp3enc", "h264enc", "jpg2k_enc", 
          "mp3enc", "h264enc", "jpg2k_enc", "h264enc", "mp3dec"]

# Asocia cada simulación a un color distinto
colors = {
    "h264dec": "blue",
    "h264enc": "green",
    "jpg2k_dec": "purple",
    "jpg2k_enc": "orange",
    "mp3dec": "red",
    "mp3enc": "brown"
}
point_colors = [colors[label] for label in labels]

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.scatter(ipc, energy, c=point_colors, s=50, alpha=0.7)

# Configuración de etiquetas y título
plt.xlabel("IPC")
plt.ylabel("Energia")
plt.title("Energia vs IPC")

# Leyenda basada en los colores
for label, color in colors.items():
    plt.scatter([], [], c=color, label=label)
plt.legend(title="Programa")

plt.show()
