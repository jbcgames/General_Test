import os
import subprocess
import re

# Definir las rutas necesarias
gem5_path = "/home/jbcgames/mySimTools/gem5/build/ARM"
script_dir = "../../scripts/CortexA76_scripts_gem5"
mcpat_script_path = "/home/jbcgames/mySimTools/test/scripts/McPAT/gem5toMcPAT_cortexA76.py"
mcpat_path = "/home/jbcgames/mySimTools/mcpat/mcpat"
mcpat_xml = "/home/jbcgames/mySimTools/test/scripts/McPAT/ARM_A76_2.1GHz.xml"

processes = [
    {"name": "h264_dec", "dir": "h264decResult", "options": "h264dec_testfile.264 h264dec_outfile.yuv"},
    {"name": "h264_enc", "dir": "h264encResult", "options": "h264enc_configfile.cfg"},
    {"name": "jpg2k_dec", "dir": "hjgpdecResult", "options": "-i jpg2kdec_testfile.j2k -o jpg2kdec_outfile.bmp"},
    {"name": "jpg2k_enc", "dir": "hjgpencResult", "options": "-i jpg2kenc_testfile.bmp -o jpg2kenc_outfile.j2k"},
    {"name": "mp3_dec", "dir": "mp3decResult", "options": "-w mp3dec_outfile.wav mp3dec_testfile.mp3"},
    {"name": "mp3_enc", "dir": "mp3encResult", "options": "mp3enc_testfile.wav mp3enc_outfile.mp3"}
]

# Valores de los parámetros a probar
l2_sizes = ["512kB", "1MB", "2MB"]
l2_assocs = [2, 4, 8]
l3_sizes = ["4MB", "8MB", "16MB"]
l3_assocs = [8, 16, 32]
num_fu_reads = [1, 2, 4]
num_fu_intALUs = [2, 4, 8]

def run_mcpat_and_extract_dynamic(sim_output_dir):
    stats_file = os.path.join(sim_output_dir, "stats.txt")
    config_file = os.path.join(sim_output_dir, "config.json")
    mcpat_output_file = "config.xml"  # El archivo XML que se generará
    mcpat_log_file = "mcpat.log"

    # Ejecutar el script de gem5 a McPAT
    cmd_mcpat_script = f"python3 {mcpat_script_path} {stats_file} {config_file} {mcpat_xml}"
    subprocess.run(cmd_mcpat_script, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Mover el archivo XML generado a la carpeta de resultados de la simulación
    if os.path.exists(mcpat_output_file):
        destination_path = os.path.join(sim_output_dir, mcpat_output_file)
        os.rename(mcpat_output_file, destination_path)
        print(f"{mcpat_output_file} movido a {destination_path}")
    else:
        print(f"{mcpat_output_file} no fue encontrado y no se movió.")
        
    # Ejecutar McPAT
    cmd_mcpat = f"{mcpat_path} -infile {mcpat_output_file} -print_level 0 > {mcpat_log_file}"
    subprocess.run(cmd_mcpat, shell=True, cwd=sim_output_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
   
    
    # Extraer Runtime Dynamic de mcpat.log
    mcpat_log_path = os.path.join(sim_output_dir, mcpat_log_file)
    runtime_dynamic = None
    
    if os.path.exists(mcpat_log_path):
        with open(mcpat_log_path, 'r') as file:
            for line in file:
                match = re.search(r"Runtime Dynamic = ([\d\.]+)", line)
                if match:
                    runtime_dynamic = float(match.group(1))
                    print(runtime_dynamic)
                    break
    else:
        print(f"{sim_output_dir}: {mcpat_log_file} no fue encontrado")
    
    return runtime_dynamic

# Función para ejecutar la simulación con los parámetros dados y retornar el IPC
def run_simulation(process, l2_size, l2_assoc, l3_size, l3_assoc, num_fu_read, num_fu_intALU):
    sim_output_dir = f"{process['dir']}_l2{l2_size}_l3{l3_size}_nfu{num_fu_read}_intALU{num_fu_intALU}"
    
    # Mostrar los parámetros con los que se ejecutará la simulación
    print(f"Ejecutando simulación para {process['name']} con parámetros:")
    print(f"  l2_size: {l2_size}")
    print(f"  l2_assoc: {l2_assoc}")
    print(f"  l3_size: {l3_size}")
    print(f"  l3_assoc: {l3_assoc}")
    print(f"  num_fu_read: {num_fu_read}")
    print(f"  num_fu_intALU: {num_fu_intALU}")
    print(f"  Directorio de salida: {sim_output_dir}")
    
    # Comando con los parámetros
    cmd = f"{gem5_path}/gem5.fast -d {sim_output_dir} {script_dir}/CortexA76.py --cmd={process['name']} --options='{process['options']}' --l2_size={l2_size} --l2_assoc={l2_assoc} --l3_size={l3_size} --l3_assoc={l3_assoc} --num_fu_read={num_fu_read} --num_fu_intALU={num_fu_intALU}"
    
    # Ejecutar el comando redirigiendo stdout y stderr a DEVNULL para ocultar la salida de gem5
    process_exec = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return process_exec, sim_output_dir

# Función para extraer el IPC de un archivo stats.txt
def extract_ipc(sim_output_dir):
    stats_file_path = os.path.join(sim_output_dir, 'stats.txt')
    ipc = None
    
    if os.path.exists(stats_file_path):
        with open(stats_file_path, 'r') as file:
            for line in file:
                match = re.search(r'system.cpu.ipc\s+([\d\.]+)', line)
                if match:
                    ipc = float(match.group(1))
                    break
    else:
        print(f"{sim_output_dir}: stats.txt not found")
    
    return ipc

# Función para encontrar el mejor valor de un parámetro dado, manteniendo los otros parámetros fijos para todos los procesos simultáneamente
def find_best_value_for_all_processes(processes, param_values, fixed_params, param_name):
    best_value_for_each_process = {}
    best_ipc_for_each_process = {}
    
    for value in param_values:
        total_ipc_for_all_processes = 0
        
        # Ejecutar simulaciones simultáneamente para todos los procesos
        active_processes = []
        for process in processes:
            current_params = fixed_params[process['name']].copy()
            current_params[param_name] = value
            
            proc_exec, sim_output_dir = run_simulation(
                process, 
                current_params['l2_size'], current_params['l2_assoc'],
                current_params['l3_size'], current_params['l3_assoc'],
                current_params['num_fu_read'], current_params['num_fu_intALU']
            )
            active_processes.append((proc_exec, sim_output_dir, process['name']))
        
        # Esperar a que todos los procesos terminen y recolectar resultados
        for proc_exec, sim_output_dir, process_name in active_processes:
            proc_exec.wait()  # Esperar a que el proceso termine

            # Ejecutar McPAT y extraer el dynamic power después de que termine la simulación
            runtime_dynamic = run_mcpat_and_extract_dynamic(sim_output_dir)
            if runtime_dynamic is not None:
                print(f"Runtime Dynamic para {process_name} con {param_name}={value}: {runtime_dynamic}")

            # Extraer el IPC después de que la simulación termine
            ipc = extract_ipc(sim_output_dir)
            
            # Mostrar el resultado del IPC de la simulación
            if ipc is not None:
                print(f"Resultado IPC para {process_name} con {param_name}={value}: {ipc}")
                total_ipc_for_all_processes += ipc
                # Si el IPC es mejor que el previo para este proceso, guardar el mejor valor
                if process_name not in best_ipc_for_each_process or ipc > best_ipc_for_each_process[process_name]:
                    best_ipc_for_each_process[process_name] = ipc
                    best_value_for_each_process[process_name] = value
    
    return best_value_for_each_process, best_ipc_for_each_process

# Iniciar con valores por defecto para cada proceso
fixed_params = {
    process['name']: {
        'l2_size': l2_sizes[0],
        'l2_assoc': l2_assocs[0],
        'l3_size': l3_sizes[0],
        'l3_assoc': l3_assocs[0],
        'num_fu_read': num_fu_reads[0],
        'num_fu_intALU': num_fu_intALUs[0]
    }
    for process in processes
}

# Encontrar el mejor tamaño de L2 para cada proceso
best_l2_size, best_ipc_l2 = find_best_value_for_all_processes(processes, l2_sizes, fixed_params, 'l2_size')
print(f"Mejores L2 size por proceso: {best_l2_size}")

# Actualizar los valores de L2 size en los parámetros fijos
for process in processes:
    fixed_params[process['name']]['l2_size'] = best_l2_size[process['name']]

# Encontrar la mejor asociatividad de L2 para cada proceso
best_l2_assoc, best_ipc_l2_assoc = find_best_value_for_all_processes(processes, l2_assocs, fixed_params, 'l2_assoc')
print(f"Mejores L2 assoc por proceso: {best_l2_assoc}")

# Actualizar los valores de L2 assoc en los parámetros fijos
for process in processes:
    fixed_params[process['name']]['l2_assoc'] = best_l2_assoc[process['name']]

# Encontrar el mejor tamaño de L3 para cada proceso
best_l3_size, best_ipc_l3 = find_best_value_for_all_processes(processes, l3_sizes, fixed_params, 'l3_size')
print(f"Mejores L3 size por proceso: {best_l3_size}")

# Actualizar los valores de L3 size en los parámetros fijos
for process in processes:
    fixed_params[process['name']]['l3_size'] = best_l3_size[process['name']]

# Encontrar la mejor asociatividad de L3 para cada proceso
best_l3_assoc, best_ipc_l3_assoc = find_best_value_for_all_processes(processes, l3_assocs, fixed_params, 'l3_assoc')
print(f"Mejores L3 assoc por proceso: {best_l3_assoc}")

# Actualizar los valores de L3 assoc en los parámetros fijos
for process in processes:
    fixed_params[process['name']]['l3_assoc'] = best_l3_assoc[process['name']]

# Encontrar el mejor número de unidades funcionales de lectura para cada proceso
best_num_fu_read, best_ipc_fu_read = find_best_value_for_all_processes(processes, num_fu_reads, fixed_params, 'num_fu_read')
print(f"Mejores num_fu_read por proceso: {best_num_fu_read}")

# Actualizar los valores de num_fu_read en los parámetros fijos
for process in processes:
    fixed_params[process['name']]['num_fu_read'] = best_num_fu_read[process['name']]

# Encontrar el mejor número de ALUs enteras para cada proceso
best_num_fu_intALU, best_ipc_fu_intALU = find_best_value_for_all_processes(processes, num_fu_intALUs, fixed_params, 'num_fu_intALU')
print(f"Mejores num_fu_intALU por proceso: {best_num_fu_intALU}")

# Actualizar los valores de num_fu_intALU en los parámetros fijos
for process in processes:
    fixed_params[process['name']]['num_fu_intALU'] = best_num_fu_intALU[process['name']]

# Mostrar los resultados finales
print("Mejores configuraciones finales por proceso:")
for process in processes:
    print(f"{process['name']}: {fixed_params[process['name']]}")
