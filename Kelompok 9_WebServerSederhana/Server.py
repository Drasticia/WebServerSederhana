import socket
import os

def handle_request(request):
    # Memisahkan baris permintaan untuk mendapatkan metode dan path
    lines = request.split("\r\n")
    method, path, _ = lines[0].split(" ")

    # Memeriksa apakah HTTP adalah GET
    if method == "GET":
        # Menghapus karakter '/' pada awal path
        path = path[1:]

        # Memeriksa keberadaan file HTML
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'r') as file:
                content = file.read()
                response = "HTTP/1.1 200 OK\r\n\r\n" + content
        else:
            # Mengirim respons 404 dengan file 404.html
            if os.path.exists('404.html') and os.path.isfile('404.html'):
                with open('404.html', 'r') as file:
                    content = file.read()
                    response = "HTTP/1.1 404 Not Found\r\n\r\n" + content

    # Menangani permintaan selain GET
    else:
        # Mengirim respons 501 jika metode tidak didukung
        response = "HTTP/1.1 501 Not Implemented\r\n\r\n501 Not Implemented"

    return response

def start_server():
    # Membuat objek socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 4444)

    # Mengikat socket ke alamat dan port yang ditentukan
    server_socket.bind(server_address)

    # Mendengarkan koneksi masuk
    server_socket.listen(1)
    print("Server berjalan di http://localhost:8080/")

    while True:
        # Menerima koneksi dari klien
        client_socket, client_address = server_socket.accept()
        print("Menerima koneksi dari:", client_address)

        # Membaca data dari koneksi klien
        request = client_socket.recv(1024).decode('utf-8')

        # Menangani permintaan dan mendapatkan respons
        response = handle_request(request)

        # Mengirimkan respons kembali ke klien
        client_socket.sendall(response.encode('utf-8'))

        # Menutup koneksi
        client_socket.close()

if __name__ == "__main__":
    start_server()