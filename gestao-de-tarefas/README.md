# 📋 Sistema de Gestão de Tarefas

Um sistema completo de gestão de tarefas com interface web moderna, desenvolvido com React (frontend) e FastAPI (backend).

## ✨ Funcionalidades

### Para Usuários
- 🔐 Login seguro com autenticação JWT
- 📝 Criar, editar e gerenciar tarefas
- 👥 Atribuir responsáveis da mesma equipe
- 📊 Dashboard com estatísticas
- 🎯 Visualização Kanban
- 🏷️ Categorização e priorização de tarefas

### Para Administradores
- 👨‍💼 Painel administrativo completo
- 👤 Cadastro e gerenciamento de usuários
- 🏢 Criação e gestão de equipes
- 📈 Visão geral do sistema
- 🔧 Configurações avançadas

## 🚀 Deploy Rápido

### Opção 1: Vercel + MongoDB Atlas (Recomendado)
1. Faça fork deste repositório
2. Configure MongoDB Atlas (gratuito)
3. Deploy no Vercel com um clique
4. Configure variáveis de ambiente

[📖 Guia Completo de Deploy](./guia_deploy_completo.md)

### Opção 2: Docker
```bash
docker-compose up -d
```

## 🛠️ Desenvolvimento Local

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- MongoDB (local ou Atlas)

### Backend
```bash
cd backend
pip install -r requirements.txt
python server.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🔧 Configuração

### Variáveis de Ambiente
Copie `.env.example` para `.env` e configure:

```env
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/
DB_NAME=taskmanager
SECRET_KEY=sua_chave_secreta_super_forte
```

### Gerar Chave Secreta
```bash
python scripts/generate_secret.py
```

### Verificar Configuração
```bash
python scripts/check_config.py
```

## 📊 Estrutura do Projeto

```
gestao-de-tarefas/
├── backend/                 # API FastAPI
│   ├── server.py           # Servidor principal
│   ├── init_admin.py       # Script de inicialização
│   └── requirements.txt    # Dependências Python
├── frontend/               # Interface React
│   ├── src/
│   │   ├── App.js         # Componente principal
│   │   └── Components.js  # Componentes da UI
│   └── package.json       # Dependências Node.js
├── scripts/               # Scripts utilitários
├── vercel.json           # Configuração Vercel
└── README.md             # Este arquivo
```

## 🔐 Credenciais Padrão

Após executar `init_admin.py`:

**Administrador:**
- Email: admin@taskmanager.com
- Senha: admin123

**Usuário de Teste:**
- Email: joao@taskmanager.com
- Senha: user123

⚠️ **Altere essas credenciais em produção!**

## 🐛 Troubleshooting

### Erro de Conexão com Banco
1. Verifique se MongoDB está rodando
2. Confirme a string de conexão
3. Verifique permissões de rede (Atlas)

### Erro de Autenticação
1. Verifique se SECRET_KEY está configurada
2. Confirme se usuários foram criados
3. Execute `init_admin.py` se necessário

### Frontend não carrega
1. Verifique se backend está rodando
2. Confirme URL da API no frontend
3. Verifique console do navegador

## 📈 Monitoramento

### Logs
- **Vercel:** Painel → Functions → Logs
- **Local:** Console do terminal

### Métricas
- **MongoDB Atlas:** Painel → Metrics
- **Vercel:** Painel → Analytics

## 🤝 Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- 📖 [Guia de Deploy](./guia_deploy_completo.md)
- 🐛 [Issues](https://github.com/seu-usuario/gestao-de-tarefas/issues)
- 📧 Email: seu-email@exemplo.com

---

**Desenvolvido com ❤️ para facilitar sua gestão de tarefas!**

