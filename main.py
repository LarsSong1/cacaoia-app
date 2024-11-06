import serial
import time

def get_sensor_data(ser):
    if ser.in_waiting > 0:
        serial_data = ser.readline().decode('utf-8').rstrip()
        try:
            return int(serial_data)
        except ValueError:
            print("Error: No se pudo convertir a entero")
            return None
    return None



try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2) 

    while True:
        humidity = get_sensor_data(ser)
        if humidity is not None:
            print(f'Humedad: {humidity}')
        time.sleep(1)  # Leer cada segundo

except serial.SerialException as e:
    print(f'Error de conexión serial: {e}')

except KeyboardInterrupt:
    print('Lectura interrumpida por el usuario.')

finally:
    if ser.is_open:
        ser.close()
        print('Conexión serial cerrada.')
