class Base:

    FUNCTIONS = []

    class Actions:

        class DoesNotExist(Exception):
            pass

        def __init__(self, functions):
            self.functions = {function: getattr(self, function) for function in functions}

        def serve(self, request):
            if request['function'] not in self.functions:
                raise self.DoesNotExist('Function with given name does not exists.')
            return {
                'app': request['app'],
                'function': request['function'],
                'result': self.functions[request['function']](*request['args'], **request['kwargs'])
            }

    def __init__(self, functions=[]):
        self.functions = functions

    def __enter__(self):
        return self.Actions(
            [function for function in self.functions if function in self.FUNCTIONS]
        )

    def __exit__(self, exception_type, exception_value, traceback):
        pass