def callback(ch, method, properties, body):
    event = json.loads(body)
    print(f"[x] Evento recebido: {event}")
    print(f"[->] Enviando e-mail para {event['user_id']} sobre pedido {event['order_id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
