#!/usr/bin/env python3
"""
PROTEÇÃO DE MÁQUINA COM MONITORAMENTO EM TEMPO REAL
Sistema que monitora e desliga a máquina automaticamente
se detectar: porno, mineração, pirataria
"""

import os
import sys
import subprocess
import time
import json
import threading
import platform
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import socket
import re

class ProtecaoMaquina:
    def __init__(self):
        self.sistema = platform.system()
        self.ativo = False
        self.config = self._carregar_config()
        self.historico = []
        self.processos_perigosos = self._carregar_processos_perigosos()
        self.sites_bloqueados = self._carregar_sites_bloqueados()
        
    # ============ CONFIGURAÇÃO ============
    
    def _carregar_config(self):
        """Carrega configuração do sistema"""
        return {
            "monitorar_processos": True,
            "monitorar_rede": True,
            "monitorar_downloads": True,
            "desligar_automatico": True,
            "delay_verificacao": 2,  # segundos
            "tempo_aviso": 10  # segundos antes de desligar
        }
    
    def _carregar_processos_perigosos(self):
        """Lista de processos perigosos conhecidos"""
        return {
            "mineradores": [
                "xmrig", "minergate", "kucoin", "cryptonight",
                "bitminer", "dwarfpool", "nicehash", "cgminer",
                "stratum", "ethminer", "claymore", "teamredminer",
                "nbminer", "gminer", "bminer", "lolminer"
            ],
            "porno": [
                "pornhub", "xvideos", "redtube", "youporn",
                "xnxx", "xhamster", "tube8", "pornoxo"
            ],
            "pirataria": [
                "thepiratebay", "kickasstorrent", "1337x",
                "torrentz2", "nyaa", "torrent", "magnet",
                "qbittorrent", "transmission", "utorrent",
                "bitcomet", "vuze", "deluge"
            ]
        }
    
    def _carregar_sites_bloqueados(self):
        """Sites a bloquear por tipo"""
        return {
            "porno": [
                "pornhub.com", "xvideos.com", "redtube.com",
                "youporn.com", "xnxx.com", "xhamster.com",
                "tube8.com", "pornoxo.com", "spankbang.com",
                "brazzers.com", "xnxxvideos.com", "freeporn.com"
            ],
            "pirataria": [
                "thepiratebay.org", "thepiratebay.vip",
                "kickasstorrent.to", "1337x.to", "torrentz2.eu",
                "nyaa.si", "rarbg.to", "torrent.com"
            ],
            "mineracao": [
                "stratum+tcp", "mining.pool", "hashpool",
                "nicehash.com", "minergate.com", "kucoin.com"
            ]
        }
    
    # ============ MENU PRINCIPAL ============
    
    def menu_principal(self):
        """Menu interativo principal"""
        while True:
            self._limpar_tela()
            print("=" * 70)
            print("🛡️  SISTEMA DE PROTEÇÃO DE MÁQUINA")
            print("=" * 70)
            print("\n[1] ▶️  INICIAR PROTEÇÃO (MONITORAMENTO)")
            print("[2] 🛑 PARAR PROTEÇÃO")
            print("[3] 📋 VER HISTORICO DE ATIVIDADES")
            print("[4] ⚙️  CONFIGURAÇÕES")
            print("[5] 🔍 VERIFICAÇÃO RÁPIDA")
            print("[6] 📊 STATUS DO SISTEMA")
            print("[0] ❌ SAIR")
            print("\n" + "=" * 70)
            
            opcao = input("\n👉 Digite a opção (0-6): ").strip()
            
            if opcao == "1":
                self.iniciar_protecao()
            elif opcao == "2":
                self.parar_protecao()
            elif opcao == "3":
                self.ver_historico()
            elif opcao == "4":
                self.menu_configuracoes()
            elif opcao == "5":
                self.verificacao_rapida()
            elif opcao == "6":
                self.status_sistema()
            elif opcao == "0":
                print("\n❌ Encerrando... Até logo!")
                sys.exit(0)
            else:
                input("❌ Opção inválida! Pressione ENTER...")
    
    def _limpar_tela(self):
        """Limpa a tela do terminal"""
        if self.sistema == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    
    # ============ INICIAR PROTEÇÃO ============
    
    def iniciar_protecao(self):
        """Inicia monitoramento em tempo real"""
        self._limpar_tela()
        print("=" * 70)
        print("🟢 PROTEÇÃO INICIADA")
        print("=" * 70)
        print("\n⏳ Monitorando máquina em tempo real...")
        print("🔍 Verificando processos, rede e downloads...")
        print("\n⚠️  A máquina será DESLIGADA automaticamente se detectar:")
        print("   • 🔞 Conteúdo adulto/pornográfico")
        print("   • ⚡ Mineradores de criptomoedas")
        print("   • 🏴 Torrent/Pirataria")
        print("\n(Pressione CTRL+C para parar, mas recomenda-se deixar rodando)")
        print("\n" + "=" * 70)
        
        self.ativo = True
        
        try:
            while self.ativo:
                # Executa verificações
                self._monitorar_processos()
                self._monitorar_rede()
                self._monitorar_downloads()
                
                time.sleep(self.config["delay_verificacao"])
        
        except KeyboardInterrupt:
            print("\n\n⏸️  Proteção pausada pelo usuário")
            self.ativo = False
            input("Pressione ENTER para voltar ao menu...")
    
    # ============ MONITORAMENTO DE PROCESSOS ============
    
    def _monitorar_processos(self):
        """Monitora processos em execução"""
        try:
            if self.sistema == "Windows":
                processos = self._listar_processos_windows()
            else:
                processos = self._listar_processos_linux()
            
            # Verifica cada processo
            for proc in processos:
                proc_lower = proc.lower()
                
                # Verifica mineradores
                for minerador in self.processos_perigosos["mineradores"]:
                    if minerador.lower() in proc_lower:
                        self._ameaca_detectada(
                            tipo="MINERAÇÃO",
                            descricao=f"Processo de mineração detectado: {proc}",
                            risco="CRÍTICO"
                        )
                
                # Verifica pirataria
                for pirata in self.processos_perigosos["pirataria"]:
                    if pirata.lower() in proc_lower:
                        self._ameaca_detectada(
                            tipo="PIRATARIA",
                            descricao=f"Cliente Torrent detectado: {proc}",
                            risco="ALTO"
                        )
        
        except Exception as e:
            pass  # Silenciosamente ignora erros de permissão
    
    def _listar_processos_windows(self):
        """Lista processos no Windows"""
        try:
            resultado = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return resultado.stdout.split('\n')
        except:
            return []
    
    def _listar_processos_linux(self):
        """Lista processos no Linux"""
        try:
            resultado = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return resultado.stdout.split('\n')
        except:
            return []
    
    # ============ MONITORAMENTO DE REDE ============
    
    def _monitorar_rede(self):
        """Monitora conexões de rede"""
        try:
            if self.sistema == "Windows":
                conexoes = self._listar_conexoes_windows()
            else:
                conexoes = self._listar_conexoes_linux()
            
            for conexao in conexoes:
                # Verifica sites de porno
                for site_porno in self.sites_bloqueados["porno"]:
                    if site_porno.lower() in conexao.lower():
                        self._ameaca_detectada(
                            tipo="PORNO",
                            descricao=f"Acesso a site adulto detectado: {site_porno}",
                            risco="ALTO"
                        )
                
                # Verifica pirataria
                for site_pirata in self.sites_bloqueados["pirataria"]:
                    if site_pirata.lower() in conexao.lower():
                        self._ameaca_detectada(
                            tipo="PIRATARIA",
                            descricao=f"Acesso a site de pirataria detectado: {site_pirata}",
                            risco="CRÍTICO"
                        )
                
                # Verifica mineração
                if "stratum+tcp" in conexao.lower() or "mining.pool" in conexao.lower():
                    self._ameaca_detectada(
                        tipo="MINERAÇÃO",
                        descricao="Conexão de mineração detectada",
                        risco="CRÍTICO"
                    )
        
        except Exception as e:
            pass
    
    def _listar_conexoes_windows(self):
        """Lista conexões no Windows"""
        try:
            resultado = subprocess.run(
                ["netstat", "-bn"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return resultado.stdout.split('\n')
        except:
            return []
    
    def _listar_conexoes_linux(self):
        """Lista conexões no Linux"""
        try:
            resultado = subprocess.run(
                ["netstat", "-an"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return resultado.stdout.split('\n')
        except:
            return []
    
    # ============ MONITORAMENTO DE DOWNLOADS ============
    
    def _monitorar_downloads(self):
        """Monitora pasta de downloads"""
        try:
            if self.sistema == "Windows":
                download_path = Path.home() / "Downloads"
            else:
                download_path = Path.home() / "Downloads"
            
            if not download_path.exists():
                return
            
            for arquivo in download_path.glob("*"):
                if arquivo.is_file():
                    nome = arquivo.name.lower()
                    
                    # Verifica extensões suspeitas
                    extensoes_pirata = [".torrent", ".magnet"]
                    for ext in extensoes_pirata:
                        if nome.endswith(ext):
                            self._ameaca_detectada(
                                tipo="PIRATARIA",
                                descricao=f"Arquivo Torrent detectado: {arquivo.name}",
                                risco="CRÍTICO"
                            )
        
        except Exception as e:
            pass
    
    # ============ DETECÇÃO DE AMEAÇA ============
    
    def _ameaca_detectada(self, tipo: str, descricao: str, risco: str):
        """Processa detecção de ameaça"""
        # Registra no histórico
        evento = {
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
            "descricao": descricao,
            "risco": risco
        }
        self.historico.append(evento)
        
        # Exibe alerta
        print(f"\n{'⚠️' * 20}")
        print(f"🚨 AMEAÇA DETECTADA!")
        print(f"Tipo: {tipo}")
        print(f"Risco: {risco}")
        print(f"Detalhes: {descricao}")
        print(f"{'⚠️' * 20}")
        
        # Se risco crítico, desliga máquina
        if risco == "CRÍTICO":
            self._desligar_maquina()
    
    # ============ DESLIGAMENTO AUTOMÁTICO ============
    
    def _desligar_maquina(self):
        """Desliga a máquina automaticamente"""
        self._limpar_tela()
        
        print("=" * 70)
        print("🔴 MÁQUINA SERÁ DESLIGADA POR SEGURANÇA!")
        print("=" * 70)
        print("\n⚠️  AMEAÇA CRÍTICA DETECTADA!")
        print("\n🛑 A máquina será desligada em 10 segundos...")
        print("📝 Salve seus arquivos agora!")
        print("\nPara cancelar, feche o programa (pode pedir privilégios admin)")
        
        # Countdown
        for i in range(10, 0, -1):
            print(f"\r⏱️  Desligando em {i} segundos...", end="", flush=True)
            time.sleep(1)
        
        print("\n\n🔴 DESLIGANDO AGORA...")
        
        # Desliga conforme o SO
        if self.sistema == "Windows":
            os.system("shutdown /s /f /t 0")
        else:
            os.system("sudo shutdown -h now")
    
    # ============ PARAR PROTEÇÃO ============
    
    def parar_protecao(self):
        """Para o monitoramento"""
        self.ativo = False
        print("\n✅ Proteção parada")
        input("Pressione ENTER...")
    
    # ============ VERIFICAÇÃO RÁPIDA ============
    
    def verificacao_rapida(self):
        """Faz uma verificação única sem deixar rodando"""
        self._limpar_tela()
        print("=" * 70)
        print("🔍 VERIFICAÇÃO RÁPIDA")
        print("=" * 70)
        
        print("\n[1/3] Verificando processos...")
        self._monitorar_processos()
        
        print("[2/3] Verificando rede...")
        self._monitorar_rede()
        
        print("[3/3] Verificando downloads...")
        self._monitorar_downloads()
        
        if len(self.historico) == 0:
            print("\n✅ Nenhuma ameaça detectada!")
        else:
            print(f"\n⚠️  {len(self.historico)} ameaça(s) detectada(s)!")
        
        input("\nPressione ENTER para voltar...")
    
    # ============ HISTÓRICO ============
    
    def ver_historico(self):
        """Exibe histórico de ameaças detectadas"""
        self._limpar_tela()
        print("=" * 70)
        print("📋 HISTÓRICO DE ATIVIDADES SUSPEITAS")
        print("=" * 70)
        
        if len(self.historico) == 0:
            print("\n✅ Nenhuma ameaça detectada até agora!")
        else:
            for i, evento in enumerate(self.historico, 1):
                print(f"\n[{i}] {evento['timestamp']}")
                print(f"    Tipo: {evento['tipo']}")
                print(f"    Risco: {evento['risco']}")
                print(f"    Detalhes: {evento['descricao']}")
        
        input("\nPressione ENTER para voltar...")
    
    # ============ CONFIGURAÇÕES ============
    
    def menu_configuracoes(self):
        """Menu de configurações"""
        while True:
            self._limpar_tela()
            print("=" * 70)
            print("⚙️  CONFIGURAÇÕES")
            print("=" * 70)
            
            print(f"\n[1] Monitorar Processos: {'✅' if self.config['monitorar_processos'] else '❌'}")
            print(f"[2] Monitorar Rede: {'✅' if self.config['monitorar_rede'] else '❌'}")
            print(f"[3] Monitorar Downloads: {'✅' if self.config['monitorar_downloads'] else '❌'}")
            print(f"[4] Desligar Automático: {'✅' if self.config['desligar_automatico'] else '❌'}")
            print(f"[5] Delay Verificação: {self.config['delay_verificacao']}s")
            print(f"[6] Tempo Aviso: {self.config['tempo_aviso']}s")
            print("[0] Voltar")
            
            opcao = input("\n👉 Escolha: ").strip()
            
            if opcao == "1":
                self.config['monitorar_processos'] = not self.config['monitorar_processos']
            elif opcao == "2":
                self.config['monitorar_rede'] = not self.config['monitorar_rede']
            elif opcao == "3":
                self.config['monitorar_downloads'] = not self.config['monitorar_downloads']
            elif opcao == "4":
                self.config['desligar_automatico'] = not self.config['desligar_automatico']
            elif opcao == "5":
                try:
                    valor = int(input("Digite novo delay (segundos): "))
                    self.config['delay_verificacao'] = valor
                except ValueError:
                    pass
            elif opcao == "6":
                try:
                    valor = int(input("Digite novo tempo de aviso (segundos): "))
                    self.config['tempo_aviso'] = valor
                except ValueError:
                    pass
            elif opcao == "0":
                break
    
    # ============ STATUS DO SISTEMA ============
    
    def status_sistema(self):
        """Exibe status geral do sistema"""
        self._limpar_tela()
        print("=" * 70)
        print("📊 STATUS DO SISTEMA")
        print("=" * 70)
        
        print(f"\n💻 Sistema Operacional: {platform.platform()}")
        print(f"🔵 Status Proteção: {'🟢 ATIVA' if self.ativo else '🔴 INATIVA'}")
        print(f"\n⚙️  Configurações:")
        print(f"   • Monitorar Processos: {'✅' if self.config['monitorar_processos'] else '❌'}")
        print(f"   • Monitorar Rede: {'✅' if self.config['monitorar_rede'] else '❌'}")
        print(f"   • Monitorar Downloads: {'✅' if self.config['monitorar_downloads'] else '❌'}")
        print(f"   • Desligar Automático: {'✅' if self.config['desligar_automatico'] else '❌'}")
        
        print(f"\n📋 Histórico:")
        print(f"   • Total de Ameaças Detectadas: {len(self.historico)}")
        
        if self.historico:
            tipos = {}
            for evento in self.historico:
                tipos[evento['tipo']] = tipos.get(evento['tipo'], 0) + 1
            
            print(f"\n   Por Tipo:")
            for tipo, count in tipos.items():
                print(f"     - {tipo}: {count}")
        
        input("\nPressione ENTER para voltar...")


# ============ FUNÇÃO PRINCIPAL ============

def main():
    """Ponto de entrada"""
    try:
        # Verifica privilégios admin no Windows
        if platform.system() == "Windows":
            import ctypes
            try:
                is_admin = ctypes.windll.shell.IsUserAnAdmin()
            except:
                is_admin = False
            
            if not is_admin:
                print("⚠️  AVISO: Execute como Administrador para melhor proteção!")
                print("Continuando de qualquer forma...\n")
                input("Pressione ENTER para continuar...")
        
        # Inicia sistema
        protecao = ProtecaoMaquina()
        protecao.menu_principal()
    
    except KeyboardInterrupt:
        print("\n\n❌ Programa encerrado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
