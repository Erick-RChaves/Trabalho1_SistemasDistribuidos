with grpc.insecure_channel('localhost:50051') as channel:
    stub = ecommerce_pb2_grpc.OrderServiceStub(channel)
    order_request = ecommerce_pb2.CreateOrderRequest(user_id="user-123", product_id="product-abc", amount=99.99)
    response = stub.CreateOrder(order_request)
    print(response)
