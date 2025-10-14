#!/usr/bin/env python3
"""
Script de teste para verificar os serviços do honeypot.
"""

import socket
import time
import sys


def test_http(host='localhost', port=8080):
    """Testa o serviço HTTP."""
    print(f"🔍 Testando HTTP em {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        request = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        sock.send(request)
        
        response = sock.recv(4096).decode('utf-8', errors='ignore')
        sock.close()
        
        if 'HTTP' in response:
            print("✅ HTTP: OK")
            return True
        else:
            print("❌ HTTP: Resposta inválida")
            return False
    except Exception as e:
        print(f"❌ HTTP: Falhou - {e}")
        return False


def test_ftp(host='localhost', port=2121):
    """Testa o serviço FTP."""
    print(f"🔍 Testando FTP em {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        
        if '220' in banner:
            # Tentar login
            sock.send(b"USER test\r\n")
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            
            sock.send(b"PASS test123\r\n")
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            
            sock.send(b"QUIT\r\n")
            sock.close()
            
            print("✅ FTP: OK")
            return True
        else:
            print("❌ FTP: Banner inválido")
            return False
    except Exception as e:
        print(f"❌ FTP: Falhou - {e}")
        return False


def test_ssh(host='localhost', port=2222):
    """Testa o serviço SSH."""
    print(f"🔍 Testando SSH em {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        # Receber banner SSH
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        
        if 'SSH' in banner:
            print("✅ SSH: OK")
            sock.close()
            return True
        else:
            print("❌ SSH: Banner inválido")
            sock.close()
            return False
    except Exception as e:
        print(f"❌ SSH: Falhou - {e}")
        return False


def main():
    """Executa todos os testes."""
    print("=" * 50)
    print("TESTE DOS SERVIÇOS DO HONEYPOT")
    print("=" * 50)
    print()
    
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    
    results = []
    
    results.append(test_http(host))
    print()
    
    results.append(test_ftp(host))
    print()
    
    results.append(test_ssh(host))
    print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ Todos os testes passaram! ({passed}/{total})")
        return 0
    else:
        print(f"⚠️  Alguns testes falharam ({passed}/{total})")
        return 1


if __name__ == '__main__':
    sys.exit(main())
