Análisis y Optimización de Procesador ARM Cortex A76
Autor: Miguel Angel Alvarez Guzman
Simuladores: gem5, McPAT
Idioma: Python

Descripción del Proyecto
Este proyecto tiene como objetivo analizar y optimizar el rendimiento de un procesador ARM Cortex A76 bajo diferentes configuraciones de parámetros utilizando el entorno de simulación gem5 y evaluando el consumo energético con McPAT. Se centra en identificar los parámetros que maximizan el rendimiento en términos de IPC (Instrucciones por Ciclo) y optimizan la eficiencia energética.

Estructura del Proyecto
El proyecto se estructura de la siguiente manera:

scripts/: Contiene los scripts de Python que automatizan las simulaciones y el análisis de resultados.
config/: Archivos de configuración para el entorno gem5 y McPAT.
data/: Carpeta donde se almacenan los resultados y perfiles de cada simulación.
figuras/: Incluye gráficos generados, como comparaciones de IPC, consumo energético, EDP, y tiempos de ejecución.
Metodología
Configuración Inicial: Se establece la configuración base del procesador en gem5 siguiendo la documentación de gem5 y McPAT, con configuraciones proporcionadas por los profesores.
Selección de Parámetros: Basado en una simulación inicial, se identifican parámetros clave para modificar, tales como:
Tamaño y líneas de caché L2 y L3.
Número de unidades funcionales de lectura y ALU.
Simulaciones Iterativas: Se implementa un script en Python que realiza simulaciones para cada configuración, analizando el impacto de cada ajuste en el rendimiento.
Análisis de Resultados: Los resultados se analizan en términos de IPC, consumo energético y EDP para determinar la configuración óptima.
Resultados
Los resultados principales muestran que el aumento en el número de unidades funcionales de lectura y ALU tiende a mejorar el rendimiento, mientras que los aumentos en el tamaño de la caché no siempre son beneficiosos. Los gráficos generados ilustran cómo cada cambio de parámetro afecta el IPC y el consumo energético.

Conclusiones
Este estudio concluye que:

Las unidades funcionales adicionales son determinantes para optimizar el rendimiento.
Aumentar el tamaño de la caché debe evaluarse cuidadosamente, ya que puede no tener impacto significativo en el IPC.
Las configuraciones óptimas varían según el tipo de programa, por lo que se recomienda adaptar los parámetros a las necesidades de cada aplicación.
Requisitos
Para reproducir este proyecto, se requiere:

Python (versión 3.6+)
gem5 (última versión estable)
McPAT
Ejecución
Configura gem5 y McPAT en tu entorno siguiendo las guías oficiales.
Clona este repositorio:
bash
Copiar código
git clone https://github.com/jbcgames/General_Test
Ejecuta los scripts de simulación en la carpeta scripts/.
Referencias
Más detalles y código disponible en: https://github.com/jbcgames/General_Test.

