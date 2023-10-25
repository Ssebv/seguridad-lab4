import socket
from sympy import primerange
from random import randint

# Función para generar una clave compartida
def generate_shared_key(p, g, secret):
    shared_key = (g ** secret) % p
    return shared_key

# Configuración del servidor
host = '127.0.0.1'
port = 12345

# Valores de Diffie-Hellman
p_values = list(primerange(100, 500))
p = p_values[randint(0, len(p_values) - 1)]
g = 2  # Puedes elegir otro valor, pero 2 suele ser común

# Inicializar el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Esperando una conexión en {host}:{port}...")

conn, addr = server_socket.accept()

# Enviar p y g al cliente
conn.send(str(p).encode())
conn.send(str(g).encode())

# Generar clave privada del servidor
server_private_key = randint(1, p - 1)

# Recibir la clave pública del cliente
client_public_key = int(conn.recv(1024).decode())

# Generar clave compartida
shared_key = generate_shared_key(p, g, server_private_key)

# Enviar la clave pública del servidor al cliente
conn.send(str((g ** server_private_key) % p).encode())

print(f"Clave compartida en el servidor: {shared_key}")

conn.close()
server_socket.close()
