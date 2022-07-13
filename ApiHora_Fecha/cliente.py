from zeep import Client

client = Client('http://localhost:8000/?wsdl')
#result = client.service.ejer_a("pen")
#result = client.service.ejer_b("pen","jpy")
#result = client.service.ejer_c("2022-02-02","pen")
result = client.service.ejer_d("36.7201600","-4.4203400","2022-04-21","-5")

print(result)