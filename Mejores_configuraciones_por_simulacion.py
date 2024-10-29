import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo de resultados
df = pd.read_excel("Resultados_Especificos.xlsx")

# Crear listas para almacenar los resultados óptimos
best_ipc_results = []
lowest_energy_results = []
best_edp_results = []

# Agrupar por el tipo de simulación y seleccionar los mejores valores
for simulacion, group in df.groupby("simulacion"):
    # Mejor IPC
    best_ipc_row = group.loc[group['ipc'].idxmax()]
    best_ipc_results.append(best_ipc_row)
    
    # Menor consumo energético
    lowest_energy_row = group.loc[group['energy'].idxmin()]
    lowest_energy_results.append(lowest_energy_row)
    
    # Mejor EDP
    best_edp_row = group.loc[group['edp'].idxmin()]
    best_edp_results.append(best_edp_row)

# Crear DataFrames a partir de las listas de resultados
best_ipc_df = pd.DataFrame(best_ipc_results)
lowest_energy_df = pd.DataFrame(lowest_energy_results)
best_edp_df = pd.DataFrame(best_edp_results)

# Guardar los resultados en un nuevo archivo Excel con diferentes hojas para cada criterio
with pd.ExcelWriter("Resultados_Optimos.xlsx") as writer:
    best_ipc_df.to_excel(writer, sheet_name="Mejor_IPC", index=False)
    lowest_energy_df.to_excel(writer, sheet_name="Menor_Energia", index=False)
    best_edp_df.to_excel(writer, sheet_name="Mejor_EDP", index=False)

# --- Generar gráficos ---

# 1. Gráfico de barras para el mejor IPC de cada simulación
plt.figure(figsize=(10, 6))
plt.bar(best_ipc_df['simulacion'], best_ipc_df['ipc'], color='skyblue')
plt.title('Mejor IPC por Simulación')
plt.xlabel('Simulación')
plt.ylabel('Valor de IPC')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(best_ipc_df['ipc']):
    plt.text(i, value + 0.05, f"{value:.2f}", ha='center')
plt.tight_layout()
plt.savefig("Mejor_IPC.png")
plt.show()

# 2. Gráfico de barras apiladas para consumo energético mínimo
plt.figure(figsize=(10, 6))
plt.bar(lowest_energy_df['simulacion'], lowest_energy_df['total_leakage'], label='Total Leakage', color='orange')
plt.bar(lowest_energy_df['simulacion'], lowest_energy_df['runtime_dynamic'], bottom=lowest_energy_df['total_leakage'], label='Runtime Dynamic', color='blue')
plt.title('Consumo Energético Mínimo por Simulación')
plt.xlabel('Simulación')
plt.ylabel('Consumo Energético (W)')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("Consumo_Energetico_Minimo.png")
plt.show()

# 3. Gráfico de dispersión para el mejor EDP de cada simulación
plt.figure(figsize=(10, 6))
plt.scatter(best_edp_df['simulacion'], best_edp_df['edp'], color='green', s=100)
plt.title('Mejor EDP por Simulación')
plt.xlabel('Simulación')
plt.ylabel('Valor de EDP')
for i, value in enumerate(best_edp_df['edp']):
    plt.text(i, value + 0.05, f"{value:.4f}", ha='center')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("Mejor_EDP.png")
plt.show()
