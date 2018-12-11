from apps.node import Node
from apps.admin import Admin
from apps.client import Client

class App:

    def serve(self, request):
        if request['app'] == 'node':
            with Node([
                'found',
            ]) as actions:
                return actions.serve(request)
        
        if request['app'] == 'admin':
            with Admin([
                'add',
            ]) as actions:
                return actions.serve(request)

        if request['app'] == 'client':
            with Client([
                'last_view',
            ]) as actions:
                return actions.serve(request)