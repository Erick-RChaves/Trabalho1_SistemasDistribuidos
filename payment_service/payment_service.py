import grpc
from concurrent import futures
import time
import protos.ecommerce_pb2 as ecommerce_pb2
import protos.ecommerce_pb2_grpc as ecommerce_pb2_grpc
import uuid
class PaymentService(ecommerce_pb2_grpc.PaymentServiceServicer):
def ProcessPayment(self, request, context):
print(f"Processando pagamento para a encomenda {request.order_id} no valor de
${request.amount:.2f}")
# Lógica de pagamento simulada
if request.amount > 0:
transaction_id = str(uuid.uuid4())
print(f"Pagamento APROVADO. ID da Transação: {transaction_id}")
return ecommerce_pb2.PaymentResponse(success=True,
transaction_id=transaction_id)
else:
print("Pagamento RECUSADO: valor inválido.")
return ecommerce_pb2.PaymentResponse(success=False)
def serve():
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ecommerce_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
server.add_insecure_port('[::]:50052')
server.start()
print("Serviço de Pagamentos a correr na porta 50052.")
server.wait_for_termination()
if __name__ == '__main__':
serve()
