import socket

# Función para generar una clave compartida
def generate_shared_key(p, g, secret):
    shared_key = (g ** secret) % p
    return shared_key

# Configuración del cliente
host = '127.0.0.1'
port = 12345

# Inicializar el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Recibir p y g del servidor
p = int(client_socket.recv(1024).decode())
g = int(client_socket.recv(1024).decode())

# Generar clave privada del cliente
client_private_key = 3  # Puedes cambiar este valor si lo deseas

# Generar clave pública del cliente y enviarla al servidor
client_public_key = (g ** client_private_key) % p
client_socket.send(str(client_public_key).encode())

# Recibir la clave pública del servidor
server_public_key = int(client_socket.recv(1024).decode())

# Generar clave compartida
shared_key = (server_public_key ** client_private_key) % p

print(f"Clave compartida en el cliente: {shared_key}")

client_socket.close()
