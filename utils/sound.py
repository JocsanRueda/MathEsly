import numpy as np
from scipy.io.wavfile import write
import os

# Frecuencias de referencia para las notas de la 4ª octava (A4 = 440 Hz)
# Do, Re, Mi, Fa, Sol, La, Si
PIANO_NOTES_FREQ = {
    "C4": 261.63,  # Do4
    "D4": 293.66,  # Re4
    "E4": 329.63,  # Mi4
    "F4": 349.23,  # Fa4
    "G4": 392.00,  # Sol4
    "A4": 440.00,  # La4
    "B4": 493.88,  # Si4
}
# Orden de las notas para el mapeo por índice
NOTE_ORDER = ["C", "D", "E", "F", "G", "A", "B"]

# --- Función para generar y guardar tonos con envolvente ADSR y armónicos ---
def generate_tone(frequency, duration_sec, sample_rate=44100, full_filename="temp_tone.wav"):
    """
    Genera una onda base con armónicos, aplica una envolvente ADSR 
    para un sonido más similar al de un piano (más limpio), y la guarda como un archivo .wav.
    """
    if frequency <= 0: 
        print(f"Advertencia: Frecuencia no válida ({frequency} Hz), no se generará sonido.")
        return None
    
    num_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, num_samples, False)
    
    # 1. Generar la onda base con armónicos (síntesis aditiva simple)
    wave = 1.0 * np.sin(frequency * t * 2 * np.pi)
    harmonics_params = [
        (2, 0.5),  # 2do armónico, amplitud ajustada
        (3, 0.3),  # 3er armónico, amplitud ajustada
        (4, 0.2),  # 4to armónico, amplitud ajustada
        (5, 0.1)   # 5to armónico, amplitud ajustada
    ]
    
    for multiple, amplitude_factor in harmonics_params:
        wave += amplitude_factor * np.sin(multiple * frequency * t * 2 * np.pi)

    max_wave_abs = np.max(np.abs(wave))
    if max_wave_abs > 0:
        wave /= max_wave_abs
    
    # 2. Crear una envolvente ADSR para un sonido más limpio/percusivo
    attack_time = 0.005  # Ataque muy rápido
    decay_time = 0.08    # Decaimiento corto
    sustain_level = 0.1  # Nivel de sustain MUY bajo para un sonido limpio
    release_time = 0.05  # Liberación rápida

    # Ajustar tiempos de envolvente si la duración total es muy corta
    # Esta lógica intenta preservar el carácter percusivo incluso para notas cortas.
    if duration_sec < (attack_time + decay_time + release_time):
        # Si es muy corto, priorizar ataque y un decaimiento/liberación rápidos
        attack_time = min(attack_time, duration_sec * 0.1)
        decay_time = min(decay_time, duration_sec * 0.4)
        release_time = duration_sec - attack_time - decay_time
        if release_time < 0: # Si aún no cabe
            decay_time = duration_sec - attack_time
            release_time = 0
        if decay_time < 0: # Si solo cabe el ataque
            attack_time = duration_sec
            decay_time = 0
        sustain_level = 0.05 # Aún más bajo para notas muy cortas

    if attack_time < 0: attack_time = 0
    if decay_time < 0: decay_time = 0
    if release_time < 0: release_time = 0
    
    envelope = np.zeros(num_samples)
    
    # Attack
    attack_samples = int(sample_rate * attack_time)
    if attack_samples > num_samples: attack_samples = num_samples
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay
    decay_samples = int(sample_rate * decay_time)
    if attack_samples + decay_samples > num_samples: decay_samples = num_samples - attack_samples
    sustain_start_sample = attack_samples 
    if decay_samples > 0 :
        envelope[sustain_start_sample : sustain_start_sample + decay_samples] = np.linspace(1, sustain_level, decay_samples)
    
    # Sustain y Release
    sustain_phase_start_sample = attack_samples + decay_samples
    release_samples = int(sample_rate * release_time)
    if sustain_phase_start_sample + release_samples > num_samples: 
        release_samples = num_samples - sustain_phase_start_sample
        if release_samples < 0: release_samples = 0 # Asegurar que no sea negativo

    sustain_only_samples = num_samples - sustain_phase_start_sample - release_samples
    if sustain_only_samples < 0: sustain_only_samples = 0 # Asegurar que no sea negativo
    
    if sustain_only_samples > 0:
        envelope[sustain_phase_start_sample : sustain_phase_start_sample + sustain_only_samples] = sustain_level
    
    if release_samples > 0:
        release_start_sample = sustain_phase_start_sample + sustain_only_samples
        # Asegurar que el índice de fin no exceda el tamaño del array
        end_release_sample = min(release_start_sample + release_samples, num_samples)
        actual_release_samples_count = end_release_sample - release_start_sample

        if actual_release_samples_count > 0 :
             envelope[release_start_sample : end_release_sample] = np.linspace(sustain_level, 0, actual_release_samples_count)
        # Si no hay espacio para linspace (ej. actual_release_samples_count es 0 o 1),
        # el último punto de la envolvente debería ser 0 si es posible.
        elif end_release_sample == num_samples and num_samples > 0:
             envelope[num_samples-1] = 0


    # Corrección final si la duración es extremadamente corta y la envolvente es cero
    if num_samples > 0 and np.sum(envelope) == 0: 
        envelope[:] = sustain_level * 0.5 # Un nivel muy bajo si todo falló

    # 3. Aplicar la envolvente a la onda compuesta
    sound_wave = wave * envelope
    
    # Normalizar el audio final a 16-bit PCM
    max_abs_sound = np.max(np.abs(sound_wave))
    if max_abs_sound == 0: 
        audio = np.zeros_like(sound_wave, dtype=np.int16) 
    else:
        audio = sound_wave * (2**15 - 1) / max_abs_sound
        audio = audio.astype(np.int16)
    
    try:
        write(full_filename, sample_rate, audio)
        return full_filename
    except Exception as e:
        print(f"Error writing WAV file {full_filename}: {e}")
        return None

# --- Función para generar notas de piano (usa la `generate_tone` mejorada) ---
def generate_piano_note_wav(
    input_value, 
    duration_sec=0.3, # Duración ajustada para un sonido más limpio
    output_dir="assets/sounds"
):
    """
    Genera un archivo .wav correspondiente a una nota de piano (Do-Si)
    basada en el input_value. La octava también varía con el input_value.
    Utiliza generate_tone que ahora aplica una envolvente ADSR y armónicos para un sonido más limpio.
    Crea el archivo en el output_dir especificado.
    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Directorio creado: {output_dir}")
        except OSError as e:
            print(f"No se pudo crear el directorio {output_dir}: {e}")
            return None

    note_index = int(input_value) % 7
    selected_note_name = NOTE_ORDER[note_index]
    
    base_freq_key = selected_note_name + "4"
    if base_freq_key not in PIANO_NOTES_FREQ:
        print(f"Error: Clave de frecuencia base '{base_freq_key}' no encontrada en PIANO_NOTES_FREQ.")
        return None
    base_frequency = PIANO_NOTES_FREQ[base_freq_key]

    octave_cycle = (int(input_value) // 7) % 3 
    
    actual_octave_number = 4 
    octave_multiplier = 1.0
    if octave_cycle == 0: 
        octave_multiplier = 0.5 
        actual_octave_number = 3
    elif octave_cycle == 1: 
        octave_multiplier = 1.0
        actual_octave_number = 4
    else: 
        octave_multiplier = 2.0
        actual_octave_number = 5
        
    final_frequency = base_frequency * octave_multiplier
    
    if final_frequency <= 0:
        print(f"Advertencia: Frecuencia final calculada no válida ({final_frequency} Hz) para input {input_value}.")
        return None

    filename = f"s_val_{int(input_value)}.wav" 
    full_file_path = os.path.join(output_dir, filename)

    return generate_tone(
        frequency=final_frequency,
        duration_sec=duration_sec,
        full_filename=full_file_path
    )

if __name__ == '__main__':
    # --- Ejemplo de uso para probar las funciones ---
    print("Generando sonidos de prueba (versión más limpia)...")
    
    test_output_dir = "test_piano_sounds_cleaner" 
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)

    valores_de_prueba = [0, 1, 2, 7, 8, 14, 15] 
    
    for val in valores_de_prueba:
        print(f"\nGenerando nota para el valor: {val}")
        # Usar una duración un poco mayor para la prueba individual para poder escucharla bien
        path = generate_piano_note_wav(val, duration_sec=0.5, output_dir=test_output_dir) 
        if path:
            print(f"Sonido de prueba generado: {path}")
        else:
            print(f"Fallo al generar sonido para el valor: {val}")
    
    print("\nGenerando tono simple de prueba (A4 = 440Hz) con armónicos y envolvente más limpia...")
    path_tono_simple = generate_tone(440, 0.5, full_filename=os.path.join(test_output_dir, "tono_A4_440hz_cleaner_adsr.wav"))
    if path_tono_simple:
        print(f"Tono simple de prueba generado: {path_tono_simple}")
    else:
        print("Fallo al generar tono simple de prueba.")
        
    print(f"\nPruebas completadas. Revisa la carpeta '{test_output_dir}'.")

