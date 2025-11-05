import socket
import threading

class ChatServer:
    def __init__(self):
        self.clients = {}
        self.nicknames = {}
        self.lock = threading.Lock()
    
    def broadcast(self, sender_sock, message):
        """Envia mensagem para todos exceto o remetente - VERSÃO CORRIGIDA"""
        with self.lock:
            # Criar uma cópia da lista para evitar modificar durante iteração
            clients_to_send = list(self.clients.items())
        
        disconnected_clients = []
        
        for sock, nick in clients_to_send:
            if sock != sender_sock:
                try:
                    sock.send((message + "\n").encode("utf-8"))
                    print(f"[ENVIADO] Para {nick}: {message}")
                except Exception as e:
                    print(f"[ERRO ENVIO] Para {nick}: {e}")
                    disconnected_clients.append(sock)
        
        # Remove clientes desconectados fora do lock principal
        if disconnected_clients:
            with self.lock:
                for sock in disconnected_clients:
                    if sock in self.clients:
                        nick = self.clients[sock]
                        print(f"[REMOVENDO] Cliente {nick} por falha no envio")
                        del self.clients[sock]
                        if nick in self.nicknames:
                            del self.nicknames[nick]
    
    def send_dm(self, from_nick, to_nick, message):
        """Envia mensagem direta"""
        with self.lock:
            target_sock = self.nicknames.get(to_nick)
            if target_sock:
                try:
                    target_sock.send(f"FROM {from_nick} [dm]: {message}\n".encode("utf-8"))
                    return True
                except:
                    # Se falhar ao enviar DM, remove o cliente
                    self.remove_client(target_sock)
            return False
    
    def remove_client(self, sock):
        """Remove cliente da lista - VERSÃO CORRIGIDA"""
        nick_to_remove = None
        
        with self.lock:
            if sock in self.clients:
                nick_to_remove = self.clients[sock]
                del self.clients[sock]
                if nick_to_remove in self.nicknames:
                    del self.nicknames[nick_to_remove]
        
        if nick_to_remove:
            print(f"[SAIU] {nick_to_remove} desconectou")
            # Notifica outros clientes sobre a saída
            self.broadcast(sock, f"User {nick_to_remove} left")
        
        try:
            sock.close()
        except:
            pass
    
    def handle_client(self, sock, addr):
        print(f"[CONEXAO] {addr} conectado")
        nick = None
        
        try:
            # Fase 1: Registrar nick
            sock.send(b"Digite seu apelido: ")
            nick_data = sock.recv(1024).decode("utf-8").strip()
            
            if nick_data.startswith("NICK "):
                nick = nick_data[5:]
            else:
                nick = nick_data
            
            # Verificar se nick já existe
            with self.lock:
                if nick in self.nicknames:
                    sock.send(b"ERR apelido_em_uso\n")
                    sock.close()
                    return
                
                self.clients[sock] = nick
                self.nicknames[nick] = sock
            
            print(f"[REGISTRO] {nick} registrado")
            sock.send(f"✅ Registrado como '{nick}'. Agora você pode conversar!\n".encode("utf-8"))
            self.broadcast(sock, f"User {nick} joined")
            
            # Loop principal
            while True:
                data = sock.recv(1024).decode("utf-8").strip()
                if not data:
                    print(f"[DESCONEXAO] {nick} desconectou abruptamente")
                    break
                    
                print(f"[RECEBIDO] {nick}: {data}")
                
                if data.upper() == "QUIT":
                    sock.send(b"BYE\n")
                    print(f"[SAIU] {nick} saiu voluntariamente")
                    break
                    
                elif data.upper() == "WHO":
                    with self.lock:
                        users = ", ".join(self.nicknames.keys())
                    sock.send(f"👥 Usuários online: {users}\n".encode("utf-8"))
                    
                elif data.startswith("MSG "):
                    payload = data[4:].strip()
                    
                    if payload.startswith("@"):
                        # Mensagem direta
                        parts = payload.split(" ", 1)
                        target_nick = parts[0][1:]
                        message_text = parts[1] if len(parts) > 1 else ""
                        
                        if self.send_dm(nick, target_nick, message_text):
                            sock.send(f"✅ Mensagem enviada para {target_nick}\n".encode("utf-8"))
                        else:
                            sock.send(f"❌ Usuário '{target_nick}' não encontrado\n".encode("utf-8"))
                    else:
                        # Broadcast
                        self.broadcast(sock, f"FROM {nick} [all]: {payload}")
                        
                else:
                    # Mensagem normal (broadcast)
                    self.broadcast(sock, f"FROM {nick} [all]: {data}")
                    
        except Exception as e:
            print(f"[ERRO] {nick if nick else addr}: {e}")
        finally:
            if nick:
                self.remove_client(sock)
    
    def start(self, host='0.0.0.0', port=5000):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        
        print(f"🚀 Servidor rodando em {host}:{port}")
        print("👉 Aguardando conexões...")
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 Servidor parando...")
        except Exception as e:
            print(f"[ERRO SERVIDOR] {e}")
        finally:
            server_socket.close()
            print("Servidor fechado")

if __name__ == "__main__":
    server = ChatServer()
    server.start()