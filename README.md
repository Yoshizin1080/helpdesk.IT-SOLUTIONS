🚀 Como executar o projeto
1. Pré-requisitos

Python 3.8+ instalado.

Não é necessário instalar bibliotecas externas, pois o projeto usa apenas módulos nativos (tkinter e ttk).

2. Executar o sistema

No terminal, dentro da pasta do projeto, rode:

python helpdesk.py

3. Funcionalidades

📊 Dashboard → visão geral dos chamados (Abertos, Em andamento e Fechados).

➕ Abrir Chamado → criar novo chamado com título, descrição e importância.

📋 Listar Chamados → visualizar todos os chamados e acessar detalhes.

✏️ Editar Chamado → alterar título, descrição, status e importância.

🗑️ Excluir Chamado → remover chamados por ID.

🚪 Sair → fechar o sistema.

4. Observações

Os dados são armazenados em memória. Ao fechar o sistema, os chamados são perdidos.

Para persistência, pode-se implementar gravação em arquivo JSON ou banco de dados (diferencial sugerido).
