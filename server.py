import socket
from sympy import primerange
from random import randint

# Función para generar una clave compartida
def generate_shared_key(p, g, secret):
    shared_key = (g ** secret) % p # p es el módulo, g es la base, secret es la clave privada
    return shared_key # Devuelve la clave compartida

# Configuración del servidor
host = '127.0.0.1'
port = 12345 

# Valores de Diffie-Hellman
p_values = list(primerange(100, 500)) # Genera una lista de números primos entre 100 y 500
p = p_values[randint(0, len(p_values) - 1)] # Elige un número primo aleatorio de la lista
g = 2  # Puedes elegir otro valor, pero 2 suele ser común en la práctica

# Inicializar el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Esperando una conexión en {host}:{port}...")

conn, addr = server_socket.accept() # Aceptar la conexión entrante
 
# Enviar p y g al cliente
conn.send(str(p).encode()) # Envía el número primo al cliente
conn.send(str(g).encode()) # Envía la base al cliente

# Generar clave privada del servidor
server_private_key = randint(1, p - 1) # Genera un número aleatorio entre 1 y p - 1

client_public_key = int(conn.recv(1024).decode()) # Recibe la clave pública del cliente

shared_key = generate_shared_key(p, g, server_private_key) # Genera la clave compartida

conn.send(str((g ** server_private_key) % p).encode()) # Envía la clave pública del servidor al cliente

# Intercambio de claves compartidas
client_key = int(conn.recv(1024).decode())
conn.send(str(shared_key).encode())

print(f"Clave compartida en el servidor: {shared_key}")


conn.close()
server_socket.close()
