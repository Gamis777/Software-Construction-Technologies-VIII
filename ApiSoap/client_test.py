from zeep import Client

client = Client('http://localhost:8000/?wsdl')
result = client.service.multiplicacion(4,5)

print(result)