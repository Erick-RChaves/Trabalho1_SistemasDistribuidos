import grpc
from concurrent import futures

import pubsub_pb2
import pubsub_pb2_grpc

subscribers = {} #ver depois

class PubSubService(pubsub_pb2_grpc.PubSubServicer):
  def publish(self, request, context):
    topic = request.topic
    if topic in subscribers:
      for responder in subscribers[topic]:
        responder.add(request)
    return pubsub_pb2.ack(status=f"Mensagem publicada em {topic}")

def Subscribe(self, request, context):
  topic = request.topic
  class Responder:
    def __init__(self):
      self.queue = []
    def add(self, msg):
      self.queue.append(msg)

responder = responder()
subscribers.setdefault(topic, []).append(responder)

while True:
      if responder.queue:
        yield responder.queue.pop(0)

def server():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pubsub_pb2_grpc.add_PubSubServicer_to_server(pubSubService(), server)
  server.add_insecure_port()
  print("servidor gRPC rodando na porta")
  server.wait_for_termination()

if __name__ == "__main__":
  server()
      
      

