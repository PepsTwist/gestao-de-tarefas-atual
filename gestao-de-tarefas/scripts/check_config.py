#!/usr/bin/env python3
"""
Script para verificar se a configuração está correta antes do deploy
"""
import os
import sys
from urllib.parse import urlparse

def check_mongo_url(url):
    """Verifica se a URL do MongoDB está no formato correto"""
    if not url:
        return False, "MONGO_URL não definida"
    
    if not url.startswith('mongodb+srv://'):
        return False, "URL deve começar com 'mongodb+srv://'"
    
    if '<password>' in url:
        return False, "Substitua <password> pela senha real"
    
    parsed = urlparse(url)
    if not parsed.hostname:
        return False, "Hostname inválido na URL"
    
    return True, "URL do MongoDB válida"

def check_secret_key(key):
    """Verifica se a chave secreta é forte o suficiente"""
    if not key:
        return False, "SECRET_KEY não definida"
    
    if len(key) < 32:
        return False, "SECRET_KEY deve ter pelo menos 32 caracteres"
    
    return True, "SECRET_KEY válida"

def check_db_name(name):
    """Verifica se o nome do banco está definido"""
    if not name:
        return False, "DB_NAME não definida"
    
    if len(name) < 3:
        return False, "DB_NAME deve ter pelo menos 3 caracteres"
    
    return True, "DB_NAME válida"

def main():
    print("🔍 Verificando configuração do sistema...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    mongo_url = os.getenv('MONGO_URL')
    secret_key = os.getenv('SECRET_KEY')
    db_name = os.getenv('DB_NAME')
    
    checks = [
        ("MONGO_URL", check_mongo_url(mongo_url)),
        ("SECRET_KEY", check_secret_key(secret_key)),
        ("DB_NAME", check_db_name(db_name))
    ]
    
    all_passed = True
    
    for var_name, (passed, message) in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {var_name}: {message}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 Todas as verificações passaram! Sistema pronto para deploy.")
        return 0
    else:
        print("⚠️  Corrija os problemas acima antes de fazer o deploy.")
        print("\nPara configurar as variáveis de ambiente:")
        print("1. No Vercel: Settings → Environment Variables")
        print("2. Localmente: crie um arquivo .env na raiz do projeto")
        return 1

if __name__ == "__main__":
    sys.exit(main())

