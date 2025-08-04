# Configuração do MongoDB Atlas

## Passo 1: Criar Conta no MongoDB Atlas

1. Acesse: https://www.mongodb.com/cloud/atlas
2. Clique em "Try Free"
3. Crie sua conta (gratuita)
4. Faça login no painel

## Passo 2: Criar Cluster

1. No painel, clique em "Build a Database"
2. Escolha "M0 Sandbox" (gratuito)
3. Selecione uma região próxima (ex: São Paulo)
4. Nomeie seu cluster (ex: "taskmanager-cluster")
5. Clique em "Create"

## Passo 3: Configurar Acesso

### 3.1 Criar Usuário do Banco
1. Vá em "Database Access" no menu lateral
2. Clique em "Add New Database User"
3. Escolha "Password" como método de autenticação
4. Defina:
   - Username: `taskmanager_user`
   - Password: `[GERE UMA SENHA FORTE]`
5. Em "Database User Privileges", selecione "Read and write to any database"
6. Clique em "Add User"

### 3.2 Configurar IP Whitelist
1. Vá em "Network Access" no menu lateral
2. Clique em "Add IP Address"
3. Clique em "Allow Access from Anywhere" (0.0.0.0/0)
4. Clique em "Confirm"

## Passo 4: Obter String de Conexão

1. Vá em "Database" no menu lateral
2. Clique em "Connect" no seu cluster
3. Escolha "Connect your application"
4. Selecione "Python" e versão "3.6 or later"
5. Copie a string de conexão (será algo como):
   ```
   mongodb+srv://taskmanager_user:<password>@taskmanager-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Substitua `<password>` pela senha que você criou

## Passo 5: Criar Banco de Dados

1. No painel do cluster, clique em "Browse Collections"
2. Clique em "Add My Own Data"
3. Defina:
   - Database name: `taskmanager`
   - Collection name: `users`
4. Clique em "Create"

## Variáveis de Ambiente Necessárias

Para o deploy, você precisará das seguintes variáveis:

```
MONGO_URL=mongodb+srv://taskmanager_user:SUA_SENHA@taskmanager-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=taskmanager
SECRET_KEY=sua_chave_secreta_super_forte_aqui_com_pelo_menos_32_caracteres
```

### Como Gerar SECRET_KEY

Execute este comando Python para gerar uma chave segura:

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Inicialização dos Dados

Após o deploy, você precisará executar o script de inicialização para criar o usuário admin e dados de exemplo:

```bash
python backend/init_admin.py
```

Este script criará:
- Usuário admin: admin@taskmanager.com / admin123
- Usuários de exemplo
- Equipes de exemplo
- Tarefas de exemplo

## Segurança

⚠️ **IMPORTANTE:**
- Nunca compartilhe suas credenciais do banco
- Use senhas fortes
- Mantenha as variáveis de ambiente seguras
- Em produção, considere restringir IPs específicos no Network Access

