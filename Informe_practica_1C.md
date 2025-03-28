
# Práctica 1C. Mediciones de potencia y frecuencia

## **Objetivo General**
Familiarizarse con el uso de herramientas de software definido por radio (SDR) como GNU Radio, junto con equipos de medición como el USRP 2920, el osciloscopio R&S RTB2004 y el analizador de espectros R&S FPC1000. Los estudiantes aprenderán a medir y analizar parámetros clave en comunicaciones, como potencia, ancho de banda, relación señal a ruido (SNR) y piso de ruido.

---

## **Materiales y Equipos**
- **USRP 2920**: Radio definido por software.
- **Osciloscopio R&S RTB2004**: Para visualización de señales en el dominio del tiempo y frecuencia.
- **Analizador de Espectros R&S FPC1000**: Para mediciones en el dominio de la frecuencia.
- **Computador con GNU Radio**: Para simulación y generación de señales usando el USRP 2920.
- **Cables y conectores**: Para interconexión de equipos.

---

## **Actividad 1: Revisión de Especificaciones de los Equipos**

### **Objetivo**
Familiarizarse con las especificaciones técnicas de los equipos de laboratorio y entender cómo configurarlos para realizar mediciones.

### **Procedimiento**
1. **Revisar Manuales y Verificar Equipos**:
   - Revisar las especificaciones de los equipos de laboratorio (USRP 2920, Osciloscopio R&S RTB2004 y Analizador de Espectros R&S FPC1000).
   - Identificar las principales funciones y controles de los equipos.

2. **Seleccionar Especificaciones Relevantes**:
   - Seleccionar las **5 especificaciones** que consideren **más relevantes** de cada equipo. 

3. **Configuración de los Equipos**:
   - **USRP 2920**: Identificar el rango de frecuencia y ganancia configurable del radio. Para esto, conecte la alimentación y el cable de red al radio, y desde un terminal (Ctrl + Alt + T) ejecute el comando `uhd_usrp_probe`.
   - **Osciloscopio R&S RTB2004**: Identificar el ancho de banda máximo, resolución vertical y tipos de mediciones soportadas.
   - **Analizador de Espectros R&S FPC1000**: Identificar el rango de frecuencia, resolución y figura de ruido.

### **Preguntas Orientadoras**
1. ¿Cuál es el rango de frecuencia del USRP 2920 y cómo se compara con el del analizador de espectros?
2. ¿Qué parámetros del USRP 2920 se deben configurar para transmitir una señal en una frecuencia específica?
3. ¿Cómo se configura el osciloscopio para medir la amplitud y la frecuencia de una señal?
4. ¿Qué diferencia hay entre medir una señal en el dominio del tiempo (osciloscopio) y en el dominio de la frecuencia (analizador de espectros)?
5. ¿Cómo se mide el piso de ruido en el analizador de espectros? ¿Cómo afecta la frecuencia central, SPAN y RBW la medida de piso de ruido? ¿Por qué?
#### **Respuestas**
1. El rango de frecuencia es de 50 MHz a 2.2 GHz, y, el analizador 1 GHz de SPAN.
2. Es necesario configurar los siguientes parámetros: La frecuencia de muestreo, la frecuencia de la señal y la ganancia de transmisión.
3. Para debe cerciorarse de que la señal sea visible de forma que se aprecie al menos un ciclo completo, y, que la amplitud no sea tan pequeña como para verse poco ni tan grande como para no verse (por salirse de la pantalla). Luego ir al apartado de Measure y mostrar Amplitud y Frecuencia.
4. La diferencia es que en el dominio de la frecuencia, la señal revela las frecuencias fundamentales y sus armónicos, mientras que en el dominio del tiempo se observa cómo varía a lo largo de un intervalo. Dependiendo de la información que se necesite, es más conveniente trabajar con uno u otro. Un ejemplo puede ser el cálculo de la potencia de una señal, es más sencillo analizarla en el dominio de la frecuencia para identificar los "picos" y luego convertir esa información a potencia.
5. Existen varias formas de medir el piso de ruido, y una de ellas consiste en normalizar el ancho de banda de resolución (RBW) a 1 Hz. De este modo, el logaritmo no altera la potencia del ruido, a diferencia de lo que ocurriría si el RBW estuviera en 300 Hz o 1 KHz. Además, la frecuencia central es relevante, ya que no es lo mismo medir el piso de ruido en un rango de frecuencias donde no hay señales notables, que hacerlo en un rango donde sí se detecta una señal y se desea evaluar el ancho de banda útil, descartando el resto como "ruido".
### **Evidencia**
- Lista con las 5 especificaciones más relevantes de cada equipo.
- Realice una medición de piso de ruido normalizado. La medición de piso resulto en -54.9 dBm aproximadamente. 

---

## **Actividad 2: Simulación de Señales en GNU Radio**

### **Objetivo**
Generar y analizar señales en GNU Radio para entender cómo se comportan diferentes formas de onda en tiempo y frecuencia.

### **Procedimiento**
1. **Iniciar GNU Radio**:
   - Ejecute GNU Radio Companion (GRC) (`gnuradio-companion`).
   - Cargue el flujograma [`simple_flowgraph.grc`](https://github.com/omreyes/LabComUIS/blob/develop/guides/practice1/simple_flowgraph.grc).
   - Identifique los bloques principales: `Signal Source`, `Throttle`, `QT GUI Time Sink` y `QT GUI Frequency Sink`.
   - Configure la frecuencia de muestreo (samp_rate) en 20 kHz.

2. **Ejecutar el Flujograma**:
   - Ejecute el flujograma y observe los diferentes controles (Source Controls, Channel Controls, USRP Controls), así como las señales generadas en las ventanas de tiempo (`Time Sink`) y frecuencia (`Frequency Sink`).
   - Identifique y relacione los bloques presentes en el flujograma con lo observado en la ventana de ejecución.
  
3. **Análisis de Señales** 
   - Analice y valide los resultados en el dominio del tiempo y de frecuencia si se modifica:
     - el tipo de dato de la fuente (compleja o flotante)
     - la forma de onda 
     - la frecuencia y fase de la señal
     - la amplitud de la señal generada.
   - Modifique el nivel de ruido del modelo de canal y analice el efecto en tiempo y frecuencia.

### **Preguntas Orientadoras**
1. ¿Cómo se puede explicar matemáticamente la diferencia entre una fuente de tipo flotante y una de tipo complejo?
2. ¿Cómo afecta la forma de onda a la distribución de energía (potencia) en el dominio de la frecuencia?
3. ¿Qué sucede con la señal en el dominio del tiempo y la frecuencia si se modifican los diferentes parámetros de la fuente? ¿Lo observado corresponde a lo esperado teóricamente?
4. ¿Cómo se relaciona la amplitud de la señal con la potencia observada en el dominio de la frecuencia?
5. ¿Qué diferencias se observan entre una señal senoidal y una señal cuadrada en el dominio de la frecuencia?

#### **Respuestas**
1. La principal diferencia entre una fuente de tipo flotante y una de tipo complejo radica en que la fuente flotante solo tiene un número decimal, correspondiente a la parte real de la señal. En cambio, una fuente de tipo complejo incluye tanto un número decimal para la parte real como otro número decimal para la parte imaginaria de la señal, lo que agrega una variable adicional.
2. La forma de la onda influye considerablemente en la distribución de la energía, ya que su descomposición en series de Fourier genera más componentes. Por ejemplo, una onda senoidal debería mostrar solo dos picos en el dominio de la frecuencia, mientras que una onda en forma de sierra, al tener una mayor complejidad, genera múltiples picos en ese mismo dominio. Es decir, afecta la cantidad de armónicos que son necesarios para representar a la señal al pasarla a potencia.
![Networking](Triangle_4500Hz.png)
![Networking](imagenes/Sine_100Hz.png)
3. En el dominio del tiempo, los cambios son más difíciles de notar, limitándose a una ligera variación en la amplitud. Sin embargo, en el dominio de la frecuencia, la potencia de las señales aumenta de manera significativa, lo que hace que estos cambios sean más evidentes.
4. La amplitud de la señal está relacionada con la potencia debido a su representación en la transformada de Fourier. Matemáticamente, esto se debe a que el espectro de una señal de la forma Acos(wt + p)es equivalente a dos impulsos con una amplitud de A/2. Esto muestra cómo la potencia de la señal se distribuye en el dominio de la frecuencia.
5. En el dominio de la frecuencia, una señal senoidal generalmente se representa por uno o dos picos notables, dependiendo de la frecuencia de la señal (sin incluir la frecuencia de la portadora). En cambio, para una señal cuadrada, los coeficientes de Fourier tienen un valor de \2A/(pi*n), lo que implica que se generan varios impulsos en el dominio de la frecuencia. Estos impulsos corresponden a los armónicos de la señal, y su amplitud disminuye a medida que aumenta el valor del número de n-armónico.

### **Evidencias**
- Capturas de pantalla de señales generadas en el dominio del tiempo y la frecuencia que evidencien cada una de las comparaciones realizadas.

---

## **Actividad 3: Transmisión y Medición de Señales con el USRP 2920**

### **Objetivo**
Transmitir señales usando el USRP 2920 y medir parámetros clave como potencia, ancho de banda, piso de ruido y relación señal a ruido (SNR).

### **Procedimiento**
1. **Configurar el USRP 2920**:
   - Configure el flujograma en GNU Radio para transmitir una señal a través del USRP. Habilite o deshabilite los bloques correspondientes (Channel Model, Throttle, UHD: USRP Sink, Virtual Sink). Para esto seleccione el bloque deseado y presionando `E` (enable) o `D` (disable), respectivamente.
   - Identifique el bloque de frecuencia de muestreo (samp_rate) y observe el efecto de cambiar su valor (e.g. 10 kHz).
   - Configure la frecuencia de muestreo (samp_rate) en 1 MHz.
   - Verifique el efecto de modificar la frecuencia y ganancia del USRP. 

2. **Medición con el Analizador de Espectros**:
   - Conecte la salida del USRP al analizador de espectros.
   - Mida el piso de ruido normalizado a la frecuencia de portadora que va a utilizar. --> DA -140dB. 
   - Compare el espectro de la señal observada en el analizador de espectros con la observada en la pantalla de simulación. Tenga en cuenta que el radio (USRP) equivale al diagrama de bloques mostrado en la figura.

<img src="qam_modulator.png" alt="QAM Modulator" width="400">
     
   - Analice y valide los resultados en el dominio de la frecuencia si se modifica:
     - el tipo de dato de la fuente (compleja o flotante)
     - la forma de onda 
     - la frecuencia y fase de la señal
     - la amplitud de la señal generada.
   - Mida potencia de la señal transmitida y ancho de banda de diferentes señales generadas.
   - Conecte una antena apropiada a la entrada del analizador de espectros y observe el espectro de una señal FM (las estaciones FM se sitúan entre los 88 MHz y 108 MHz). Mida su ancho de banda y relación señal a ruido. 
   - Determinar la máxima potencia de transmisión.
   - Evalúe la respuesta en frecuencia del canal midiendo los cambios de ganancia del sistema cuando varía la frecuencia de portadora.
   - Compare los resultados de transmitir usando un cable y usando antenas.

4. **Medición con el Osciloscopio**:
   - Analice y valide los resultados en el dominio del tiempo si se modifica:
     - el tipo de dato de la fuente (compleja o flotante)
     - la forma de onda 
     - la frecuencia y fase de la señal
     - la amplitud de la señal generada.
  - Contraste estos resultados con los obtenidos con el analizador de espectros.

5. **Cálculo de la Relación Señal a Ruido (SNR)**:
   - Usar las mediciones de potencia y piso de ruido para calcular la SNR de algunas de las señales generadas.
   - Anotar el valor de la SNR en dB.

### **Preguntas Orientadoras**
1. ¿Cómo se configura el USRP 2920 para transmitir una señal en una frecuencia específica?
2. ¿Qué parámetros del flujograma afectan la potencia de la señal transmitida?
3. ¿Cómo se mide el ancho de banda de la señal transmitida en el analizador de espectros?
4. ¿Cómo se calcula la relación señal a ruido (SNR) a partir de las mediciones de potencia y piso de ruido?
5. ¿Qué diferencias se observan en las mediciones de potencia cuando se varía la ganancia del USRP?
6. ¿Es posible medir o estimar la potencia de la señal observada en el osciloscopio? ¿Por qué?

### **Evidencia**
- Capturas de pantalla de señales generadas en el dominio del tiempo y la frecuencia que evidencien las principales comparaciones realizadas.
- Captura de la señal FM usada para medición de ancho de banda.

---

## **Actividad 4: Análisis de Resultados y Conclusiones**

### **Objetivo**
Analizar los resultados obtenidos y sacar conclusiones sobre el comportamiento de las señales en diferentes condiciones para elaborar el informe.

### **Para la Elaboración del Informe**
1. **Comparar Resultados**:
   - Compare los resultados obtenidos en las simulaciones y las transmisiones reales.
   - Discuta las diferencias entre las mediciones realizadas con el osciloscopio y el analizador de espectros.

2. **Reflexionar sobre la SNR**:
   - Analice la importancia de la relación señal a ruido (SNR) en las comunicaciones inalámbricas.
   - Discuta cómo el piso de ruido afecta la capacidad de detectar señales débiles.

3. **Conclusiones Finales**:
   - Escriba conclusiones basadas en los resultados obtenidos.
   - Reflexe sobre las limitaciones de los equipos y cómo se podrían mejorar las mediciones.

### **Preguntas Orientadoras**
1. ¿Qué conclusiones se pueden obtener sobre la relación entre la potencia de la señal y la calidad de la comunicación?
2. ¿Cómo afecta el piso de ruido a la capacidad de detectar señales débiles?
3. ¿Qué limitaciones tienen los equipos utilizados en términos de ancho de banda y precisión en las mediciones?
4. ¿Cómo se pueden mejorar las mediciones de señal en un entorno con alto nivel de ruido?
5. ¿Qué aplicaciones prácticas tienen las mediciones de potencia y ancho de banda en sistemas de comunicaciones reales?
6. ¿Cómo se puede medir la respuesta en frecuencia de un canal alámbrico?
7. ¿Cómo se puede obtener un modelo sencillo de las pérdidas (_pathloss_) en un canal inalámbrico?
