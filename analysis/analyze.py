#!/usr/bin/env python3
"""
Análise estatística dos ataques capturados pelo honeypot.
"""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def load_attacks(log_dir='logs'):
    """Carrega todos os ataques dos arquivos JSON."""
    attacks = []
    log_path = Path(log_dir)
    
    if not log_path.exists():
        print(f"Diretório {log_dir} não encontrado!")
        return attacks
    
    for file in log_path.glob('attacks_*.json'):
        with open(file, 'r') as f:
            for line in f:
                try:
                    attacks.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    
    return attacks


def analyze_attacks(attacks):
    """Realiza análise estatística dos ataques."""
    if not attacks:
        print("Nenhum ataque encontrado!")
        return
    
    print("=" * 60)
    print("ANÁLISE ESTATÍSTICA DE ATAQUES DO HONEYPOT")
    print("=" * 60)
    print()
    
    # Total de ataques
    print(f"📊 Total de ataques registrados: {len(attacks)}")
    print()
    
    # Distribuição por serviço
    services = Counter(a['service'] for a in attacks)
    print("📈 Distribuição por serviço:")
    for service, count in services.most_common():
        percentage = (count / len(attacks)) * 100
        print(f"  {service:10s}: {count:6d} ({percentage:5.1f}%)")
    print()
    
    # Top 10 IPs atacantes
    ips = Counter(a['source_ip'] for a in attacks)
    print("🌐 Top 10 IPs atacantes:")
    for i, (ip, count) in enumerate(ips.most_common(10), 1):
        print(f"  {i:2d}. {ip:15s}: {count:6d} tentativas")
    print()
    
    # Credenciais mais tentadas (SSH/FTP)
    credentials = []
    for a in attacks:
        if 'data' in a and 'username' in a['data'] and 'password' in a['data']:
            credentials.append((a['data']['username'], a['data']['password']))
    
    if credentials:
        cred_counter = Counter(credentials)
        print("🔑 Top 10 credenciais tentadas:")
        for i, ((user, pwd), count) in enumerate(cred_counter.most_common(10), 1):
            print(f"  {i:2d}. {user:15s}:{pwd:15s} ({count} vezes)")
        print()
    
    # Usuários mais tentados
    usernames = [a['data'].get('username') for a in attacks 
                 if 'data' in a and 'username' in a['data']]
    if usernames:
        user_counter = Counter(usernames)
        print("👤 Top 10 usuários tentados:")
        for i, (user, count) in enumerate(user_counter.most_common(10), 1):
            print(f"  {i:2d}. {user:20s}: {count:6d} vezes")
        print()
    
    # Senhas mais tentadas
    passwords = [a['data'].get('password') for a in attacks 
                 if 'data' in a and 'password' in a['data']]
    if passwords:
        pwd_counter = Counter(passwords)
        print("🔒 Top 10 senhas tentadas:")
        for i, (pwd, count) in enumerate(pwd_counter.most_common(10), 1):
            print(f"  {i:2d}. {pwd:20s}: {count:6d} vezes")
        print()
    
    # Análise temporal
    try:
        hours = Counter(
            datetime.fromisoformat(a['timestamp']).hour
            for a in attacks
            if 'timestamp' in a
        )
        print("⏰ Distribuição por hora do dia:")
        max_count = max(hours.values()) if hours else 1
        for hour in range(24):
            count = hours.get(hour, 0)
            bar_length = int((count / max_count) * 40) if max_count > 0 else 0
            bar = '█' * bar_length
            print(f"  {hour:02d}:00 {bar:40s} {count:4d}")
        print()
    except Exception as e:
        print(f"Erro na análise temporal: {e}")
        print()
    
    # Análise de comandos HTTP
    http_attacks = [a for a in attacks if a['service'] == 'HTTP']
    if http_attacks:
        print("🌐 Requisições HTTP:")
        request_lines = [a['data'].get('request_line', '') for a in http_attacks 
                        if 'data' in a and 'request_line' in a['data']]
        methods = Counter(line.split()[0] if line.split() else 'UNKNOWN' 
                         for line in request_lines if line)
        for method, count in methods.most_common():
            print(f"  {method:10s}: {count:6d}")
        print()


def export_csv(attacks, output_file='analysis/attacks_export.csv'):
    """Exporta ataques para CSV."""
    import csv
    
    Path('analysis').mkdir(exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'service', 'source_ip', 'source_port', 
                        'username', 'password', 'type'])
        
        for a in attacks:
            data = a.get('data', {})
            writer.writerow([
                a.get('timestamp', ''),
                a.get('service', ''),
                a.get('source_ip', ''),
                a.get('source_port', ''),
                data.get('username', ''),
                data.get('password', ''),
                data.get('type', '')
            ])
    
    print(f"✅ Dados exportados para {output_file}")


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Análise de ataques do honeypot')
    parser.add_argument('--log-dir', default='logs', help='Diretório de logs')
    parser.add_argument('--export-csv', action='store_true', 
                       help='Exportar para CSV')
    parser.add_argument('--output', default='analysis/attacks_export.csv',
                       help='Arquivo de saída CSV')
    
    args = parser.parse_args()
    
    attacks = load_attacks(args.log_dir)
    
    if attacks:
        analyze_attacks(attacks)
        
        if args.export_csv:
            export_csv(attacks, args.output)
    else:
        print("Nenhum ataque encontrado. Execute o honeypot primeiro!")


if __name__ == '__main__':
    main()
