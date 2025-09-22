import grpc
import protos.ecommerce_pb2 as ecommerce_pb2
import protos.ecommerce_pb2_grpc as ecommerce_pb2_grpc

def run():
    # O cliente conecta-se à porta exposta no docker-compose
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ecommerce_pb2_grpc.OrderServiceStub(channel)
        print("--- Criando uma nova encomenda ---")

        # Criar uma requisição de encomenda
        order_request = ecommerce_pb2.CreateOrderRequest(
            user_id="user-123",
            product_id="product-abc",
            amount=99.99
        )

        # Chamar o serviço de encomendas
        response = stub.CreateOrder(order_request)
        print(f"Resposta do Serviço de Encomendas:")
        print(f" ID da Encomenda: {response.order_id}")
        print(f" Status: {response.status}")


if __name__ == '__main__':
    run()
