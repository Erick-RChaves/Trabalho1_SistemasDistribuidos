import grpc
from concurrent import futures
import time
import pika
import json
import uuid
import ecommerce_pb2
import ecommerce_pb2_grpc

class OrderService(ecommerce_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        # Conexão gRPC com o serviço de pagamentos
        self.payment_channel = grpc.insecure_channel('payment_service:50052')
        self.payment_stub = ecommerce_pb2_grpc.PaymentServiceStub(self.payment_channel)

        # Conexão RabbitMQ
        credentials = pika.PlainCredentials('user', 'password')
        self.rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
        self.rabbit_channel = self.rabbit_connection.channel()
        self.rabbit_channel.exchange_declare(exchange='order_events', exchange_type='topic')
        print("Serviço de Encomendas conectado ao RabbitMQ.")

    def CreateOrder(self, request, context):
        print(f"Recebido pedido de encomenda para o utilizador {request.user_id} para o produto {request.product_id}")
        order_id = str(uuid.uuid4())

        # 1. Chamar o serviço de pagamentos (gRPC Síncrono)
        payment_request = ecommerce_pb2.PaymentRequest(order_id=order_id, amount=request.amount)
        payment_response = self.payment_stub.ProcessPayment(payment_request)

        if not payment_response.success:
            print(f"Encomenda {order_id} falhou: Pagamento recusado.")
            return ecommerce_pb2.CreateOrderResponse(order_id=order_id, status="FALHOU_PAGAMENTO")

        # 2. Publicar evento no RabbitMQ (Assíncrono)
        event_message = {
            'order_id': order_id,
            'user_id': request.user_id,
            'product_id': request.product_id,
            'transaction_id': payment_response.transaction_id
        }
        self.rabbit_channel.basic_publish(
            exchange='order_events',
            routing_key='order.created',
            body=json.dumps(event_message)
        )
        print(f"Evento 'order.created' publicado para a encomenda {order_id}")

        return ecommerce_pb2.CreateOrderResponse(order_id=order_id, status="APROVADA")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ecommerce_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Serviço de Encomendas a correr na porta 50051.")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

