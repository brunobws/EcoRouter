#!/usr/bin/env python3
"""
Script de configuração automática do EcoRouter
Instala dependências e configura variáveis de ambiente
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def main():
    print_header("🌿 Setup do EcoRouter")
    
    # 1. Verificar Python
    print(f"✓ Python {sys.version.split()[0]} detectado")
    
    # 2. Criar venv se não existir
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Criando ambiente virtual...")
        os.system(f"{sys.executable} -m venv venv")
        print("✓ Ambiente virtual criado")
    else:
        print("✓ Ambiente virtual já existe")
    
    # 3. Instalar dependências
    print("\n📥 Instalando dependências...")
    pip_cmd = "venv\\Scripts\\pip.exe" if sys.platform == "win32" else "venv/bin/pip"
    os.system(f"{pip_cmd} install -r requirements.txt")
    print("✓ Dependências instaladas")
    
    # 4. Verificar .env
    print("\n⚙️  Verificando arquivo .env...")
    env_path = Path(".env")
    if not env_path.exists():
        print("📄 Criando arquivo .env...")
        env_path.write_text(
            "# Configurações do OpenRouteService\n"
            "# Obtenha sua chave gratuita em: https://openrouteservice.org/sign-up/\n"
            "# Limites gratuitos: 40.000 requisições por dia\n\n"
            "ORS_API_KEY=sua_chave_api_aqui\n"
        )
        print("✓ Arquivo .env criado")
        print("  ⚠️  IMPORTANTE: Edite .env e adicione sua chave OpenRouteService!")
    else:
        print("✓ Arquivo .env já existe")
    
    print_header("✅ Setup Concluído!")
    print("Próximos passos:")
    print("1. Edite o arquivo .env e adicione sua chave OpenRouteService")
    print("2. Execute: python app.py")
    print("3. Abra: http://127.0.0.1:5000\n")

if __name__ == "__main__":
    main()
