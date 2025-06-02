# Quantum Audio Processor 🎵⚛️

Aplicación de efectos de procesamiento de audio utilizando computación cuántica con Qiskit. Este proyecto implementa dos algoritmos cuánticos diferentes para modificar archivos de audio WAV.

## Características principales

- **Dos algoritmos cuánticos**:
  - `quantum_phase_modulation`: Modulación de fase basada en estados cuánticos
  - `quantum_modulation_enhanced`: Efecto mejorado con distorsión creativa basada en mediciones cuánticas

- **Efectos únicos**:
  - Distorsión armónica no lineal
  - Modulación de fase cuántica
  - Efectos basados en probabilidades de medición cuántica

- **Optimizaciones**:
  - Caché de resultados cuánticos
  - Submuestreo inteligente
  - Procesamiento eficiente de audio

## Requisitos

- Python 3.8+
- Dependencias:
  ```
  numpy
  qiskit
  qiskit-aer
  ```

Instalar dependencias con:
```bash
pip install numpy qiskit qiskit-aer
```

## Uso

1. Coloca tu archivo de audio WAV (16-bit o 32-bit) en el mismo directorio con nombre `audio.wav`

2. Ejecuta el procesador:
```bash
python main.py
```

3. El archivo procesado se guardará como `audio_quantico.wav`

### Parámetros ajustables

- `intensity` (0.1 a 1.0): Controla la intensidad del efecto
- `sample_rate`: Se ajusta automáticamente al archivo de entrada

## Algoritmos implementados

### 1. Quantum Phase Modulation
- Circuito de 1 qubit con compuertas Hadamard y Phase
- Modifica la fase de la señal basándose en simulaciones cuánticas
- Efecto: modulación de fase suave con características cuánticas

### 2. Enhanced Quantum Modulation
- Circuito de 1 qubit con compuerta RY y medición
- Usa probabilidades de medición para:
  - Modular amplitud
  - Aplicar distorsión no lineal
- Efecto: más pronunciado con características armónicas complejas

## Estructura del código

- `read_wav_file()`: Lee archivos WAV usando el módulo `wave`
- `write_wav_file()`: Escribe archivos WAV de 16-bit
- `main()`: Función principal que orquesta el procesamiento
- Manejo de errores con traceback completo

## Ejemplos de uso

Procesamiento con intensidad media:
```python
processed_audio = quantum_modulation_enhanced(audio, sample_rate, intensity=0.5)
```

Procesamiento con efecto de fase cuántica:
```python
processed_audio = quantum_phase_modulation(audio, sample_rate, intensity=0.3)
```

## Limitaciones

- Procesa solo el primer canal en archivos estéreo
- Submuestrea audio para mantener tiempos de procesamiento razonables
- Requiere archivos WAV con formato soportado (16-bit o 32-bit)

## Contribuciones

¡Contribuciones son bienvenidas! Algunas ideas:
- Implementar efectos cuánticos adicionales
- Mejorar la eficiencia del procesamiento
- Añadir soporte para más formatos de audio

## Licencia

Este proyecto está bajo licencia MIT.

## Circuitos Cuánticos Implementados

### 1. Circuito de Modulación de Fase Cuántica (`quantum_phase_modulation`)

```python
qc = QuantumCircuit(1)
qc.h(0)        # Hadamard
qc.p(theta, 0) # Compuerta de fase
```

**Compuertas utilizadas:**
- `Hadamard (H)`:
  - Crea superposición cuántica: |0⟩ → (|0⟩ + |1⟩)/√2
  - Matriz: 
    ```
    [1  1]
    [1 -1] * (1/√2)
    ```
  
- `Phase (P)`:
  - Aplica rotación de fase al estado |1⟩
  - Matriz:
    ```
    [1   0]
    [0 e^(iθ)]
    ```

**Flujo del circuito:**
1. Inicializa |0⟩
2. Aplica H para crear superposición
3. Aplica P(θ) para modificar la fase relativa
4. Mide el vector de estado resultante

### 2. Circuito de Modulación Mejorada (`quantum_modulation_enhanced`)

```python
qc = QuantumCircuit(1, 1)
qc.ry(theta, 0) # Rotación Y
qc.measure(0, 0) # Medición
```

**Compuertas utilizadas:**
- `RY(theta)`:
  - Rotación alrededor del eje Y
  - Matriz:
    ```
    [cos(θ/2)  -sin(θ/2)]
    [sin(θ/2)   cos(θ/2)]
    ```
  
- `Medición`:
  - Colapsa el estado cuántico a |0⟩ o |1⟩
  - Probabilidad P(0) = cos²(θ/2)
  - Probabilidad P(1) = sin²(θ/2)

**Flujo del circuito:**
1. Inicializa |0⟩
2. Aplica RY(θ) para rotación
3. Mide el qubit (256 shots)
4. Usa estadísticas de medición para modificar audio

## Diagramas de Circuitos

### Circuito de Modulación de Fase
```
     ┌───┐┌───────┐
q_0: ┤ H ├┤ P(θ) ├
     └───┘└───────┘
```

### Circuito de Modulación Mejorada
```
     ┌──────────┐┌─┐
q_0: ┤ RY(θ)[0] ├┤M├
     └──────────┘└╥┘
c: 1/═════════════╩═
                  0 
```

## Explicación Física de los Efectos

### Para Modulación de Fase:
1. El estado final es (|0⟩ + e^(iθ)|1⟩)/√2
2. La diferencia de fase θ se calcula como:
   ```python
   phase_diff = np.angle(statevector[1]) - np.angle(statevector[0])
   ```
3. Se aplica al audio como:
   ```python
   sample * np.exp(1j * phase_diff * intensity).real
   ```

### Para Modulación Mejorada:
1. Las probabilidades de medición modifican la amplitud:
   ```python
   sample * (1 + intensity * (p1 - p0))
   ```
2. Efectos no lineales adicionales cuando:
   - p1 > 0.7: Añade componente cúbica (`sample**3`)
   - p0 > 0.7: Añade componente cuadrática (`sample**2`)

## Parámetros Cuánticos

| Parámetro      | Descripción                          | Rango        | Efecto en el audio |
|----------------|--------------------------------------|--------------|--------------------|
| `theta`        | Ángulo de rotación                   | [0, π]       | Controla intensidad |
| `intensity`    | Factor de escala del efecto          | [0.1, 1.0]   | Ajusta fuerza modulación |
| `shots`        | Número de mediciones (solo enhanced) | 256 (fijo)   | Suaviza estadísticas |

## Relación Audio-Cuántica

Cada muestra de audio se mapea a:
```python
angle = np.arcsin(np.clip(np.abs(sample), 0, 1)) * intensity * np.pi
```

Este ángulo controla:
- La rotación de fase en `quantum_phase_modulation`
- La rotación Y en `quantum_modulation_enhanced`

Los efectos cuánticos producen:
- Distorsión armónica no lineal
- Modulación de fase dependiente de amplitud
- Efectos de "chorus" cuántico cuando intensity > 0.5