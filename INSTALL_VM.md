# Guia de Instalação em VM

## Criação da Máquina Virtual

### VirtualBox

1. **Criar nova VM:**
   - Nome: HoneyPot
   - Tipo: Linux
   - Versão: Ubuntu (64-bit)
   - Memória: 1024 MB
   - Disco: 10 GB (dinâmico)

2. **Configuração de Rede:**
   - Adaptador 1: NAT ou Bridge (para acesso externo)
   - Adaptador 2: Host-only (para gerenciamento)

### VMware

1. **Criar nova VM:**
   - Custom Configuration
   - Linux / Ubuntu 64-bit
   - 1 GB RAM
   - 10 GB HD

2. **Configuração de Rede:**
   - Network Adapter: NAT ou Bridged
   - Adicionar segundo adaptador: Host-only

## Instalação do Sistema Operacional

### Ubuntu Server 22.04 LTS

1. **Download:**
   ```bash
   wget https://releases.ubuntu.com/22.04/ubuntu-22.04.3-live-server-amd64.iso
   ```

2. **Instalação Básica:**
   - Selecione idioma
   - Configure teclado
   - Configuração de rede (DHCP)
   - Usuário: honeypot
   - Instale OpenSSH Server

## Configuração Pós-Instalação

### 1. Atualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalar Dependências

```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    ufw \
    fail2ban \
    htop \
    net-tools
```

### 3. Configurar Firewall

```bash
# Permitir SSH de gerenciamento
sudo ufw allow 22/tcp

# Permitir portas do honeypot
sudo ufw allow 2222/tcp  # SSH honeypot
sudo ufw allow 8080/tcp  # HTTP honeypot
sudo ufw allow 2121/tcp  # FTP honeypot

# Ativar firewall
sudo ufw enable
```

### 4. Criar Usuário para Honeypot

```bash
# Criar usuário dedicado
sudo useradd -m -s /bin/bash honeypot
sudo passwd honeypot

# Mudar para o usuário
sudo su - honeypot
```

### 5. Instalar o Honeypot

```bash
# Clone o repositório
git clone https://github.com/6xll/HoneyPot.git
cd HoneyPot

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 6. Configurar como Serviço Systemd

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/honeypot.service
```

Adicionar conteúdo:

```ini
[Unit]
Description=HoneyPot Network Service
After=network.target

[Service]
Type=simple
User=honeypot
WorkingDirectory=/home/honeypot/HoneyPot
Environment="PATH=/home/honeypot/HoneyPot/venv/bin"
ExecStart=/home/honeypot/HoneyPot/venv/bin/python3 /home/honeypot/HoneyPot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot
sudo systemctl status honeypot
```

### 7. Configurar Rotação de Logs

```bash
sudo nano /etc/logrotate.d/honeypot
```

Adicionar:

```
/home/honeypot/HoneyPot/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 honeypot honeypot
}

/home/honeypot/HoneyPot/logs/*.json {
    daily
    rotate 60
    compress
    delaycompress
    notifempty
    create 0640 honeypot honeypot
}
```

## Monitoramento

### Ver Logs em Tempo Real

```bash
# Logs do serviço
sudo journalctl -u honeypot -f

# Logs do honeypot
tail -f /home/honeypot/HoneyPot/logs/honeypot_*.log

# Ataques capturados
tail -f /home/honeypot/HoneyPot/logs/attacks_*.json
```

### Comandos Úteis

```bash
# Status do serviço
sudo systemctl status honeypot

# Reiniciar serviço
sudo systemctl restart honeypot

# Parar serviço
sudo systemctl stop honeypot

# Ver portas em uso
sudo netstat -tulpn | grep python
```

## Segurança Adicional

### 1. Fail2Ban para SSH Real

```bash
sudo nano /etc/fail2ban/jail.local
```

```ini
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

### 2. Atualização Automática

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Hardening Básico

```bash
# Desabilitar IPv6 (se não usado)
echo "net.ipv6.conf.all.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf

# Proteção SYN flood
echo "net.ipv4.tcp_syncookies = 1" | sudo tee -a /etc/sysctl.conf

# Aplicar mudanças
sudo sysctl -p
```

## Backup

### Script de Backup Automático

```bash
nano /home/honeypot/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/honeypot/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /home/honeypot/HoneyPot/logs/

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "logs_*.tar.gz" -mtime +7 -delete
```

```bash
chmod +x /home/honeypot/backup.sh

# Adicionar ao cron (diário às 2 AM)
crontab -e
0 2 * * * /home/honeypot/backup.sh
```

## Troubleshooting

### Problema: Porta em uso

```bash
# Verificar processo usando porta
sudo lsof -i :2222

# Matar processo
sudo kill -9 <PID>
```

### Problema: Permissões

```bash
# Corrigir permissões
sudo chown -R honeypot:honeypot /home/honeypot/HoneyPot
chmod +x /home/honeypot/HoneyPot/main.py
```

### Problema: Dependências Python

```bash
# Recriar ambiente virtual
cd /home/honeypot/HoneyPot
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Próximos Passos

1. Configurar análise de logs com ELK Stack
2. Implementar alertas por email/Slack
3. Adicionar mais serviços honeypot
4. Integrar com SIEM
5. Criar dashboard de visualização
