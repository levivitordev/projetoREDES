# 🗨️ Mini-Chat TCP — PROJETO DE REDES 

## 📋 Pré-requisitos ( Tecnologias Necessarias )
- **Python 3.6** ou superior instalado  
- **Sistema operacional:** Windows, Linux ou macOS

---

## 🚀 Como Executar o mini-chat ⬇️

### 1️⃣ Clone o repositório ou baixe os arquivos:
- `server_melhorado.py`  
- `client_melhorado.py`

### ▶️ Executar o Servidor
**Terminal 1 - Servidor:**
```bash
python server_melhorado.py
```
✅ **Saída esperada:**
```
🚀 Servidor rodando em 0.0.0.0:5000
👉 Aguardando conexões...
```

---

### 🔌 Conectar os Clientes
**Terminal 2 - Cliente 1:**
```bash
python client_melhorado.py
```

**Terminal 3 - Cliente 2:**
```bash
python client_melhorado.py
```

**Terminal 4 - Cliente 3 (opcional):**
```bash
python client_melhorado.py
```

---

## 👤 Registrar Usuários
Em cada cliente, quando aparecer:

```
✅ Conectado ao servidor!
==================================================
Digite seu apelido:
```

Digite um apelido **único** para cada cliente:

| Cliente | Apelido |
|----------|----------|
| Cliente 1 | ana |
| Cliente 2 | joao |
| Cliente 3 | maria |

---

## 💡 Como Usar o Chat

### 📢 Mensagens Normais (Broadcast)
```
Olá pessoal!
```
💬 **VOCÊ [para todos]:** Olá pessoal!  
Todos os usuários conectados recebem a mensagem.

---

### 📩 Mensagem Direta (DM)
```
/dm joao Ei, mensagem secreta!
```
📩 **VOCÊ [para joao]:** Ei, mensagem secreta!  
Apenas o usuário mencionado recebe a mensagem.

---

### 👥 Listar Usuários Online
```
/who
```
👥 **Usuários online:** ana, joao, maria

---

### 🚪 Sair do Chat
```
/quit
```
👋 **Saindo do chat...**  
🔌 **Desconectado**

---

## 🧪 Casos de Teste Recomendados

✅ **Teste 1 — Mensagem Broadcast**  
Cliente 1 digita: `Olá everyone!`  
Verifique: Clientes 2 e 3 recebem a mensagem.

✅ **Teste 2 — Mensagem Direta**  
Cliente 2 digita: `/dm ana Mensagem secreta!`  
Verifique: Apenas Cliente 1 recebe a mensagem.

✅ **Teste 3 — Listar Usuários**  
Cliente 3 digita: `/who`  
Verifique: Lista todos os usuários conectados.

✅ **Teste 4 — Apelido Duplicado**  
Tente conectar um Cliente 4 com apelido `ana`.  
Verifique: Recebe erro **"Apelido já em uso"**.

✅ **Teste 5 — Sair e Reconectar**  
Cliente 1 digita: `/quit`  
Verifique: Clientes 2 e 3 recebem notificação de saída.  
Reconecte Cliente 1 com mesmo apelido.  
Verifique: Consegue se reconectar normalmente.

---

## ⚠️ Solução de Problemas

❌ **"Porta já em uso"**  
➡️ Espere alguns segundos ou mude a porta no servidor.

❌ **"Conexão recusada"**  
➡️ Verifique se o servidor está rodando.

❌ **"Apelido já em uso"**  
➡️ Escolha outro apelido.

❌ **Mensagens não aparecem"**  
➡️ Verifique se todos os clientes estão registrados com apelidos.

---

## 🎯 Estrutura do Projeto
```
mini-chat/
├── server_melhorado.py   # Servidor do chat
├── client_melhorado.py   # Cliente do chat
└── README.md              # Este guia
```

---

## 📞 Comandos Disponíveis

| Comando | Descrição | Exemplo |
|----------|------------|----------|
| Mensagem normal | Envia a todos | `Olá mundo!` |
| `/dm` | Mensagem privada | `/dm ana Oi!` |
| `/who` | Lista usuários online | `/who` |
| `/quit` | Sai do chat | `/quit` |

---

# 🤝 RESPONSAVEIS PELO PROJETO

- Luan Bandeira
- Levi Vitor
- Alexis Prado
