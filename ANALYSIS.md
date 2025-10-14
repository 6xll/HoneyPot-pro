# Análise de Logs - Guia Completo

## Estrutura dos Logs

### Logs Gerais
Localização: `logs/honeypot_YYYYMMDD.log`

Formato:
```
2025-10-14 12:00:00,123 - HoneyPot - INFO - Connection to SSH from 192.168.1.100:45678
2025-10-14 12:00:05,456 - HoneyPot - WARNING - Attack on SSH from 192.168.1.100:45678
```

### Logs de Ataques
Localização: `logs/attacks_YYYYMMDD.json`

Formato JSON:
```json
{
  "timestamp": "2025-10-14T12:00:05.456789",
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

## Análise Básica com jq

### Instalação do jq

```bash
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq
```

### Comandos Úteis

#### Ver todos os ataques formatados
```bash
cat logs/attacks_*.json | jq '.'
```

#### Contar ataques por serviço
```bash
cat logs/attacks_*.json | jq -r '.service' | sort | uniq -c
```

#### Listar IPs únicos
```bash
cat logs/attacks_*.json | jq -r '.source_ip' | sort | uniq
```

#### Top 10 IPs mais ativos
```bash
cat logs/attacks_*.json | jq -r '.source_ip' | sort | uniq -c | sort -rn | head -10
```

#### Senhas mais tentadas (SSH/FTP)
```bash
cat logs/attacks_*.json | jq -r 'select(.data.password) | .data.password' | sort | uniq -c | sort -rn | head -20
```

#### Usuários mais tentados
```bash
cat logs/attacks_*.json | jq -r 'select(.data.username) | .data.username' | sort | uniq -c | sort -rn | head -20
```

#### Ataques de um IP específico
```bash
cat logs/attacks_*.json | jq 'select(.source_ip == "192.168.1.100")'
```

#### Ataques em HTTP
```bash
cat logs/attacks_*.json | jq 'select(.service == "HTTP")'
```

#### Ataques nas últimas 24 horas
```bash
cat logs/attacks_$(date +%Y%m%d).json | jq '.'
```

## Scripts de Análise

### Script 1: Resumo Diário

```bash
#!/bin/bash
# Salvar como: analysis/daily_summary.sh

LOG_FILE="logs/attacks_$(date +%Y%m%d).json"

echo "=== Resumo de Ataques - $(date +%Y-%m-%d) ==="
echo

echo "Total de ataques:"
cat $LOG_FILE | wc -l

echo
echo "Ataques por serviço:"
cat $LOG_FILE | jq -r '.service' | sort | uniq -c

echo
echo "Top 5 IPs atacantes:"
cat $LOG_FILE | jq -r '.source_ip' | sort | uniq -c | sort -rn | head -5

echo
echo "Top 10 senhas tentadas:"
cat $LOG_FILE | jq -r 'select(.data.password) | .data.password' | sort | uniq -c | sort -rn | head -10

echo
echo "Top 10 usuários tentados:"
cat $LOG_FILE | jq -r 'select(.data.username) | .data.username' | sort | uniq -c | sort -rn | head -10
```

### Script 2: Exportar para CSV

```bash
#!/bin/bash
# Salvar como: analysis/export_csv.sh

OUTPUT="analysis/attacks_$(date +%Y%m%d).csv"

echo "timestamp,service,source_ip,source_port,username,password" > $OUTPUT

cat logs/attacks_*.json | jq -r '
  [
    .timestamp,
    .service,
    .source_ip,
    (.source_port // ""),
    (.data.username // ""),
    (.data.password // "")
  ] | @csv' >> $OUTPUT

echo "Exportado para $OUTPUT"
```

### Script 3: Detector de Padrões

```bash
#!/bin/bash
# Salvar como: analysis/pattern_detector.sh

echo "=== Análise de Padrões de Ataque ==="
echo

# Detectar brute force
echo "Possíveis ataques de força bruta (>10 tentativas do mesmo IP):"
cat logs/attacks_*.json | jq -r '.source_ip' | sort | uniq -c | awk '$1 > 10 {print $2, ":", $1, "tentativas"}'

echo
echo "Combinações usuário/senha comuns:"
cat logs/attacks_*.json | jq -r 'select(.data.username and .data.password) | .data.username + ":" + .data.password' | sort | uniq -c | sort -rn | head -10

echo
echo "User-Agents em requisições HTTP:"
cat logs/attacks_*.json | jq -r 'select(.service == "HTTP") | .data.headers[]' | grep -i "user-agent" | sort | uniq -c
```

## Análise Avançada com Python

### Script: Análise Estatística

```python
#!/usr/bin/env python3
# Salvar como: analysis/stats.py

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

def load_attacks(log_dir='logs'):
    attacks = []
    for file in Path(log_dir).glob('attacks_*.json'):
        with open(file) as f:
            for line in f:
                try:
                    attacks.append(json.loads(line))
                except:
                    pass
    return attacks

def analyze(attacks):
    print("=== Análise Estatística de Ataques ===\n")
    
    # Total
    print(f"Total de ataques: {len(attacks)}")
    
    # Por serviço
    services = Counter(a['service'] for a in attacks)
    print(f"\nPor serviço:")
    for service, count in services.most_common():
        print(f"  {service}: {count}")
    
    # Por IP
    ips = Counter(a['source_ip'] for a in attacks)
    print(f"\nTop 10 IPs:")
    for ip, count in ips.most_common(10):
        print(f"  {ip}: {count}")
    
    # Credenciais
    credentials = Counter(
        (a['data'].get('username'), a['data'].get('password'))
        for a in attacks
        if 'data' in a and 'username' in a['data']
    )
    print(f"\nTop 10 credenciais:")
    for (user, pwd), count in credentials.most_common(10):
        print(f"  {user}:{pwd}: {count}")
    
    # Timeline
    hours = Counter(
        datetime.fromisoformat(a['timestamp']).hour
        for a in attacks
        if 'timestamp' in a
    )
    print(f"\nAtividade por hora:")
    for hour in sorted(hours.keys()):
        bar = '█' * (hours[hour] // 10)
        print(f"  {hour:02d}:00 {bar} ({hours[hour]})")

if __name__ == '__main__':
    attacks = load_attacks()
    analyze(attacks)
```

### Script: Geolocalização de IPs

```python
#!/usr/bin/env python3
# Salvar como: analysis/geolocate.py
# Requer: pip install geoip2

import json
import geoip2.database
from collections import Counter
from pathlib import Path

def geolocate_attacks(log_dir='logs', db_path='GeoLite2-City.mmdb'):
    # Download GeoLite2: https://dev.maxmind.com/geoip/geoip2/geolite2/
    
    attacks = []
    for file in Path(log_dir).glob('attacks_*.json'):
        with open(file) as f:
            for line in f:
                try:
                    attacks.append(json.loads(line))
                except:
                    pass
    
    reader = geoip2.database.Reader(db_path)
    countries = Counter()
    
    for attack in attacks:
        try:
            response = reader.city(attack['source_ip'])
            country = response.country.name
            countries[country] += 1
        except:
            countries['Unknown'] += 1
    
    print("=== Ataques por País ===\n")
    for country, count in countries.most_common():
        print(f"{country}: {count}")
    
    reader.close()

if __name__ == '__main__':
    geolocate_attacks()
```

## Integração com ELK Stack

### 1. Instalar Elasticsearch e Kibana

```bash
# Adicionar repositório
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

# Instalar
sudo apt update
sudo apt install elasticsearch kibana
```

### 2. Configurar Filebeat

```bash
sudo apt install filebeat

# Configurar filebeat.yml
sudo nano /etc/filebeat/filebeat.yml
```

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /home/honeypot/HoneyPot/logs/attacks_*.json
  json.keys_under_root: true
  json.add_error_key: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "honeypot-attacks-%{+yyyy.MM.dd}"

setup.kibana:
  host: "localhost:5601"
```

### 3. Criar Dashboard no Kibana

1. Acesse: http://localhost:5601
2. Crie índice: honeypot-attacks-*
3. Crie visualizações:
   - Mapa de calor: Ataques por hora
   - Gráfico de pizza: Distribuição por serviço
   - Tabela: Top IPs
   - Mapa geográfico: Origem dos ataques

## Alertas e Notificações

### Alerta por Email

```python
#!/usr/bin/env python3
# Salvar como: analysis/email_alert.py

import smtplib
import json
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime, timedelta

def check_attacks():
    threshold = 100  # Alertar se mais de 100 ataques/hora
    
    attacks = []
    log_file = Path(f"logs/attacks_{datetime.now().strftime('%Y%m%d')}.json")
    
    if log_file.exists():
        with open(log_file) as f:
            for line in f:
                try:
                    attack = json.loads(line)
                    timestamp = datetime.fromisoformat(attack['timestamp'])
                    if datetime.now() - timestamp < timedelta(hours=1):
                        attacks.append(attack)
                except:
                    pass
    
    if len(attacks) > threshold:
        send_alert(len(attacks), attacks)

def send_alert(count, attacks):
    msg = MIMEText(f"Alerta: {count} ataques na última hora!\n\nDetalhes: {attacks[:5]}")
    msg['Subject'] = f'HoneyPot Alert: {count} ataques'
    msg['From'] = 'honeypot@example.com'
    msg['To'] = 'admin@example.com'
    
    # Configurar SMTP
    # s = smtplib.SMTP('localhost')
    # s.send_message(msg)
    # s.quit()
    
    print(msg)

if __name__ == '__main__':
    check_attacks()
```

## Relatórios Periódicos

### Relatório Semanal

```bash
#!/bin/bash
# Salvar como: analysis/weekly_report.sh
# Agendar no cron: 0 9 * * 1 /path/to/weekly_report.sh

REPORT_FILE="reports/weekly_$(date +%Y%m%d).txt"
mkdir -p reports

{
  echo "=== Relatório Semanal - $(date +%Y-%m-%d) ==="
  echo
  
  echo "Total de ataques nos últimos 7 dias:"
  find logs -name "attacks_*.json" -mtime -7 -exec cat {} \; | wc -l
  
  echo
  echo "Distribuição por serviço:"
  find logs -name "attacks_*.json" -mtime -7 -exec cat {} \; | jq -r '.service' | sort | uniq -c
  
  echo
  echo "Top 20 IPs atacantes:"
  find logs -name "attacks_*.json" -mtime -7 -exec cat {} \; | jq -r '.source_ip' | sort | uniq -c | sort -rn | head -20
  
  echo
  echo "Top 20 senhas tentadas:"
  find logs -name "attacks_*.json" -mtime -7 -exec cat {} \; | jq -r 'select(.data.password) | .data.password' | sort | uniq -c | sort -rn | head -20
} > $REPORT_FILE

echo "Relatório salvo em $REPORT_FILE"
```

## Exportação para SIEM

### Syslog

```python
#!/usr/bin/env python3
# Integração com syslog para SIEM

import syslog
import json

def forward_to_siem(attack):
    syslog.openlog('honeypot', syslog.LOG_PID, syslog.LOG_LOCAL0)
    message = json.dumps(attack)
    syslog.syslog(syslog.LOG_WARNING, message)
    syslog.closelog()
```

### CEF Format (para ArcSight/Splunk)

```python
def to_cef(attack):
    cef = f"CEF:0|HoneyPot|HoneyPot|1.0|{attack['service']}|Attack|7|"
    cef += f"src={attack['source_ip']} "
    cef += f"spt={attack['source_port']} "
    cef += f"msg={json.dumps(attack['data'])}"
    return cef
```
