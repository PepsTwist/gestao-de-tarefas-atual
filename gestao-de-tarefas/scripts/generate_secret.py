#!/usr/bin/env python3
"""
Script para gerar uma chave secreta segura para o sistema
"""
import secrets

def generate_secret_key():
    """Gera uma chave secreta segura"""
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 50)
    print("CHAVE SECRETA GERADA:")
    print("=" * 50)
    print(secret_key)
    print("=" * 50)
    print("\nCopie esta chave e use como SECRET_KEY nas variáveis de ambiente do Vercel")
    print("IMPORTANTE: Mantenha esta chave segura e não a compartilhe!")

