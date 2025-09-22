import pika
import json
import time
def main():
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

channel = connection.channel()
channel.exchange_declare(exchange='order_events', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='order_events', queue=queue_name,
routing_key='order.created')
print('Serviço de Notificações a aguardar por eventos de encomendas...')
def callback(ch, method, properties, body):
event = json.loads(body)
print(f" [x] Recebido evento 'order.created': {event}")
print(f" [->] SIMULANDO ENVIO DE EMAIL para o utilizador {event['user_id']} sobre a
encomenda {event['order_id']}")
ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
if __name__ == '__main__':
# Adiciona um retry para esperar o RabbitMQ iniciar
time.sleep(10) # Atraso para garantir que o RabbitMQ está pronto
main()
