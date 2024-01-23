# Importação das bibliotecas
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import requests

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Configuração do sensor DHT22
sensor = Adafruit_DHT.DHT22
pin = 22

# Chave de escrita do canal ThingSpeak
write_api_key = '65XMXASI8KNCLJ1Z'

# Função para enviar os dados para o ThingSpeak
def send_to_thingspeak(temperature, humidity):
    url = f'https://api.thingspeak.com/update.json'
    payload = {'api_key': write_api_key, 'field1': temperature, 'field2': humidity}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Dados enviados para o ThingSpeak com sucesso!')
    else:
        print('Erro ao enviar dados para o ThingSpeak:', response.text)

# Loop principal
while True:
    # Obtém a hora atual
    current_hour = time.localtime().tm_hour
    
    # Verifica se está no intervalo de tempo para ligar/desligar o relé na GPIO 23
    if current_hour >= 8 and current_hour < 18 :
        GPIO.output(23, GPIO.LOW)  # Liga o relé na GPIO 23
    else:
        GPIO.output(23, GPIO.HIGH)  # Desliga o relé na GPIO 23
    
    # Realiza a leitura do sensor DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Verifica se a leitura foi bem-sucedida
    if humidity is not None and temperature is not None:
        print(f'Temperatura: {temperature:.2f}°C, Umidade: {humidity:.2f}%')
        
        # Verifica a umidade para controlar o relé na GPIO 24
        if humidity < 90:
            GPIO.output(24, GPIO.LOW)  # Desliga o relé na GPIO 24
        else:
            GPIO.output(24, GPIO.HIGH)  # Liga o relé na GPIO 24
        
        # Envia os dados para o ThingSpeak
        send_to_thingspeak(temperature, humidity)
    
    else:
        print('Falha ao ler os dados do sensor DHT22.')
    
    time.sleep(60)  # Aguarda 60 segundos até a próxima leitura

# Função para commitar os dados em arquivo Json
def committData():
    print("Commiting data to Json...")
    
    