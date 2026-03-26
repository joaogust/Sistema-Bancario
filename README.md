# 📌 IFSP - Instituição Financeira de São Paulo
### Projeto desenvolvido por **João Gustavo**, **Andrey Segantin** e **Elton Araújo** Curso: **Banco de Dados – IFSP**

---

## 📖 Sobre o Projeto

O **Sistema Bancário** é uma aplicação web desenvolvida para demonstrar conceitos práticos de bancos de dados, integração backend–frontend e deploy em nuvem.  
O sistema permite o gerenciamento de contas, clientes, transações e funcionalidades essenciais de uma solução bancária simples, focando em segurança e integridade dos dados.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3** e **Flask** (Backend)
- **HTML5**, **CSS3** e **Bootstrap** (Frontend)
- **PostgreSQL** (Banco de Dados Relacional)
- **Render.com** (Hospedagem do Servidor e DB)

---

## 🚀 Guia de Configuração e Execução

Siga os passos abaixo para configurar o ambiente e rodar o projeto localmente.

### 1. Clonar o Repositório
Abra o terminal e execute:
```bash
git clone [https://github.com/joaogust/Sistema-Bancario](https://github.com/joaogust/Sistema-Bancario)
cd Sistema-Bancario
```

### 2. Configurar o Ambiente Virtual (venv)
É crucial usar um ambiente virtual para isolar as bibliotecas do projeto e evitar conflitos.

| Ação | Comando (Windows) | Comando (Linux/MacOS) |
| :--- | :--- | :--- |
| **Criar** | `python -m venv venv` | `python3 -m venv venv` |
| **Ativar** | `.\\venv\\Scripts\\activate` | `source venv/bin/activate` |

### 3. Instalar Dependências
Com o ambiente virtual **ativado**, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 4. Configurar a IDE (Ex: PyCharm)
Se a sua IDE não reconhecer as bibliotecas, aponte o interpretador para o Python dentro da pasta `venv`:
1. Vá em **Settings > Project > Python Interpreter**.
2. Selecione **Add Interpreter** e escolha o caminho `venv/Scripts/python.exe` (Windows) ou `venv/bin/python` (Linux).

### 5. Configurar Variáveis de Ambiente (.env)
Crie um arquivo chamado `.env` na raiz do projeto. Você precisará configurar suas próprias chaves para o funcionamento pleno (Banco de Dados e API de E-mail):

```ini
SECRET_KEY="sua_chave_secreta"
POSTGRESQL_HOST="seu_host_render"
POSTGRESQL_USER="seu_usuario"
POSTGRESQL_PASSWORD="sua_senha"
POSTGRESQL_DATABASE="seu_banco_de_dados"
SENDGRID_API_KEY="sua_chave_sendgrid"
```
*⚠️ **Aviso:** Nunca envie seu arquivo `.env` para repositórios públicos.*

### 6. Executar o Projeto
```bash
flask run
```
Acesse no navegador: `http://127.0.0.1:5000`

---

## 🛑 Finalizar Ambiente
Para desativar o ambiente virtual após o uso, execute:
```bash
deactivate
```
```

Deseja que eu ajude a criar um arquivo `.env.example` para que outros usuários saibam exatamente quais chaves precisam preencher sem ver as suas originais?
