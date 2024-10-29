import os
import re
import pandas as pd

# Lista de carpetas
folders = [
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
]

# Diccionario para almacenar resultados
results = []

# Procesar cada carpeta
for folder in folders:
    mcpat_file_path = os.path.join(folder, "mcpat.log")
    stats_file_path = os.path.join(folder, "stats.txt")

    total_leakage = None
    runtime_dynamic = None
    cpi = None
    ipc = None
    sim_seconds = None  # Tiempo de ejecución

    # Extraer parámetros del nombre de la carpeta
    simulation_match = re.match(r"(\w+?)Result_", folder)
    l2_cache_match = re.search(r"_l(\d+)(MB|kB)", folder)
    l3_cache_match = re.search(r"_l3(\d+)(MB|kB)", folder)
    nfu_match = re.search(r"_nfu(\d+)", folder)
    intALU_match = re.search(r"_intALU(\d+)", folder)

    # Ajustes para l2_cache_size y l3_cache_size
    simulation = simulation_match.group(1) if simulation_match else None
    l2_cache_size = f"{int(l2_cache_match.group(1)[1:])}{l2_cache_match.group(2)}" if l2_cache_match else None
    l3_cache_size = f"{int(l3_cache_match.group(1))}{l3_cache_match.group(2)}" if l3_cache_match else None
    num_fu_read = int(nfu_match.group(1)) if nfu_match else None
    num_fu_intALU = int(intALU_match.group(1)) if intALU_match else None

    try:
        # Procesar mcpat.txt
        if os.path.exists(mcpat_file_path):
            with open(mcpat_file_path, "r") as mcpat_file:
                mcpat_content = mcpat_file.read()
                total_leakage_match = re.search(r"Total Leakage = ([\d\.]+) W", mcpat_content)
                runtime_dynamic_match = re.search(r"Runtime Dynamic = ([\d\.]+) W", mcpat_content)

                if total_leakage_match:
                    total_leakage = float(total_leakage_match.group(1))
                if runtime_dynamic_match:
                    runtime_dynamic = float(runtime_dynamic_match.group(1))

        # Procesar stats.txt
        if os.path.exists(stats_file_path):
            with open(stats_file_path, "r") as stats_file:
                stats_content = stats_file.read()
                cpi_match = re.search(r"(system\.cpu\.cpi\s+[\d\.]+)", stats_content)
                ipc_match = re.search(r"(system\.cpu\.ipc\s+[\d\.]+)", stats_content)
                sim_seconds_match = re.search(r"simSeconds\s+([\d\.]+)", stats_content)

                if cpi_match:
                    cpi = float(cpi_match.group(0).split()[-1])
                if ipc_match:
                    ipc = float(ipc_match.group(0).split()[-1])
                if sim_seconds_match:
                    sim_seconds = float(sim_seconds_match.group(1))  # Guardar el tiempo de simulación

        # Almacenar resultados si todos los valores son encontrados
        if all(v is not None for v in [total_leakage, runtime_dynamic, cpi, ipc, simulation, l2_cache_size, l3_cache_size, num_fu_read, num_fu_intALU, sim_seconds]):
            results.append({
                "folder": folder,
                "simulacion": simulation,
                "l2_cache_size": l2_cache_size,
                "l3_cache_size": l3_cache_size,
                "num_fu_read": num_fu_read,
                "num_fu_intALU": num_fu_intALU,
                "total_leakage": total_leakage,
                "runtime_dynamic": runtime_dynamic,
                "cpi": cpi,
                "ipc": ipc,
                "sim_seconds": sim_seconds,  # Añadir tiempo de simulación al diccionario
                "energy": (total_leakage + runtime_dynamic) * cpi,
                "edp": (total_leakage + runtime_dynamic) * cpi * cpi
            })

    except Exception as e:
        print(f"Error al leer los archivos en la carpeta {folder}: {e}")

# Crear DataFrame y guardar en Excel
df = pd.DataFrame(results)
df.to_excel("Resultados_Especificos.xlsx", index=False, sheet_name="Resultados")
