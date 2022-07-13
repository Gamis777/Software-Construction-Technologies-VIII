from ast import dump
from urllib import request
from spyne import Application, ServiceBase, Unicode, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import requests
from requests_toolbelt.utils import dump
from datetime import datetime
from datetime import timedelta


class Convertor(ServiceBase):

    @rpc(str, str, str, str, _returns=str)
    def ejer_d(ctx, la:str, lo: str, fe: str,ho: str) -> str:
        url="https://api.sunrise-sunset.org/json?lat="+la+"&lng="+lo+"&date="+fe+"&formatted"+ho+""
        c=requests.get(url)
        d=dump.dump_all(c)
        return(d.decode('utf-8'))

application = Application(
    services=[Convertor],
    tns='http://tests.python-zeep.org/',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())

application = WsgiApplication(application)

if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, application)
    server.serve_forever()