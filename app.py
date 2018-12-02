class App:  
    def serve(self, request):
        return {
            'app': 'server',
            'function': 'some',
            'result': 122,
        }