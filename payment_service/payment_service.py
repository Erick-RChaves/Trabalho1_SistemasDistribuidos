class PaymentService(ecommerce_pb2_grpc.PaymentServiceServicer):
    def ProcessPayment(self, request, context):
        print(f"Processando pagamento da ordem {request.order_id} - valor: {request.amount}")
        if request.amount > 0:
            transaction_id = str(uuid.uuid4())
            return ecommerce_pb2.PaymentResponse(success=True, transaction_id=transaction_id)
        else:
            return ecommerce_pb2.PaymentResponse(success=False)
