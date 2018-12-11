import socket
import time
import numpy as np
from pprint import pprint
from apps.node import Node
from connection import Selector
from sessions import (
    FoundsSession, HistorySession
)
from apps.node import Node
from apps.client import Client

# selector = Selector()

# def reader(conenction, obj):
#     print(obj)

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('127.0.0.1', 8080))
# connection = selector.register(sock, sock.getsockname())
# connection.reader(reader)

# connection.send({
#     'app': 'node',
#     'function': 'found',
#     'args': [],
#     'kwargs': {
#         'camera': 'Camera 1',
#         'place': 'Place 1',
#         'face_encoding': []
#     },
# })

# while True:
#     try:
#         selector.step()
#         time.sleep(0.1)
#     except Exception:
#         pass
#     except KeyboardInterrupt:
#         sock.close()
#         exit()






# with Node(['found']) as actions:
#     actions.found('Place 1', 'Camera 1', [np.array([-0.07305394,  0.01363766,  0.00351507, -0.06707755, -0.06373984,
#        -0.02890858,  0.03333014, -0.11330593,  0.09077144, -0.11083597,
#         0.30164397, -0.09913448, -0.21657309, -0.14030647, -0.03646757,
#         0.14209104, -0.10887936, -0.08083898, -0.06420404, -0.00681543,
#         0.10115616, -0.05360883, -0.02963421,  0.03823626, -0.04176153,
#        -0.33879244, -0.10329235, -0.02388146,  0.07865575, -0.08338119,
#        -0.03097011,  0.01005391, -0.1874963 , -0.04999496, -0.01635474,
#         0.04617029, -0.02827929, -0.08970955,  0.17012249, -0.02286296,
#        -0.23031324, -0.00619672,  0.03180414,  0.21459495,  0.20173377,
#         0.03402312, -0.02477773, -0.10754794,  0.05981764, -0.22689851,
#         0.03760446,  0.11507041,  0.10973567,  0.04137872, -0.04416704,
#        -0.08333265, -0.00126475,  0.12070975, -0.20716685, -0.01222536,
#         0.08353411, -0.06696812, -0.03773543, -0.06850734,  0.19226153,
#         0.11157554, -0.16057031, -0.11609015,  0.14507924, -0.1913017 ,
#         0.00497996,  0.03646359, -0.10335634, -0.23466548, -0.24703391,
#         0.10023701,  0.40210178,  0.17857361, -0.18413416, -0.02118266,
#        -0.09695497,  0.04490121,  0.22003832,  0.0717875 ,  0.01956793,
#        -0.05660713, -0.08352853,  0.00855713,  0.1678097 , -0.07494379,
#        -0.041733  ,  0.23277023, -0.01689604,  0.05283426,  0.00732144,
#         0.07362172, -0.0167671 ,  0.08379041, -0.09298749,  0.05691862,
#         0.04936712, -0.06070145,  0.06505848,  0.10887763, -0.10931208,
#         0.13784645,  0.02305797,  0.03606503,  0.10627887, -0.03464404,
#        -0.08307163, -0.09572352,  0.08188966, -0.24537468,  0.1933884 ,
#         0.17416722,  0.04306418,  0.13261265,  0.12062126,  0.11252683,
#         0.05000631, -0.10146163, -0.19001594,  0.0043037 ,  0.06735821,
#        -0.01360147,  0.07202588, -0.03910035])])


# with FoundsSession() as manager:
#     pprint(manager.items())

# with HistorySession() as manager:
#     pprint(manager.items())


with Client([
    'last_view'
]) as manager:
    print(manager.last_view('Azamat', 'Bakhytzhan'))