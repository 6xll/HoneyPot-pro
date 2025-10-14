#!/bin/bash
# Setup script for HoneyPot installation

set -e

echo "================================================"
echo "  HoneyPot - Instalação Automática"
echo "================================================"
echo

# Check Python version
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION encontrado"
echo

# Create virtual environment
echo "📦 Criando ambiente virtual..."
python3 -m venv venv
echo "✅ Ambiente virtual criado"
echo

# Activate virtual environment
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente virtual ativado"
echo

# Upgrade pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip -q
echo "✅ pip atualizado"
echo

# Install requirements
echo "📥 Instalando dependências..."
pip install -r requirements.txt -q
echo "✅ Dependências instaladas"
echo

# Create logs directory
echo "📁 Criando diretório de logs..."
mkdir -p logs
echo "✅ Diretório de logs criado"
echo

# Create analysis directory
echo "📁 Criando diretório de análise..."
mkdir -p analysis
echo "✅ Diretório de análise criado"
echo

# Make scripts executable
echo "🔑 Configurando permissões..."
chmod +x main.py test_services.py analysis/analyze.py
echo "✅ Permissões configuradas"
echo

echo "================================================"
echo "  ✅ Instalação concluída com sucesso!"
echo "================================================"
echo
echo "Para iniciar o honeypot:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo
echo "Para testar os serviços:"
echo "  python3 test_services.py"
echo
echo "Para analisar logs:"
echo "  python3 analysis/analyze.py"
echo
echo "Consulte README.md para mais informações."
echo
