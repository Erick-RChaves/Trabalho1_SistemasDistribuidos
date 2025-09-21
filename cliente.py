import grpc 
import pubsub_pb2
import pubsub_pb2_grpc
import threading

def subscriber(stub,topic)
request = pubsub_pb2.SubscribeRequest(topic = topic)
for msg in stub.Subscribe(request):
  print(f"[{topic}] Nova mensagem: {msg.content}")

def publisher(stub, topic, content):
  msg = pubsub_pb2.Message(topic=topic, content= content)
  response = stub.publish(msg)
  print(response.status)

def main():
  channel = grpc.insecure_channel() #por depois o endereço do cluster
  stub = pubsub_pb2_grpc.PubSubStub(channel)

threading.Thread(target=subscriber, args=(stub, "noticias"), daemon=True).start()
publisher(stub, "noticias", texto)

if__name__ == "__main__":
main()
