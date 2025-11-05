import socket
import threading
import sys
import time

# Variável global para controlar a conexão
conexao_ativa = True

def receive_messages(sock):
    """Thread para receber mensagens do servidor"""
    global conexao_ativa
    while conexao_ativa:
        try:
            # Configurar timeout para verificar periodicamente se ainda está ativo
            sock.settimeout(1.0)
            data = sock.recv(1024).decode("utf-8")
            if not data:
                print("\n🔌 Conexão com servidor fechada")
                conexao_ativa = False
                break
            
            # Limpa a linha e mostra a mensagem recebida
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            print(data.strip())
            if conexao_ativa:
                sys.stdout.write("> ")
                sys.stdout.flush()
                
        except socket.timeout:
            continue  # Timeout normal, continua verificando
        except:
            if conexao_ativa:  # Só mostra erro se a conexão deveria estar ativa
                print("\n🔌 Erro na conexão")
            conexao_ativa = False
            break

def main():
    global conexao_ativa
    conexao_ativa = True
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5000))
        print("✅ Conectado ao servidor!")
        
        # Primeiro: registrar o apelido
        print("\n" + "="*50)
        apelido = input("Digite seu apelido: ").strip()
        
        # Envia o apelido para o servidor
        sock.send(apelido.encode("utf-8"))
        
        # Aguarda a confirmação do servidor
        confirmacao = sock.recv(1024).decode("utf-8")
        print(confirmacao.strip())
        
        # Comandos disponiveis para utilizar o chat
        print("\n💡 COMANDOS DISPONÍVEIS:")
        print("  • Digite mensagens normais para enviar a todos")
        print("  • /dm <usuário> <mensagem>  - Enviar uma mensagem privada")
        print("  • /who                      - Listar usuários online")
        print("  • /quit                     - Sair do chat")
        print("="*50)
        print()
        
        # Inicia a thread de recebimento APÓS o registro
        receiver = threading.Thread(target=receive_messages, args=(sock,))
        receiver.daemon = True
        receiver.start()
        
        # Loop principal de mensagens
        while conexao_ativa:
            try:
                message = input("> ").strip()
                
                if not message:
                    continue
                
                # Comandos especiais
                if message.lower() == "/quit":
                    sock.send(b"QUIT")
                    print("👋 Saindo do chat...")
                    conexao_ativa = False
                    break
                    
                elif message.lower() == "/who":
                    sock.send(b"WHO")
                    
                elif message.lower().startswith("/dm "):
                    parts = message.split(" ", 2)
                    if len(parts) >= 3:
                        dm_command = f"MSG @{parts[1]} {parts[2]}"
                        sock.send(dm_command.encode("utf-8"))
                        # Mostra localmente também
                        sys.stdout.write('\r' + ' ' * 80 + '\r')
                        print(f"📩 VOCÊ [para {parts[1]}]: {parts[2]}")
                    else:
                        print("❌ Uso: /dm <usuário> <mensagem>")
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                        
                else:
                    # Mensagem normal
                    sock.send(message.encode("utf-8"))
                    # Mostra localmente
                    sys.stdout.write('\r' + ' ' * 80 + '\r')
                    print(f"💬 VOCÊ [para todos]: {message}")
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                    
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Saindo...")
                if conexao_ativa:
                    sock.send(b"QUIT")
                conexao_ativa = False
                break
                
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conexao_ativa = False
        time.sleep(0.1)  # Pequeno delay para garantir que a thread pare
        sock.close()
        print("🔌 Desconectado")

if __name__ == "__main__":

    main()

