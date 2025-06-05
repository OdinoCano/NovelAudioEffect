# Quantum Audio Processor 🎵⚛️

Aplicación de efectos de procesamiento de audio utilizando computación cuántica con Qiskit. Este proyecto implementa cuatro algoritmos cuánticos diferentes para modificar archivos de audio WAV y generar efectos únicos basados en probabilidades y fases cuánticas.

---

## 🧩 Características principales

- **Cuatro algoritmos cuánticos**:
  1. `quantum_harmonic_frqi_modulation`: Versión avanzada con efectos auditivos mejorados (solapamiento, corrección de fase, entrelazamiento y filtrado adaptativo).
  2. `quantum_frqi_modulation`: Implementación básica de FRQI (Flexible Representation of Quantum Images) aplicada a audio.
  3. `quantum_modulation_enhanced`: Modulación perceptual mejorada con distorsión creativa basada en mediciones cuánticas (RY + medición).
  4. `quantum_phase_modulation`: Modulación de fase cuántica utilizando un circuito parametrizado de Hadamard + Phase.

- **Efectos auditivos avanzados**:
  - Distorsión armónica no lineal basada en desequilibrio cuántico.
  - Modulación de fase dependiente de amplitud, con características espaciales suaves.
  - Solapamiento (Overlap) con ventana de Hanning para transiciones más naturales.
  - Corrección de fase para reducir artefactos en estados cuánticos.
  - Entrelazamiento simulado (qubits adicionales) para mejorar coherencia temporal.
  - Filtrado adaptativo espectral con FFT y ventana Hamming para realce dinámico.

- **Optimizaciones de rendimiento**:
  - Caché de resultados cuánticos (ángulos o fases) para evitar simulaciones redundantes.
  - Submuestreo adaptativo según la frecuencia de muestreo de entrada.
  - Procesamiento en chunks (porciones) para manejo eficiente de memoria.
  - Manejo inteligente de memoria: lectura/escritura por bloques y “forward fill” para interpolación de muestras faltantes.

- **Formato compatible**:
  - Archivos WAV mono o estéreo, 16-bit o 32-bit PCM.
  - Solo primer canal de audio en caso de estéreo.

---

## 📦 Requisitos

- Python 3.8 o superior  
- Dependencias:
```bash
  pip install numpy qiskit qiskit-aer
```

* Módulo estándar `wave` (normalmente incluido en la instalación base de Python).

---

## 🚀 Uso básico

1. **Coloca tu archivo WAV**
   Asegúrate de tener un archivo llamado `audio.wav` (16-bit o 32-bit) en el mismo directorio que `main.py` o `quantum_audio.py`.

2. **Ejecuta el procesador desde línea de comandos**

   ```bash
   python main.py
   ```

   * El script leerá `audio.wav`, aplicará el algoritmo cuántico predeterminado (`quantum_harmonic_frqi_modulation` con parámetros por defecto) y guardará el resultado en `audio_quantico.wav`.
   * Mensajes informativos imprimirán la longitud de la señal, la frecuencia de muestreo y el progreso del procesamiento.

3. **Ajusta parámetros en `main.py`**
   Dentro de la función `main()`, puedes cambiar:

   ```python
   intensity = 1.0    # Intensidad del efecto (0.1 a 1.0)
   # Seleccionar algoritmo:
   processed_audio = quantum_harmonic_frqi_modulation(audio, sample_rate, intensity,
                                                      overlap=True,
                                                      phase_correction=True,
                                                      entanglement=True,
                                                      adaptive_filter=True)
   # o bien:
   processed_audio = quantum_modulation_enhanced(audio, sample_rate, intensity)
   # o:
   processed_audio = quantum_phase_modulation(audio, sample_rate, intensity)
   ```

   * El resultado se guarda en `audio_quantico.wav` por defecto.

---

## ⚙️ Parámetros configurables

| Parámetro          | Valores      | Efecto                                    |
| ------------------ | ------------ | ----------------------------------------- |
| `intensity`        | 0.0 – 1.0    | Fuerza global del efecto cuántico         |
| `overlap`          | True / False | Activa solapamiento (Overlap)             |
| `phase_correction` | True / False | Corrige artefactos de fase cuántica       |
| `entanglement`     | True / False | Simula qubits adicionales para FRQI       |
| `adaptive_filter`  | True / False | Aplica filtrado adaptativo espectral      |
| `step` (interno)   | int          | Submuestreo adaptativo según sample\_rate |

---

## 🔍 Algoritmos implementados

### 1. Quantum Harmonic FRQI Modulation

```python
quantum_harmonic_frqi_modulation(audio_data, sample_rate,
                                 intensity=0.5,
                                 overlap=False,
                                 phase_correction=False,
                                 entanglement=False,
                                 adaptive_filter=False)
```

* **Descripción**:

  * Divide la señal normalizada en chunks de tamaño base 256 (2⁸ qubits de posición).
  * Mapea cada muestra a un ángulo θ = (normalized + 1)/2 · (π/2).
  * Construye estado FRQI: |ψ⟩ = ∑ᵢ cos(θᵢ)|0⟩|i⟩ + sin(θᵢ)|1⟩|i⟩, con normalización 1/√chunk\_size.
  * Aplica un Hadamard en el qubit de amplitud para generar interferencia.
  * Decodifica probabilidades p₀, p₁ y calcula nueva amplitud invertiendo FRQI:

    ```python
    cond_p1 = p1 / (p0 + p1)
    new_theta = arcsin(√cond_p1)
    new_amp = 2*(new_theta/ (π/2)) - 1
    ```
  * Mezcla con la señal original usando `intensity`.
  * Opciones avanzadas:

    * **overlap**: reduce el chunk\_size a 75% y superpone con ventana Hanning de 64 muestras, desplazada 32 muestras (solapamiento 50%).
    * **phase\_correction**: ajusta fase relativa entre amplitud |0⟩ y |1⟩ antes de Hadamard.
    * **entanglement**: incrementa el chunk\_size en 5 qubits adicionales (carácter demostrativo de “entrelazamiento”).
    * **adaptive\_filter**: precalcula perfil espectral (FFT + ventana Hamming en primeras 4096 muestras) y pondera las nuevas amplitudes según peso espectral.

* **Efectos auditivos**: enriquecimiento armónico, suavizado de transiciones, coherencia temporal mejorada y realce o supresión de bandas según perfil espectral.

---

### 2. Quantum FRQI Modulation (versión básica)

```python
quantum_frqi_modulation(audio_data, sample_rate, intensity=0.5)
```

* **Descripción**:

  * Implementa únicamente los pasos básicos de FRQI sin opciones avanzadas.
  * Chunk\_size fijo de 256.
  * Mapea a ángulos θ, construye estado FRQI y aplica Hadamard en qubit de amplitud.
  * Decodifica probabilidades y genera nueva amplitud mezclada con la original según `intensity`.
* **Casos de uso**:

  * Punto de partida para comparar resultados con la versión avanzada.
  * Menor carga computacional al no incluir sobrelap, corrección de fase, entanglement ni filtrado adaptativo.

---

### 3. Enhanced Quantum Modulation

```python
quantum_modulation_enhanced(audio_data, sample_rate, intensity=0.5)
```

* **Descripción**:

  * Para cada muestra (o submuestra según submuestreo adaptativo), calcula ángulo θ = arcsin(clamp(sample, -1, 1)) · π.
  * Construye circuito de 1 qubit:

    ```python
    qc = QuantumCircuit(1, 1)
    qc.ry(angle, 0)
    qc.measure(0, 0)
    ```
  * Transpila el circuito al simulador AerSimulator y ejecuta 256 shots.
  * Calcula probabilidades p₀ = counts(“0”)/256, p₁ = counts(“1”)/256 y guarda en caché.
  * Modulación de amplitud:

    ```python
    mod_sample = sample * (1 + intensity * (p1 - p0))
    ```
  * Distorsión creativa:

    * Si p₁ > 0.7, añade componente cúbica: `mod_sample += intensity * (sample**3)`.
    * Si p₀ > 0.7, añade componente cuadrática negativa: `mod_sample -= intensity * (sample**2)`.
  * Interpola muestras faltantes (forward fill) para mantener continuidad.
* **Efectos auditivos**:

  * Distorsión armónica pronunciada (efecto de saturación controlada).
  * Texturas no lineales basadas en resultados de medición cuántica.
  * Características de “chorus” cuando `intensity > 0.5`.

---

### 4. Quantum Phase Modulation

```python
quantum_phase_modulation(audio_data, sample_rate, intensity=0.5)
```

* **Descripción**:

  * Normaliza audio a \[-1, 1].
  * Circuito de 1 qubit parametrizado con θ:

    ```python
    theta = Parameter('θ')
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.p(theta, 0)
    qc.save_statevector()
    ```
  * Transpila al simulador AerSimulator y guarda vino de estado.
  * Para cada submuestra (según submuestreo adaptativo), calcula ángulo:

    ```python
    angle = arcsin(|sample|) · intensity · π
    ```
  * Asigna parámetro y simula con shots=1 para obtener vector de estado |ψ⟩.
  * Calcula diferencia de fase Δϕ = arg(⟨1|ψ⟩) - arg(⟨0|ψ⟩).
  * Modula la muestra como:

    ```python
    processed[i] = sample * real(exp(i · Δϕ · intensity))
    ```
  * Interpolación de forward fill para muestras faltantes.
* **Efectos auditivos**:

  * Modulación de fase suave, creando sensaciones de espacialidad y variaciones tonales sutiles.
  * Artefactos de fase controlados según intensidad.

---

## 🔧 Estructura del código

```text
quantum_audio/
│
├── quantum_audio.py       # Implementación completa de todos los algoritmos
├── main.py                # Script principal para ejecutar el procesamiento a partir de audio.wav
├── example_usage.py       # Ejemplos de llamadas a funciones desde Python
├── README.md              # Este archivo de documentación
└── requirements.txt       # Lista de dependencias (numpy, qiskit, qiskit-aer)
```

* **`quantum_audio.py`**

  * Contiene las funciones:

    * `read_wav_file(filename)`
    * `write_wav_file(filename, sample_rate, audio_data)`
    * `quantum_harmonic_frqi_modulation(...)`
    * `quantum_frqi_modulation(...)`
    * `quantum_modulation_enhanced(...)`
    * `quantum_phase_modulation(...)`

* **`main.py`**

  * Punto de entrada:

    1. Lee `audio.wav` con `read_wav_file()`.
    2. Convierte audio a `numpy.float32` si es necesario.
    3. Llama a uno de los algoritmos con parámetros configurables.
    4. Guarda resultado con `write_wav_file('audio_quantico.wav', sample_rate, processed_audio)`.
    5. Maneja excepciones mostrando traceback completo.

* **`example_usage.py`** (opcional)

  * Muestra ejemplos de uso directo en un REPL o en otro script:

    ```python
    from quantum_audio import *
    sample_rate, audio = read_wav_file('input.wav')
    processed = quantum_modulation_enhanced(audio, sample_rate, intensity=0.3)
    write_wav_file('output.wav', sample_rate, processed)
    ```

---

## 📂 Ejemplos de uso

### 1. Procesamiento con intensidad media

```python
from quantum_audio import quantum_modulation_enhanced, read_wav_file, write_wav_file

sr, audio = read_wav_file('audio.wav')
processed = quantum_modulation_enhanced(audio, sr, intensity=0.5)
write_wav_file('audio_quantico.wav', sr, processed)
```

### 2. Modulación de fase cuántica suave

```python
from quantum_audio import quantum_phase_modulation, read_wav_file, write_wav_file

sr, audio = read_wav_file('audio.wav')
processed = quantum_phase_modulation(audio, sr, intensity=0.3)
write_wav_file('audio_quantico_fase.wav', sr, processed)
```

### 3. Versión FRQI básica sin efectos

```python
from quantum_audio import quantum_frqi_modulation, read_wav_file, write_wav_file

sr, audio = read_wav_file('audio.wav')
processed = quantum_frqi_modulation(audio, sr, intensity=0.7)
write_wav_file('audio_quantico_frqi.wav', sr, processed)
```

---

## ⚠️ Limitaciones

* Solo procesa el **primer canal** de archivos estéreo.
* Submuestrea el audio para reducir la carga computacional; esto puede generar artefactos si se usan valores altos de `sample_rate` distintos de 44100 Hz.
* No hay soporte para formatos distintos a WAV (MP3, FLAC, etc.).
* Requiere simulación cuántica en CPU (puede ser lento si se usa sin caché y con muchos shots).
* Para `quantum_phase_modulation`, si el simulador no retorna el statevector, se usa un fallback analítico.

---

## 🛠️ Contribuciones

¡Las contribuciones son bienvenidas! Áreas sugeridas:

* Soporte para **GPU** (Qiskit GPU) o aceleradores cuánticos reales.
* Añadir efectos cuánticos adicionales (por ejemplo, rotaciones X o Z paramétricas).
* Optimizar rendimiento (paralelización, vectorización de NumPy).
* Implementar soporte para **formatos de audio adicionales** (MP3, FLAC, OGG).
* Desarrollar una **interfaz gráfica (GUI)** para configuración en tiempo real.
* Agregar una **pipeline de tests unitarios** y **CI/CD**.

Para contribuir:

1. Haz un fork del repositorio.
2. Crea una rama con tu mejora: `git checkout -b mejora-nueva-funcionalidad`.
3. Realiza commits descriptivos.
4. Envía un pull request describiendo los cambios y su impacto.

---

## 📜 Licencia

Este proyecto está bajo licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.

---

## 📐 Diagramas de Circuitos

### 1. Circuito de Modulación de Fase (`quantum_phase_modulation`)

```
     ┌───┐┌───────┐
q_0: ┤ H ├┤ P(θ) ├
     └───┘└───────┘
```

* **Hadamard (H)**: crea superposición
* **Phase (P(θ))**: aplica rotación de fase en el estado |1⟩
* **save\_statevector()**: obtiene vector de estado para extraer diferencia de fase

---

### 2. Circuito de Modulación Mejorada (`quantum_modulation_enhanced`)

```
     ┌──────────┐┌─┐
q_0: ┤ RY(θ)[0] ├┤M├
     └──────────┘└╥┘
c: 1/═════════════╩═
                  0 
```

* **RY(θ)**: rotación alrededor del eje Y
* **Measurement (M)**: colapsa a |0⟩ o |1⟩ en 256 shots
* Se usa estadística para modular amplitud y agregar distorsión no lineal

---

## 🔬 Explicación Física de los Efectos

### Modulación de Fase Cuántica

1. Estado inicial: |0⟩
2. Aplica Hadamard → (|0⟩ + |1⟩)/√2
3. Aplica P(θ) → (|0⟩ + e^(iθ)|1⟩)/√2
4. Se extrae diferencia de fase Δϕ = arg(|1⟩) − arg(|0⟩).
5. Se modula señal de audio:

   ```python
   sample * real(exp(i · Δϕ · intensity))
   ```

   – Crea un efecto de desplazamiento de fase controlado, generando sensaciones de espacialidad y ligeras variaciones tonales.

### Enhanced Quantum Modulation

1. Rotación RY(θ) sobre |0⟩, donde θ = arcsin(|sample|) · π.
2. Medición en base computacional (|0⟩, |1⟩) con 256 shots:

   * P(0) = cos²(θ/2)
   * P(1) = sin²(θ/2)
3. Se usa desequilibrio (p₁ − p₀) para cambiar la amplitud:

   ```python
   sample * (1 + intensity * (p1 - p0))
   ```
4. Si p₁ > 0.7 → añade componente cúbica (`sample**3`), generando saturación armónica.
   Si p₀ > 0.7 → añade componente cuadrática negativa (`sample**2`), generando distorsión suave.
5. Resultado final: combinación de modulación lineal/perceptual y distorsión armónica adaptada a la probabilidad cuántica.

---

## 🔢 Parámetros Cuánticos

| Parámetro     | Descripción                                             | Rango         | Efecto en el audio                                               |
| ------------- | ------------------------------------------------------- | ------------- | ---------------------------------------------------------------- |
| `theta`       | Ángulo de rotación (quantum\_phase\_modulation o RY)    | \[0, π]       | Controla la fase o amplitud inicial asignada a cada muestra      |
| `intensity`   | Factor de escala global del efecto                      | \[0.1, 1.0]   | Ajusta la fuerza de cualquier modulación cuántica aplicada       |
| `shots`       | Número de mediciones (solo para enhanced, fijo en 256)  | 256           | Mayor precisión estadística en probabilidades de medición        |
| `chunk_size`  | Tamaño de bloque para FRQI (256 base + ajustes)         | 256 ± ajustes | Define cuántos qubits de posición se simulan y afecta resolución |
| `sample_rate` | Frecuencia de muestreo del archivo WAV (p.ej. 44100 Hz) | 8000 – 96000  | Determina el submuestreo adaptativo y la granularidad temporal   |

---

## 🎛️ Relación Audio ↔ Cuántica

Cada muestra de audio (valor en \[−1, 1]) se mapea a un ángulo cuántico:

```python
angle = np.arcsin(np.clip(np.abs(sample), 0, 1)) * intensity * π
```

* En **quantum\_phase\_modulation**, este ángulo se usa para la compuerta `P(θ)` después de un Hadamard, y la diferencia de fase Δϕ modula la muestra compleja.
* En **quantum\_modulation\_enhanced**, el mismo ángulo sirve como parámetro para `RY(θ)`, y las estadísticas de medición controlan amplitud y distorsión.

El resultado es un efecto auditivo que combina técnicas de procesamiento clásico (ventaneo, filtrado, mezcla) con propiedades propias de la interferencia y probabilidad cuántica, logrando:

* Enriquecimiento armónico inesperado
* Transiciones más suaves en transitorios cortos
* Sensación de espacialidad y “chorus” cuántico cuando `intensity > 0.5`
* Texturas sonoras complejas con “decodes” probabilísticas

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Revisa el archivo `LICENSE` para más detalles.

---

## 👤 Autor

Proyecto creado por un entusiasta de la computación cuántica y el procesamiento de audio.
Contribuciones, sugerencias y mejoras son bienvenidas.

---