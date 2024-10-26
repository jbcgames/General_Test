# python3 /home/estudiante/mySimtool/test/scripts/McPAT/gem5toMcPAT_cortexA76.py stats.txt config.json /home/estudiante/mySimtool/test/scripts/McPAT/ARM_A76_2.1GHz.xml 
# /home/estudiante/mySimtool/mcpat/mcpat -infile config.xml -print_level 0 > mcpat.log
import os
import subprocess
import re

# Definir las rutas necesarias
gem5_path = "/home/estudiante/mySimtool/gem5/build/ARM"
script_dir = "../../scripts/CortexA76_scripts_gem5"
mcpat_script_path = "/home/estudiante/mySimtool/test/scripts/McPAT/gem5toMcPAT_cortexA76.py"
mcpat_path = "/home/estudiante/mySimtool/mcpat/mcpat"
mcpat_xml = "/home/estudiante/mySimtool/test/scripts/McPAT/ARM_A76_2.1GHz.xml"

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

run_mcpat_and_extract_dynamic("mp3encResult_l2512kB_l34MB_nfu1_intALU2")
