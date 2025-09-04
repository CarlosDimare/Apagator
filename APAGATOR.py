#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
import threading
import subprocess
from datetime import datetime, timedelta

# --- Configuración ---
MINUTOS_PARA_APAGAR = 60
CHECK_INTERVAL = 5  # Verificar actividad cada 5 segundos
# -------------------

# --- Arte ASCII ---
BANNER = r"""
 █████╗ ██████╗  █████╗  ██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████║██████╔╝███████║██║  ███╗███████║   ██║   ██║   ██║██████╔╝
██╔══██║██╔═══╝ ██╔══██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗
██║  ██║██║     ██║  ██║╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                     
"""

ASCII_DIGITS = {
    '0': [
        "  ███  ",
        " █   █ ",
        "█     █",
        "█     █",
        " █   █ ",
        "  ███  "
    ],
    '1': [
        "  ██  ",
        " ███  ",
        "  ██  ",
        "  ██  ",
        "  ██  ",
        "███████"
    ],
    '2': [
        " █████ ",
        "█     █",
        "     █ ",
        "   ██  ",
        " ██    ",
        "███████"
    ],
    '3': [
        " █████ ",
        "█     █",
        "     █ ",
        "  ████ ",
        "█     █",
        " █████ "
    ],
    '4': [
        "█    █ ",
        "█    █ ",
        "█    █ ",
        "███████",
        "     █ ",
        "     █ "
    ],
    '5': [
        "███████",
        "█      ",
        "██████ ",
        "     █ ",
        "█    █ ",
        " █████ "
    ],
    '6': [
        " █████ ",
        "█      ",
        "██████ ",
        "█     █",
        "█     █",
        " █████ "
    ],
    '7': [
        "███████",
        "     █ ",
        "    █  ",
        "   █   ",
        "  █    ",
        " █     "
    ],
    '8': [
        " █████ ",
        "█     █",
        " █████ ",
        "█     █",
        "█     █",
        " █████ "
    ],
    '9': [
        " █████ ",
        "█     █",
        "█     █",
        " ██████",
        "      █",
        " █████ "
    ],
    ':': [
        "   ",
        " ██",
        " ██",
        "   ",
        " ██",
        " ██"
    ]
}

class DependencyManager:
    """Clase para detectar y instalar dependencias automáticamente."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.distro = None
        if self.system == "linux":
            self._detect_linux_distro()
    
    def _detect_linux_distro(self):
        """Detecta la distribución de Linux."""
        try:
            # Intentar con lsb_release
            result = subprocess.run(['lsb_release', '-is'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.distro = result.stdout.strip().lower()
                return
        except:
            pass
        
        # Intentar con archivos del sistema
        distro_files = {
            '/etc/debian_version': 'debian',
            '/etc/redhat-release': 'redhat',
            '/etc/fedora-release': 'fedora',
            '/etc/arch-release': 'arch',
            '/etc/suse-release': 'suse'
        }
        
        for file_path, distro_name in distro_files.items():
            if os.path.exists(file_path):
                self.distro = distro_name
                return
        
        # Fallback a ubuntu si es debian-like
        if os.path.exists('/etc/apt'):
            self.distro = 'ubuntu'
        elif os.path.exists('/etc/yum.conf') or os.path.exists('/etc/dnf'):
            self.distro = 'fedora'
    
    def _run_command(self, command, shell=False, timeout=30):
        """Ejecuta un comando con manejo de errores."""
        try:
            if isinstance(command, str) and not shell:
                command = command.split()
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=timeout, 
                shell=shell
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout"
        except Exception as e:
            return False, "", str(e)
    
    def install_python_package(self, package):
        """Instala un paquete de Python usando pip."""
        print(f"📦 Instalando paquete Python: {package}")
        
        # Intentar con pip3 primero, luego pip
        for pip_cmd in ['pip3', 'pip']:
            try:
                success, stdout, stderr = self._run_command([pip_cmd, 'install', package])
                if success:
                    print(f"✅ {package} instalado correctamente con {pip_cmd}")
                    return True
                else:
                    print(f"❌ Error con {pip_cmd}: {stderr}")
            except:
                continue
        
        # Intentar con python -m pip
        try:
            success, stdout, stderr = self._run_command([sys.executable, '-m', 'pip', 'install', package])
            if success:
                print(f"✅ {package} instalado correctamente con python -m pip")
                return True
        except:
            pass
        
        print(f"❌ No se pudo instalar {package}")
        return False
    
    def install_system_package_linux(self, package):
        """Instala un paquete del sistema en Linux."""
        print(f"📦 Instalando paquete del sistema: {package}")
        
        package_managers = {
            'ubuntu': ['sudo', 'apt-get', 'update', '&&', 'sudo', 'apt-get', 'install', '-y'],
            'debian': ['sudo', 'apt-get', 'update', '&&', 'sudo', 'apt-get', 'install', '-y'],
            'fedora': ['sudo', 'dnf', 'install', '-y'],
            'redhat': ['sudo', 'yum', 'install', '-y'],
            'arch': ['sudo', 'pacman', '-S', '--noconfirm'],
            'suse': ['sudo', 'zypper', 'install', '-y']
        }
        
        # Mapeo de nombres de paquetes por distribución
        package_mapping = {
            'xprintidle': {
                'ubuntu': 'xprintidle',
                'debian': 'xprintidle', 
                'fedora': 'xprintidle',
                'redhat': 'xprintidle',
                'arch': 'xprintidle',
                'suse': 'xprintidle'
            }
        }
        
        if self.distro and self.distro in package_managers:
            actual_package = package_mapping.get(package, {}).get(self.distro, package)
            
            if 'apt-get' in package_managers[self.distro]:
                # Para sistemas basados en APT
                print("🔄 Actualizando lista de paquetes...")
                success, _, _ = self._run_command(['sudo', 'apt-get', 'update'], timeout=60)
                if not success:
                    print("⚠️ No se pudo actualizar la lista de paquetes")
                
                success, stdout, stderr = self._run_command(
                    ['sudo', 'apt-get', 'install', '-y', actual_package], 
                    timeout=120
                )
            else:
                # Para otros gestores de paquetes
                cmd = package_managers[self.distro] + [actual_package]
                success, stdout, stderr = self._run_command(cmd, timeout=120)
            
            if success:
                print(f"✅ {package} instalado correctamente")
                return True
            else:
                print(f"❌ Error instalando {package}: {stderr}")
        else:
            print(f"⚠️ Distribución no soportada o no detectada: {self.distro}")
        
        return False
    
    def check_and_install_dependencies(self):
        """Verifica e instala todas las dependencias necesarias."""
        print("🔍 Verificando dependencias del sistema...")
        print(f"💻 Sistema detectado: {platform.system()}")
        
        if self.system == "linux":
            print(f"🐧 Distribución Linux: {self.distro or 'No detectada'}")
        
        dependencies_ok = True
        
        if self.system == "windows":
            dependencies_ok = self._setup_windows_deps()
        elif self.system == "linux":
            dependencies_ok = self._setup_linux_deps()
        elif self.system == "darwin":
            dependencies_ok = self._setup_macos_deps()
        else:
            print(f"❌ Sistema operativo no soportado: {self.system}")
            return False
        
        if dependencies_ok:
            print("✅ Todas las dependencias están disponibles")
        else:
            print("❌ Faltan dependencias críticas")
        
        return dependencies_ok
    
    def _setup_windows_deps(self):
        """Configura dependencias para Windows."""
        print("🪟 Configurando dependencias para Windows...")
        
        # Verificar si pywin32 está disponible
        try:
            import win32api
            import ctypes
            print("✅ pywin32 ya está instalado")
            return True
        except ImportError:
            print("❌ pywin32 no está disponible")
            
            # Intentar instalarlo
            if self.install_python_package('pywin32'):
                try:
                    import win32api
                    print("✅ pywin32 instalado y funcionando")
                    return True
                except ImportError:
                    print("❌ pywin32 instalado pero no funciona. Puede requerir reinicio.")
                    return False
            else:
                print("❌ No se pudo instalar pywin32")
                print("💡 Intenta manualmente: pip install pywin32")
                return False
    
    def _setup_linux_deps(self):
        """Configura dependencias para Linux."""
        print("🐧 Configurando dependencias para Linux...")
        
        # Verificar xprintidle
        success, _, _ = self._run_command(['which', 'xprintidle'])
        if success:
            print("✅ xprintidle ya está instalado")
            return True
        
        print("❌ xprintidle no está disponible")
        print("🔧 Intentando instalar xprintidle...")
        
        if self.install_system_package_linux('xprintidle'):
            # Verificar nuevamente
            success, _, _ = self._run_command(['which', 'xprintidle'])
            if success:
                print("✅ xprintidle instalado correctamente")
                return True
            else:
                print("❌ xprintidle instalado pero no está en el PATH")
        
        print("❌ No se pudo instalar xprintidle automáticamente")
        print("💡 Intenta manualmente:")
        print("   Ubuntu/Debian: sudo apt-get install xprintidle")
        print("   Fedora: sudo dnf install xprintidle")
        print("   Arch: sudo pacman -S xprintidle")
        
        return False
    
    def _setup_macos_deps(self):
        """Configura dependencias para macOS."""
        print("🍎 Configurando dependencias para macOS...")
        
        # Verificar ioreg (debería estar disponible por defecto)
        success, _, _ = self._run_command(['which', 'ioreg'])
        if success:
            print("✅ ioreg disponible (incluido en macOS)")
            return True
        else:
            print("❌ ioreg no encontrado (inusual en macOS)")
            return False

class ActivityMonitor:
    """Clase para monitorear la actividad del usuario."""
    
    def __init__(self):
        self.system = platform.system()
        self.last_activity_time = datetime.now()
        self.last_idle_time = 0
        self.initialized = False
        self.use_pywin32 = False  # Flag para Windows
        
        if self.system == "Windows":
            self._init_windows()
        elif self.system == "Linux":
            self._init_linux()
        elif self.system == "Darwin":
            self._init_macos()
    
    def _init_windows(self):
        """Inicialización para Windows."""
        try:
            import ctypes
            import win32api
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            self.initialized = True
            print("✅ Monitor de actividad Windows inicializado")
        except Exception as e:
            print(f"❌ Error inicializando monitor Windows: {e}")
            self.initialized = False
    
    def _init_linux(self):
        """Inicialización para Linux."""
        try:
            result = subprocess.run(['which', 'xprintidle'], capture_output=True)
            if result.returncode == 0:
                self.initialized = True
                print("✅ Monitor de actividad Linux inicializado")
            else:
                print("❌ xprintidle no disponible")
                self.initialized = False
        except Exception as e:
            print(f"❌ Error inicializando monitor Linux: {e}")
            self.initialized = False
    
    def _init_macos(self):
        """Inicialización para macOS."""
        try:
            result = subprocess.run(['which', 'ioreg'], capture_output=True)
            if result.returncode == 0:
                self.initialized = True
                print("✅ Monitor de actividad macOS inicializado")
            else:
                print("❌ ioreg no disponible")
                self.initialized = False
        except Exception as e:
            print(f"❌ Error inicializando monitor macOS: {e}")
            self.initialized = False
    
    def get_idle_time_windows(self):
        """Obtiene tiempo de inactividad en Windows."""
        try:
            import ctypes
            
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_ulong)]
            
            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
            
            if self.user32.GetLastInputInfo(ctypes.byref(lii)):
                current_time = self.kernel32.GetTickCount()
                idle_time = (current_time - lii.dwTime) / 1000.0
                return idle_time
            return 0
        except Exception as e:
            print(f"❌ Error obteniendo idle time Windows: {e}")
            return 0
    
    def get_idle_time_linux(self):
        """Obtiene tiempo de inactividad en Linux."""
        try:
            result = subprocess.run(['xprintidle'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                idle_ms = int(result.stdout.strip())
                return idle_ms / 1000.0
            return 0
        except Exception as e:
            print(f"❌ Error obteniendo idle time Linux: {e}")
            return 0
    
    def get_idle_time_macos(self):
        """Obtiene tiempo de inactividad en macOS."""
        try:
            import re
            result = subprocess.run([
                'ioreg', '-c', 'IOHIDSystem'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'HIDIdleTime' in line:
                        match = re.search(r'(\d+)', line)
                        if match:
                            idle_ns = int(match.group(1))
                            return idle_ns / 1_000_000_000.0
            return 0
        except Exception as e:
            print(f"❌ Error obteniendo idle time macOS: {e}")
            return 0
    
    def get_idle_time(self):
        """Obtiene el tiempo de inactividad del sistema."""
        if not self.initialized:
            return 0
            
        if self.system == "Windows":
            return self.get_idle_time_windows()
        elif self.system == "Linux":
            return self.get_idle_time_linux()
        elif self.system == "Darwin":
            return self.get_idle_time_macos()
        return 0
    
    def is_user_active(self):
        """Determina si hay actividad del usuario."""
        if not self.initialized:
            return False
            
        current_idle_time = self.get_idle_time()
        
        # Si el tiempo de inactividad disminuyó, hubo actividad
        if current_idle_time < self.last_idle_time:
            self.last_activity_time = datetime.now()
            self.last_idle_time = current_idle_time
            return True
        
        # Si la inactividad es muy baja, considerar activo
        if current_idle_time < 5:
            self.last_activity_time = datetime.now()
            self.last_idle_time = current_idle_time
            return True
        
        self.last_idle_time = current_idle_time
        return False
    
    def get_inactive_duration(self):
        """Retorna la duración de inactividad en segundos."""
        return self.get_idle_time() if self.initialized else 0

class ShutdownTimer:
    """Temporizador de apagado con detección de actividad."""
    
    def __init__(self, minutes=60):
        self.minutes = minutes
        self.seconds_left = minutes * 60
        self.running = True
        self.activity_monitor = ActivityMonitor()
        self.lock = threading.Lock()
        self.activity_detected = False
    
    def clear_screen(self):
        """Limpia la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_countdown(self):
        """Muestra el contador y estado."""
        with self.lock:
            self.clear_screen()
            
            # Banner
            print("\033[92m" + BANNER + "\033[0m")
            
            # Tiempo restante
            mins, secs = divmod(max(0, int(self.seconds_left)), 60)
            time_str = f"{mins:02d}:{secs:02d}"
            
            # ASCII del tiempo
            output_lines = [""] * len(ASCII_DIGITS['0'])
            for char in time_str:
                char_art = ASCII_DIGITS.get(char, [""] * len(ASCII_DIGITS['0']))
                for i in range(len(output_lines)):
                    output_lines[i] += char_art[i] + "  "
            
            print("\033[91m", end="")
            for line in output_lines:
                print(f"        {line}")
            print("\033[0m")
            
            # Estado del sistema
            inactive_time = self.activity_monitor.get_inactive_duration()
            mins_inactive = int(inactive_time // 60)
            
            print(f"\n🔥 Apagado automático en: {mins}:{secs:02d}")
            print(f"⏱️  Inactividad detectada: {mins_inactive} minutos")
            
            if self.activity_detected:
                print("\033[92m✅ ¡ACTIVIDAD DETECTADA! Contador reiniciado\033[0m")
                self.activity_detected = False
            else:
                status = "🟢 Funcionando" if self.activity_monitor.initialized else "🔴 Sin monitor"
                print(f"👤 Monitor de actividad: {status}")
            
            print(f"💻 Sistema: {platform.system()}")
            print("⚠️  Presiona Ctrl+C para cancelar")
    
    def monitor_activity(self):
        """Hilo para monitorear actividad."""
        while self.running:
            try:
                if self.activity_monitor.is_user_active():
                    with self.lock:
                        self.seconds_left = self.minutes * 60
                        self.activity_detected = True
                
                time.sleep(CHECK_INTERVAL)
            except Exception as e:
                print(f"❌ Error en monitor: {e}")
                time.sleep(CHECK_INTERVAL)
    
    def countdown_timer(self):
        """Contador regresivo."""
        while self.running and self.seconds_left > 0:
            self.display_countdown()
            time.sleep(1)
            
            with self.lock:
                self.seconds_left -= 1
        
        if self.running and self.seconds_left <= 0:
            self.shutdown_computer()
    
    def shutdown_computer(self):
        """Ejecuta el apagado."""
        self.clear_screen()
        print("\033[91m" + "="*60 + "\033[0m")
        print("\033[91m" + "⚠️  SIN ACTIVIDAD DURANTE 60 MINUTOS" + "\033[0m")
        print("\033[91m" + "🔥 INICIANDO APAGADO..." + "\033[0m")
        print("\033[91m" + "="*60 + "\033[0m")
        
        for i in range(10, 0, -1):
            print(f"\n⏰ Apagando en {i} segundos... (Ctrl+C para cancelar)")
            time.sleep(1)
        
        system = platform.system().lower()
        try:
            if system == "windows":
                os.system('shutdown /s /t 5 /c "APAGATOR: Sin actividad durante 60 min"')
            elif system == "linux":
                os.system('sudo shutdown -h +1 "APAGATOR: Sin actividad durante 60 min"')
            elif system == "darwin":
                os.system('sudo shutdown -h +1')
        except Exception as e:
            print(f"❌ Error en apagado: {e}")
    
    def start(self):
        """Inicia el sistema."""
        print("🚀 Iniciando APAGATOR...")
        print(f"⏰ Apagado tras {self.minutes} minutos sin actividad")
        time.sleep(2)
        
        try:
            # Hilo de monitoreo
            activity_thread = threading.Thread(target=self.monitor_activity, daemon=True)
            activity_thread.start()
            
            # Contador principal
            self.countdown_timer()
            
        except KeyboardInterrupt:
            self.running = False
            self.clear_screen()
            print("\n🛑 APAGADO CANCELADO")
            print("✅ Sistema detenido por el usuario")
            print("👋 ¡Hasta luego!")
        except Exception as e:
            self.running = False
            print(f"\n❌ Error inesperado: {e}")

def main():
    """Función principal con instalación automática de dependencias."""
    print("🔧 APAGATOR - Instalador y Configurador Automático")
    print("="*55)
    
    # Verificar e instalar dependencias
    dep_manager = DependencyManager()
    if not dep_manager.check_and_install_dependencies():
        print("\n❌ No se pudieron configurar todas las dependencias")
        print("El programa puede no funcionar correctamente")
        
        response = input("\n¿Continuar de todos modos? (s/n): ").lower().strip()
        if response not in ['s', 'si', 'sí', 'y', 'yes']:
            print("👋 Saliendo...")
            return
    
    print("\n" + "="*55)
    
    # Verificar permisos en sistemas Unix
    if platform.system() in ["Linux", "Darwin"]:
        if os.geteuid() != 0:
            print("⚠️ Se recomienda ejecutar como administrador (sudo)")
            print("   Esto garantiza que el apagado funcione correctamente")
            response = input("¿Continuar sin privilegios de administrador? (s/n): ").lower().strip()
            if response not in ['s', 'si', 'sí', 'y', 'yes']:
                print("💡 Ejecuta: sudo python3 apagador.py")
                return
    
    # Iniciar el sistema
    print("\n🎯 Iniciando sistema de apagado inteligente...")
    timer = ShutdownTimer(MINUTOS_PARA_APAGAR)
    timer.start()

if __name__ == "__main__":
    main()