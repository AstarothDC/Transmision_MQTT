from machine import ADC, Pin

# Configuración de los 3 canales ADC
electrode1 = ADC(Pin(34))  # GPIO 34
electrode2 = ADC(Pin(35))  # GPIO 35
electrode3 = ADC(Pin(32))  # GPIO 32

# Ajuste de resolución
electrode1.width(ADC.WIDTH_12BIT)
electrode2.width(ADC.WIDTH_12BIT)
electrode3.width(ADC.WIDTH_12BIT)

def read_adc():
    """ Lee los valores de los electrodos y devuelve un diccionario """
    return {
        "electrode1": electrode1.read(),
        "electrode2": electrode2.read(),
        "electrode3": electrode3.read(),
    }
