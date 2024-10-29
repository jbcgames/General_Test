import matplotlib.pyplot as plt

# Nombres de las barras y sus valores correspondientes
labels = ['default', 'l2_sizes', 'l2_assocs', 'l3_sizes', 'l3_assocs', 'num_fu_reads', 'num_fu_intALUs']
values = [0.833469, 0.806953, 0.807024, 0.807024, 0.807024, 0.834586, 0.837333]
params = ['', '2MB', '4', '4MB', '8', '4', '8']

# Crear la figura y el eje
fig, ax = plt.subplots()

# Crear barras con el mismo color y contorno negro
bars = ax.bar(labels, values, color='skyblue', edgecolor='black')

# Añadir los parámetros encima de cada barra
for bar, param in zip(bars, params):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002, param, ha='center', va='bottom')

# Etiquetas y título de los ejes
ax.set_xlabel('Parámetros Ajustados')
ax.set_ylabel('IPC')
ax.set_title('Comparación de Configuración de Parámetros vs IPC')

# Rango del eje y para mostrar las diferencias
ax.set_ylim(1.04, 1.11)

# Mostrar la gráfica
plt.show()
