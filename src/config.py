import os

general={}
general["API_GATEWAY_PROTOCOL"]=os.environ.get('API_GATEWAY_PROTOCOL')
general["API_GATEWAY_HOST"]=os.environ.get('API_GATEWAY_HOST')
general["API_GATEWAY_PORT"]=os.environ.get('API_GATEWAY_PORT')