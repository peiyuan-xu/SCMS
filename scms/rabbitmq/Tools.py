from pyrabbit.api import Client
cl = Client('localhost:55672', 'guest', 'guest')
cl.is_alive()