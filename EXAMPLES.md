# Exemplos de Uso do HoneyPot

## Cenários de Teste

### 1. Teste Básico Local

#### Iniciar o Honeypot
```bash
python3 main.py
```

#### Em outro terminal, testar os serviços

**Teste SSH:**
```bash
# Tentativa de conexão SSH
ssh -p 2222 admin@localhost

# Tentativa com senha
sshpass -p "123456" ssh -p 2222 root@localhost

# Múltiplas tentativas (brute force simulado)
for user in admin root user test; do
  for pass in password 123456 admin root; do
    sshpass -p "$pass" ssh -p 2222 -o StrictHostKeyChecking=no $user@localhost
  done
done
```

**Teste HTTP:**
```bash
# Requisição simples
curl http://localhost:8080

# Simular scan de vulnerabilidades
curl http://localhost:8080/admin
curl http://localhost:8080/phpmyadmin
curl http://localhost:8080/wp-admin
curl http://localhost:8080/.git/config
curl http://localhost:8080/../../../etc/passwd

# Simular ataques comuns
curl -X POST http://localhost:8080/login -d "user=admin&pass=admin"
curl http://localhost:8080 -H "User-Agent: sqlmap/1.0"
```

**Teste FTP:**
```bash
# Conexão FTP interativa
ftp localhost 2121

# Comandos dentro do FTP
USER admin
PASS password123
QUIT

# Ou usando script
echo -e "USER admin\nPASS 123456\nQUIT" | ftp -n localhost 2121
```

### 2. Simulação de Ataque com Nmap

```bash
# Scan de portas
nmap -p 2121,2222,8080 localhost

# Scan de serviços
nmap -sV -p 2121,2222,8080 localhost

# Scripts NSE
nmap --script ssh-brute -p 2222 localhost
nmap --script ftp-anon -p 2121 localhost
nmap --script http-enum -p 8080 localhost
```

### 3. Teste com Metasploit

```bash
msfconsole

# SSH Brute Force
use auxiliary/scanner/ssh/ssh_login
set RHOSTS localhost
set RPORT 2222
set USERNAME admin
set PASS_FILE /usr/share/wordlists/metasploit/common_passwords.txt
run

# HTTP Scanner
use auxiliary/scanner/http/http_version
set RHOSTS localhost
set RPORT 8080
run

# FTP Anonymous Login
use auxiliary/scanner/ftp/anonymous
set RHOSTS localhost
set RPORT 2121
run
```

### 4. Teste com Hydra (Brute Force)

```bash
# SSH Brute Force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://localhost:2222

# FTP Brute Force
hydra -l admin -P passwords.txt ftp://localhost:2121

# HTTP Form Brute Force
hydra -l admin -P passwords.txt localhost -s 8080 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"
```

### 5. Análise dos Logs Capturados

#### Ver ataques em tempo real
```bash
tail -f logs/attacks_$(date +%Y%m%d).json
```

#### Análise com o script Python
```bash
python3 analysis/analyze.py

# Exportar para CSV
python3 analysis/analyze.py --export-csv
```

#### Usar jq para análise
```bash
# Ver último ataque
cat logs/attacks_*.json | tail -1 | jq '.'

# IPs únicos que atacaram
cat logs/attacks_*.json | jq -r '.source_ip' | sort -u

# Senhas mais tentadas
cat logs/attacks_*.json | jq -r 'select(.data.password) | .data.password' | sort | uniq -c | sort -rn
```

## Cenários Avançados

### 6. Exposição Controlada na Rede Local

```bash
# Configurar para aceitar conexões da rede
# Editar config.yaml: bind_address: "0.0.0.0"

# Encontrar IP da máquina
ip addr show

# Outros computadores na rede podem atacar
# De outra máquina:
nmap 192.168.1.100 -p 2121,2222,8080
ssh -p 2222 admin@192.168.1.100
```

### 7. Uso com Docker (Isolamento)

```bash
# Criar Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 2121 2222 8080
CMD ["python3", "main.py"]
EOF

# Build
docker build -t honeypot .

# Run
docker run -p 2121:2121 -p 2222:2222 -p 8080:8080 -v $(pwd)/logs:/app/logs honeypot
```

### 8. Monitoramento com Script Personalizado

```python
#!/usr/bin/env python3
# monitor.py - Monitoramento em tempo real

import json
import time
from pathlib import Path
from datetime import datetime

def monitor_attacks():
    log_file = Path(f"logs/attacks_{datetime.now().strftime('%Y%m%d')}.json")
    
    print("🔍 Monitorando ataques em tempo real...")
    print("Pressione Ctrl+C para sair\n")
    
    if log_file.exists():
        # Ir para o final do arquivo
        with open(log_file, 'r') as f:
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    try:
                        attack = json.loads(line)
                        print(f"⚠️  [{attack['timestamp']}] "
                              f"{attack['service']} de {attack['source_ip']} - "
                              f"{attack['data']}")
                    except:
                        pass
                else:
                    time.sleep(0.5)

if __name__ == '__main__':
    try:
        monitor_attacks()
    except KeyboardInterrupt:
        print("\n\nMonitoramento encerrado.")
```

### 9. Teste de Carga

```bash
# Script para gerar múltiplas conexões
for i in {1..100}; do
  (
    curl -s http://localhost:8080 > /dev/null
    echo "USER test$i" | nc localhost 2121
  ) &
done

wait
echo "Teste de carga concluído!"
```

### 10. Integração com SIEM (Exemplo com Syslog)

```python
#!/usr/bin/env python3
# forward_to_siem.py

import json
import syslog
from pathlib import Path
from datetime import datetime

def forward_logs():
    log_file = Path(f"logs/attacks_{datetime.now().strftime('%Y%m%d')}.json")
    
    syslog.openlog('honeypot', syslog.LOG_PID, syslog.LOG_LOCAL0)
    
    with open(log_file, 'r') as f:
        for line in f:
            try:
                attack = json.loads(line)
                message = f"Honeypot Attack: {json.dumps(attack)}"
                syslog.syslog(syslog.LOG_WARNING, message)
            except:
                pass
    
    syslog.closelog()

if __name__ == '__main__':
    forward_logs()
```

## Cenários de Demonstração para Projeto Final

### Demonstração 1: Captura de Credenciais

1. Inicie o honeypot
2. Execute tentativas de login SSH com credenciais comuns
3. Mostre os logs capturando usuário e senha
4. Analise padrões com o script de análise

### Demonstração 2: Detecção de Scanners

1. Execute nmap contra o honeypot
2. Mostre como o honeypot detecta o scanner
3. Analise os diferentes tipos de scans detectados

### Demonstração 3: Ataques Web

1. Use ferramentas como dirb/gobuster
2. Simule injeção SQL e XSS
3. Mostre como o honeypot registra todas as requisições

### Demonstração 4: Análise e Relatórios

1. Execute vários ataques diferentes
2. Use o script de análise para gerar estatísticas
3. Exporte dados para CSV
4. Crie gráficos com os dados capturados

## Dicas de Apresentação

1. **Preparação:**
   - Tenha logs pré-existentes para demonstração rápida
   - Prepare scripts para gerar ataques automaticamente
   - Configure terminal com múltiplas janelas (tmux)

2. **Demonstração:**
   - Janela 1: Honeypot rodando
   - Janela 2: Logs em tempo real
   - Janela 3: Executar ataques
   - Janela 4: Análise

3. **Pontos a Destacar:**
   - Segurança: Como honeypots ajudam a entender atacantes
   - Aprendizado: Técnicas e ferramentas usadas por atacantes
   - Análise: Como os dados podem ser usados para melhorar segurança
