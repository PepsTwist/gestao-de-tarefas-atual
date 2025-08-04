# Guia Completo de Deploy - Sistema de Gestão de Tarefas

## 📋 Visão Geral

Este guia te ajudará a hospedar seu sistema de gestão de tarefas de forma independente usando **Vercel** (frontend + backend) e **MongoDB Atlas** (banco de dados).

**Tempo estimado:** 30-45 minutos
**Custo:** Gratuito para projetos pequenos
**Dificuldade:** ⭐⭐ (Fácil)

## 🎯 O que você vai conseguir

- Sistema online 24/7
- URL personalizada (ex: meu-sistema.vercel.app)
- SSL automático (HTTPS)
- Deploy automático via GitHub
- Banco de dados na nuvem

## 📋 Pré-requisitos

- [ ] Conta no GitHub
- [ ] Conta no MongoDB Atlas (gratuita)
- [ ] Conta no Vercel (gratuita)
- [ ] Git instalado no seu computador

## 🚀 Passo a Passo

### Etapa 1: Preparar o Código



#### 1.1 Baixar o Código Corrigido
1. Extraia o arquivo `gestao-de-tarefas-corrigido.zip` que te enviei
2. Abra o terminal/prompt na pasta extraída

#### 1.2 Inicializar Git (se ainda não foi feito)
```bash
git init
git add .
git commit -m "Projeto inicial de gestão de tarefas"
```

#### 1.3 Criar Repositório no GitHub
1. Acesse https://github.com
2. Clique em "New repository"
3. Nome: `gestao-de-tarefas` (ou outro nome de sua escolha)
4. Marque como "Public" ou "Private"
5. NÃO marque "Initialize with README"
6. Clique em "Create repository"

#### 1.4 Conectar ao GitHub
```bash
git remote add origin https://github.com/SEU_USUARIO/gestao-de-tarefas.git
git branch -M main
git push -u origin main
```

### Etapa 2: Configurar MongoDB Atlas

#### 2.1 Criar Conta e Cluster
1. Acesse https://www.mongodb.com/cloud/atlas
2. Clique em "Try Free" e crie sua conta
3. No painel, clique em "Build a Database"
4. Escolha "M0 Sandbox" (gratuito)
5. Selecione região "São Paulo" ou mais próxima
6. Nome do cluster: `taskmanager-cluster`
7. Clique em "Create"

#### 2.2 Configurar Usuário do Banco
1. Menu lateral → "Database Access"
2. "Add New Database User"
3. Username: `taskmanager_user`
4. Password: `[CRIE UMA SENHA FORTE]` (anote esta senha!)
5. Privileges: "Read and write to any database"
6. "Add User"

#### 2.3 Configurar Acesso de Rede
1. Menu lateral → "Network Access"
2. "Add IP Address"
3. "Allow Access from Anywhere" (0.0.0.0/0)
4. "Confirm"

#### 2.4 Obter String de Conexão
1. Menu lateral → "Database"
2. Clique em "Connect" no seu cluster
3. "Connect your application"
4. Selecione "Python" e "3.6 or later"
5. Copie a string (será algo como):
   ```
   mongodb+srv://taskmanager_user:<password>@taskmanager-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **IMPORTANTE:** Substitua `<password>` pela senha que você criou
7. **ANOTE ESTA STRING** - você vai precisar dela!



### Etapa 3: Deploy no Vercel

#### 3.1 Criar Conta no Vercel
1. Acesse https://vercel.com
2. Clique em "Sign Up"
3. Escolha "Continue with GitHub"
4. Autorize o Vercel a acessar seus repositórios

#### 3.2 Importar Projeto
1. No painel do Vercel, clique em "New Project"
2. Encontre seu repositório `gestao-de-tarefas`
3. Clique em "Import"

#### 3.3 Configurar Variáveis de Ambiente
**MUITO IMPORTANTE:** Antes de fazer o deploy, configure as variáveis:

1. Na tela de configuração do projeto, vá em "Environment Variables"
2. Adicione as seguintes variáveis:

| Nome | Valor |
|------|-------|
| `MONGO_URL` | Sua string de conexão do MongoDB Atlas |
| `DB_NAME` | `taskmanager` |
| `SECRET_KEY` | Uma chave secreta forte (veja como gerar abaixo) |

**Como gerar SECRET_KEY:**
```python
# Execute este código Python para gerar uma chave segura:
import secrets
print(secrets.token_urlsafe(32))
```

#### 3.4 Fazer Deploy
1. Após configurar as variáveis, clique em "Deploy"
2. Aguarde o processo (2-5 minutos)
3. Quando terminar, você receberá uma URL como: `https://seu-projeto.vercel.app`

### Etapa 4: Inicializar Dados do Sistema

#### 4.1 Acessar o Sistema
1. Abra a URL do seu projeto no navegador
2. Você verá a tela de login, mas ainda não há usuários

#### 4.2 Criar Usuário Administrador
Você tem duas opções:

**Opção A: Via Vercel CLI (Recomendado)**
1. Instale o Vercel CLI: `npm i -g vercel`
2. Faça login: `vercel login`
3. Execute: `vercel env pull .env.local`
4. Execute o script: `python backend/init_admin.py`

**Opção B: Via MongoDB Atlas Interface**
1. Acesse seu cluster no MongoDB Atlas
2. Clique em "Browse Collections"
3. Crie manualmente o usuário admin (mais complexo)

#### 4.3 Testar o Sistema
Após a inicialização, você pode fazer login com:
- **Admin:** admin@taskmanager.com / admin123
- **Usuário:** joao@taskmanager.com / user123


## 🎨 Personalização

### Domínio Personalizado
1. No painel do Vercel, vá em "Settings" → "Domains"
2. Adicione seu domínio personalizado
3. Configure DNS conforme instruções do Vercel

### Alterar Dados do Admin
1. Edite o arquivo `backend/init_admin.py`
2. Modifique email, senha e nome do administrador
3. Faça commit e push para GitHub
4. O Vercel fará redeploy automaticamente

## 🔧 Troubleshooting

### Problema: "Internal Server Error"
**Causa:** Variáveis de ambiente incorretas
**Solução:**
1. Verifique se todas as variáveis estão configuradas no Vercel
2. Confirme se a string do MongoDB está correta
3. Redeploy o projeto

### Problema: "Cannot connect to database"
**Causa:** Configuração do MongoDB Atlas
**Solução:**
1. Verifique se o IP 0.0.0.0/0 está liberado no Network Access
2. Confirme se o usuário do banco tem permissões corretas
3. Teste a string de conexão

### Problema: "Login não funciona"
**Causa:** Dados não inicializados
**Solução:**
1. Execute o script `init_admin.py`
2. Ou crie usuários manualmente no MongoDB Atlas

## 🔄 Atualizações Futuras

### Deploy Automático
Qualquer mudança que você fizer no código:
1. Faça commit: `git add . && git commit -m "Sua mensagem"`
2. Push para GitHub: `git push`
3. O Vercel detecta automaticamente e faz redeploy

### Backup do Banco
1. No MongoDB Atlas, vá em "Clusters"
2. Clique em "..." → "Create Snapshot"
3. Configure backups automáticos se necessário

## 📊 Monitoramento

### Logs do Vercel
1. No painel do Vercel, vá em "Functions"
2. Clique em qualquer função para ver logs
3. Use para debugar problemas

### Métricas do MongoDB
1. No MongoDB Atlas, vá em "Metrics"
2. Monitore uso de storage e conexões
3. Configure alertas se necessário

## 💰 Custos

### Plano Gratuito Inclui:
- **Vercel:** 100GB bandwidth/mês, 100 deployments/dia
- **MongoDB Atlas:** 512MB storage, 100 conexões simultâneas

### Quando Atualizar:
- **Vercel Pro ($20/mês):** Mais bandwidth e recursos
- **MongoDB M10 ($9/mês):** Mais storage e performance

## 🔒 Segurança

### Recomendações:
1. **Altere senhas padrão** imediatamente após deploy
2. **Use HTTPS sempre** (automático no Vercel)
3. **Monitore acessos** via logs
4. **Faça backups regulares** do banco
5. **Mantenha dependências atualizadas**

### Variáveis Sensíveis:
- Nunca commite arquivos `.env` para o GitHub
- Use apenas as variáveis de ambiente do Vercel
- Rotacione SECRET_KEY periodicamente

## 🎉 Parabéns!

Seu sistema de gestão de tarefas está agora online e funcionando! 

**URL do seu sistema:** https://seu-projeto.vercel.app

### Próximos Passos:
1. Teste todas as funcionalidades
2. Crie usuários e equipes reais
3. Personalize conforme necessário
4. Compartilhe com sua equipe

### Suporte:
- Documentação Vercel: https://vercel.com/docs
- Documentação MongoDB: https://docs.atlas.mongodb.com
- Para dúvidas específicas do sistema, consulte o código fonte

---

**Desenvolvido com ❤️ para facilitar sua gestão de tarefas!**

