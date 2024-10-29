import matplotlib.pyplot as plt

# Datos de los valores y nombres de los recursos
resources = ['default', 'l2_sizes', 'l2_assocs', 'l3_sizes', 'l3_assocs', 'num_fu_reads', 'num_fu_intALUs']

# Valores de rendimiento para cada aplicación
h264_dec_values = [1.065032, 1.105373, 1.105553, 1.105657, 1.105657, 1.125778, 1.126097]
h264_enc_values = [1.009344, 1.056809, 1.058638, 1.058638, 1.058638, 1.073819, 1.074143]
jpg2k_dec_values = [0.835481, 0.834011, 0.834039, 0.834105, 0.834105, 0.843714, 0.844131]
jpg2k_enc_values = [0.896866, 0.900538, 0.900538, 0.903265, 0.903265, 0.914028, 0.914592]
mp3_dec_values = [1.086794, 1.059258, 1.059258, 1.059258, 1.059258, 1.103426, 1.105382]
mp3_enc_values = [0.833469, 0.806953, 0.807024, 0.807024, 0.807024, 0.834586, 0.837333]

# Crear el gráfico de líneas para cada conjunto de datos
plt.plot(resources, h264_dec_values, marker='o', label='h264_dec')
plt.plot(resources, h264_enc_values, marker='o', label='h264_enc')
plt.plot(resources, jpg2k_dec_values, marker='o', label='jpg2k_dec')
plt.plot(resources, jpg2k_enc_values, marker='o', label='jpg2k_enc')
plt.plot(resources, mp3_dec_values, marker='o', label='mp3_dec')
plt.plot(resources, mp3_enc_values, marker='o', label='mp3_enc')

# Etiquetas y título de los ejes
plt.xlabel('Recursos Configurados')
plt.ylabel('Rendimiento (IPC)')
plt.title('Comparación de Rendimiento vs Recursos Configurados')

# Mostrar leyenda y gráfico
plt.legend()
plt.grid()
plt.show()
