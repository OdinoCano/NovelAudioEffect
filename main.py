import numpy as np
import wave
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit import Parameter

def quantum_frqi_modulation(audio_data, sample_rate, intensity=0.5):
    max_val = np.max(np.abs(audio_data))
    if max_val == 0:
        return audio_data
    
    audio_norm = audio_data.astype(np.float32) / max_val
    chunk_size = 256  # 2^8 qubits de posición
    num_chunks = (len(audio_norm) + chunk_size - 1) // chunk_size
    processed = np.zeros(num_chunks * chunk_size)
    
    for chunk_idx in range(num_chunks):
        start = chunk_idx * chunk_size
        end = min(start + chunk_size, len(audio_norm))
        chunk = audio_norm[start:end]
        
        if len(chunk) < chunk_size:
            padded_chunk = np.zeros(chunk_size)
            padded_chunk[:len(chunk)] = chunk
            chunk = padded_chunk
        
        # Paso 1: Mapeo a ángulos FRQI
        normalized_chunk = (chunk + 1) / 2.0
        theta = normalized_chunk * (np.pi / 2)
        
        # Paso 2: Construir estado FRQI
        state_vector = np.zeros(2 * chunk_size, dtype=complex)
        norm_factor = 1.0 / np.sqrt(chunk_size)
        for i in range(chunk_size):
            state_vector[i] = np.cos(theta[i]) * norm_factor
            state_vector[chunk_size + i] = np.sin(theta[i]) * norm_factor
        
        # Paso 3: Operación cuántica (Hadamard en qubit de amplitud)
        for i in range(chunk_size):
            index0 = i
            index1 = chunk_size + i
            vec0 = state_vector[index0]
            vec1 = state_vector[index1]
            state_vector[index0] = (vec0 + vec1) / np.sqrt(2)
            state_vector[index1] = (vec0 - vec1) / np.sqrt(2)
        
        # Paso 4: Decodificación y aplicación de intensidad
        new_chunk = np.zeros(chunk_size)
        for i in range(chunk_size):
            p0 = np.abs(state_vector[i])**2
            p1 = np.abs(state_vector[chunk_size + i])**2
            total = p0 + p1
            
            if total < 1e-10:
                cond_p1 = 0.5
            else:
                cond_p1 = p1 / total
            
            cond_p1 = np.clip(cond_p1, 0, 1)
            new_theta = np.arcsin(np.sqrt(cond_p1))
            new_normalized = new_theta / (np.pi / 2)
            new_amp = 2 * new_normalized - 1
            
            # Aplica intensidad como mezcla con señal original
            new_chunk[i] = (1 - intensity) * chunk[i] + intensity * new_amp
        
        # Manejo del último chunk (despadding)
        valid_length = end - start
        if chunk_idx == num_chunks - 1 and valid_length < chunk_size:
            processed[start:end] = new_chunk[:valid_length] * max_val
        else:
            processed[start:start+chunk_size] = new_chunk * max_val
    
    return processed[:len(audio_data)]

def quantum_modulation_enhanced(audio_data, sample_rate, intensity=0.5):
    max_val = np.max(np.abs(audio_data))
    if max_val == 0:
        return audio_data
    audio_norm = audio_data.astype(np.float32) / max_val

    # Circuito base con parámetro
    qc = QuantumCircuit(1, 1)
    theta = np.pi  # Placeholder
    qc.ry(theta, 0)
    qc.measure(0, 0)

    simulator = AerSimulator()
    step = max(1, int(sample_rate / 44100))  # Submuestreo: uno por cada frame de audio real
    processed = np.zeros(len(audio_norm))

    # Cache de resultados
    result_cache = {}

    # Transpilar una vez
    qc_compiled = transpile(qc, simulator)

    for i in range(0, len(audio_norm), step):
        sample = audio_norm[i]
        angle = np.arcsin(np.clip(sample, -1, 1)) * np.pi  # ∈ [-π/2, π/2]

        # Cache
        if angle in result_cache:
            p0, p1 = result_cache[angle]
        else:
            # Clonar circuito y reemplazar parámetro
            custom_qc = QuantumCircuit(1, 1)
            custom_qc.ry(angle, 0)
            custom_qc.measure(0, 0)
            compiled = transpile(custom_qc, simulator)

            job = simulator.run(compiled, shots=256)
            result = job.result()
            counts = result.get_counts()

            p0 = counts.get('0', 0) / 256
            p1 = counts.get('1', 0) / 256

            result_cache[angle] = (p0, p1)

        # 🎧 Modulación perceptual más notoria
        # 1. Amplitud modulada por desequilibrio cuántico
        mod_sample = sample * (1 + intensity * (p1 - p0))

        # 2. Distorsión creativa si hay dominancia cuántica de 1
        if p1 > 0.7:
            mod_sample += intensity * (sample ** 3)
        elif p0 > 0.7:
            mod_sample -= intensity * (sample ** 2)

        processed[i] = np.clip(mod_sample, -1, 1)

    # Interpolación hacia los huecos (simple forward fill)
    for i in range(1, len(processed)):
        if processed[i] == 0:
            processed[i] = processed[i - 1]

    return processed * max_val

def quantum_phase_modulation(audio_data, sample_rate, intensity=0.5):
    # Normalizar audio a [-1, 1]
    max_val = np.max(np.abs(audio_data))
    if max_val == 0:
        return audio_data
    audio_norm = audio_data.astype(np.float32) / max_val
    
    # Crear circuito cuántico parametrizado
    theta = Parameter('θ')
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.p(theta, 0)  # Compuerta de fase
    
    # IMPORTANTE: Guardar el vector de estado
    qc.save_statevector()
    
    # Configurar simulador cuántico
    simulator = AerSimulator()
    
    # Transpilar circuito una sola vez
    transpiled_qc = transpile(qc, simulator)
    
    # Precalcular valores para evitar simulaciones redundantes
    phase_cache = {}
    
    # Procesar muestras
    step = max(1, int(sample_rate / 44100))  # Submuestreo para eficiencia
    processed = np.zeros(len(audio_norm))
    
    for i in range(0, len(audio_norm), step):
        sample = audio_norm[i]
        angle = np.arcsin(np.clip(np.abs(sample), 0, 1)) * intensity * np.pi
        
        # Usar caché para evitar simulaciones repetidas
        if angle not in phase_cache:
            # Asignar valor al parámetro
            bound_qc = transpiled_qc.assign_parameters({theta: angle})
            
            # Simular circuito cuántico
            job = simulator.run(bound_qc, shots=1)
            result = job.result()
            
            # Obtener el vector de estado (forma corregida)
            statevector = result.data(0).get('statevector')
            
            if statevector is None:
                # Fallback: cálculo analítico
                phase0 = 0
                phase1 = angle
            else:
                # Calcular fases
                phase0 = np.angle(statevector[0])
                phase1 = np.angle(statevector[1])
            
            phase_diff = phase1 - phase0
            phase_cache[angle] = phase_diff
        
        # Aplicar modulación de fase
        processed[i] = sample * np.exp(1j * phase_cache[angle] * intensity).real
    
    # Interpolar muestras faltantes
    for i in range(1, len(processed)):
        if processed[i] == 0 and i > 0:
            processed[i] = processed[i-1]
    
    return processed * max_val

# Función para leer archivos WAV
def read_wav_file(filename):
    with wave.open(filename, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        audio_data = wav_file.readframes(n_frames)
        sample_width = wav_file.getsampwidth()
        
        # Convertir bytes a numpy array
        if sample_width == 2:
            dtype = np.int16
        elif sample_width == 4:
            dtype = np.int32
        else:
            raise ValueError(f"Ancho de muestra no soportado: {sample_width} bytes")
        
        audio = np.frombuffer(audio_data, dtype=dtype)
        return sample_rate, audio

# Función para guardar archivos WAV
def write_wav_file(filename, sample_rate, audio_data):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.astype(np.int16).tobytes())

# Procesamiento principal
def main():
    input_file = 'audio.wav'
    output_file = 'audio_quantico.wav'
    intensity = 0.7  # Intensidad del efecto (0.1 a 1.0)
    
    try:
        # Leer archivo de audio
        sample_rate, audio = read_wav_file(input_file)
        print(f"Audio cargado: {len(audio)} muestras a {sample_rate/1000} kHz")
        
        # Si es estéreo, usar solo el primer canal
        if audio.ndim > 1:
            audio = audio[:, 0]
        elif audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Aplicar efecto cuántico
        print("Procesando audio con efecto cuántico...")
        processed_audio = quantum_frqi_modulation(audio, sample_rate, intensity)
        
        # Guardar resultado
        write_wav_file(output_file, sample_rate, processed_audio)
        print(f"Audio procesado guardado en: {output_file}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()