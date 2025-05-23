from machine import ADC, Pin

# Configuración del pin ADC para el AD8232 (ECG)
ecg_signal = ADC(Pin(34))  # GPIO 34
ecg_signal.width(ADC.WIDTH_12BIT)  # 12 bits de resolución (0-4095)
ecg_signal.atten(ADC.ATTN_11DB)    # Rango hasta 3.3V

def read_adc_sigle():
    """ Lee la señal del sensor ECG y devuelve un diccionario """
    return {
        "ecg": ecg_signal.read()
    }
