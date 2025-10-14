# HoneyPot - Network Honeypot System

Projeto Final de Cibersegurança - Sistema de Honeypot para Análise de Ataques

## 📋 Descrição

Este projeto implementa um sistema de honeypot de rede completo, projetado para capturar e analisar tentativas de ataque em serviços comuns. O honeypot simula serviços vulneráveis (SSH, HTTP, FTP) para atrair atacantes e registrar suas técnicas e ferramentas.

### Características Principais

- **Multi-Serviço**: Suporta múltiplos protocolos (SSH, HTTP, FTP)
- **Logging Detalhado**: Registra todas as tentativas de conexão e ataques
- **Configurável**: Sistema de configuração YAML flexível
- **Modular**: Arquitetura extensível para adicionar novos serviços
- **Análise de Ataques**: Logs estruturados em JSON para análise posterior

## 🏗️ Arquitetura

```
HoneyPot/
├── honeypot/
│   ├── __init__.py
│   ├── config.py          # Gerenciamento de configuração
│   ├── logger.py          # Sistema de logging
│   └── services/
│       ├── __init__.py
│       ├── ssh_service.py  # Honeypot SSH
│       ├── http_service.py # Honeypot HTTP
│       └── ftp_service.py  # Honeypot FTP
├── main.py                 # Ponto de entrada principal
├── config.yaml             # Configuração dos serviços
├── requirements.txt        # Dependências Python
└── logs/                   # Diretório de logs (criado automaticamente)
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Permissões para binding em portas (ou uso de portas > 1024)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/6xll/HoneyPot.git
cd HoneyPot
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Iniciar o Honeypot

```bash
python3 main.py
```

O honeypot iniciará todos os serviços configurados e começará a aceitar conexões.

### Configuração

Edite o arquivo `config.yaml` para personalizar os serviços:

```yaml
general:
  log_dir: "logs"
  bind_address: "0.0.0.0"

services:
  ssh:
    enabled: true
    port: 2222
    banner: "SSH-2.0-OpenSSH_7.4"
  
  http:
    enabled: true
    port: 8080
    server_name: "Apache/2.4.41 (Ubuntu)"
  
  ftp:
    enabled: true
    port: 2121
    banner: "220 FTP Server Ready"
```

### Testar o Honeypot

#### SSH
```bash
ssh -p 2222 usuario@localhost
```

#### HTTP
```bash
curl http://localhost:8080
```

#### FTP
```bash
ftp localhost 2121
```

## 📊 Análise de Logs

### Localização dos Logs

- **Logs Gerais**: `logs/honeypot_YYYYMMDD.log`
- **Logs de Ataques**: `logs/attacks_YYYYMMDD.json`

### Formato dos Logs de Ataque

```json
{
  "timestamp": "2025-10-14T12:00:00.000000",
  "service": "SSH",
  "source_ip": "192.168.1.100",
  "source_port": 45678,
  "data": {
    "type": "password_auth",
    "username": "admin",
    "password": "123456"
  }
}
```

### Analisando Ataques

```bash
# Ver todos os ataques de hoje
cat logs/attacks_$(date +%Y%m%d).json | jq '.'

# Contar ataques por serviço
cat logs/attacks_*.json | jq -r '.service' | sort | uniq -c

# Ver senhas mais comuns
cat logs/attacks_*.json | jq -r 'select(.data.password) | .data.password' | sort | uniq -c | sort -rn
```

## 🖥️ Implantação em VM

### Configuração Recomendada

- **Sistema Operacional**: Ubuntu 22.04 LTS ou Debian 12
- **RAM**: Mínimo 1GB
- **CPU**: 1 vCore
- **Disco**: 10GB
- **Rede**: Interface dedicada ou isolada

### Passos para Implantação

1. **Prepare a VM:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

2. **Clone e configure o honeypot:**
```bash
git clone https://github.com/6xll/HoneyPot.git
cd HoneyPot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure como serviço systemd (opcional):**

Crie `/etc/systemd/system/honeypot.service`:
```ini
[Unit]
Description=HoneyPot Network Service
After=network.target

[Service]
Type=simple
User=honeypot
WorkingDirectory=/home/honeypot/HoneyPot
ExecStart=/home/honeypot/HoneyPot/venv/bin/python3 /home/honeypot/HoneyPot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Inicie o serviço:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot
```

### Segurança

⚠️ **IMPORTANTE**: 

- Execute o honeypot em uma VM isolada
- Não exponha diretamente à Internet sem firewall
- Use portas altas (>1024) ou configure CAP_NET_BIND_SERVICE
- Monitore regularmente os logs
- Mantenha o sistema atualizado

## 🔒 Boas Práticas

1. **Isolamento**: Execute em rede isolada ou com regras de firewall estritas
2. **Monitoramento**: Configure alertas para atividades suspeitas
3. **Backup**: Faça backup regular dos logs
4. **Análise**: Revise logs periodicamente para identificar padrões
5. **Atualização**: Mantenha dependências atualizadas

## 📈 Recursos para Análise

### Ferramentas Recomendadas

- **jq**: Processamento de JSON
- **ELK Stack**: Elasticsearch, Logstash, Kibana para visualização
- **Splunk**: Plataforma de análise de dados
- **Wireshark**: Análise de tráfego de rede

### Métricas Importantes

- Tentativas de login por serviço
- IPs de origem mais ativos
- Credenciais mais utilizadas
- Padrões de ataque temporal
- Comandos executados

## 🤝 Contribuição

Este é um projeto acadêmico. Sugestões e melhorias são bem-vindas!

## 📝 Licença

Projeto educacional para fins de aprendizado em cibersegurança.

## ⚠️ Aviso Legal

Este software é fornecido apenas para fins educacionais e de pesquisa. O uso deste honeypot deve estar em conformidade com todas as leis e regulamentos aplicáveis. Os autores não se responsabilizam pelo uso indevido desta ferramenta.

## 👥 Autores

Projeto Final - Curso de Cibersegurança

## 📚 Referências

- [The Honeynet Project](https://www.honeynet.org/)
- [OWASP Honeypot Project](https://owasp.org/www-community/Honeypots)
- [Paramiko Documentation](http://www.paramiko.org/)

---

**Versão**: 1.0.0  
**Data**: Outubro 2025
