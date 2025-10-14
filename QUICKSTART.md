# Quick Start Guide

## Opção 1: Instalação Direta (Python)

```bash
# 1. Clone o repositório
git clone https://github.com/6xll/HoneyPot.git
cd HoneyPot

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute o honeypot
python3 main.py
```

## Opção 2: Docker

```bash
# 1. Clone o repositório
git clone https://github.com/6xll/HoneyPot.git
cd HoneyPot

# 2. Build e execute com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## Opção 3: Docker (manual)

```bash
# Build
docker build -t honeypot .

# Run
docker run -d \
  -p 2121:2121 \
  -p 2222:2222 \
  -p 8080:8080 \
  -v $(pwd)/logs:/app/logs \
  --name honeypot \
  honeypot

# Ver logs
docker logs -f honeypot
```

## Testando

```bash
# SSH
ssh -p 2222 admin@localhost

# HTTP
curl http://localhost:8080

# FTP
ftp localhost 2121
```

## Analisando Logs

```bash
# Script de análise
python3 analysis/analyze.py

# Ver ataques em tempo real
tail -f logs/attacks_*.json
```

## Parar o Honeypot

**Python direto:**
```bash
# Pressione Ctrl+C no terminal
```

**Docker:**
```bash
docker-compose down
# ou
docker stop honeypot
```

## Portas Utilizadas

- **2121**: FTP Honeypot
- **2222**: SSH Honeypot  
- **8080**: HTTP Honeypot

## Estrutura de Logs

- `logs/honeypot_YYYYMMDD.log` - Logs gerais
- `logs/attacks_YYYYMMDD.json` - Ataques em JSON

## Configuração

Edite `config.yaml` para personalizar:

```yaml
services:
  ssh:
    enabled: true
    port: 2222
  http:
    enabled: true
    port: 8080
  ftp:
    enabled: true
    port: 2121
```

## Documentação Completa

- [README.md](README.md) - Documentação principal
- [INSTALL_VM.md](INSTALL_VM.md) - Instalação em VM
- [ANALYSIS.md](ANALYSIS.md) - Análise de logs
- [EXAMPLES.md](EXAMPLES.md) - Exemplos de uso

## Suporte

Para problemas ou dúvidas, consulte a documentação completa ou abra uma issue no GitHub.
