payment_request = ecommerce_pb2.PaymentRequest(order_id=order_id, amount=request.amount)
payment_response = self.payment_stub.ProcessPayment(payment_request)

if not payment_response.success:
    return ecommerce_pb2.CreateOrderResponse(order_id=order_id, status="FALHOU_PAGAMENTO")

event_message = {
    'order_id': order_id,
    'user_id': request.user_id,
    'product_id': request.product_id,
    'transaction_id': payment_response.transaction_id
}
self.rabbit_channel.basic_publish(exchange='order_events', routing_key='order.created', body=json.dumps(event_message))
