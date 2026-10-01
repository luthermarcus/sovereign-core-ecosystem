"""
Sovereign Core OS (SOS) - Universal Cross-OS Hardware & OS Abstraction Layer (HAL)
Includes RAM-Mapped SQLite WAL acceleration and Kernel Network Proof-of-Bandwidth.
"""
import os
import json
import socket
import shutil
import sqlite3
import platform
import tempfile
import subprocess

LOCAL_PROFILE_PATH = os.path.expanduser("~/.sos_host_profile.json")

def load_local_profile():
    if os.path.exists(LOCAL_PROFILE_PATH):
        try:
            with open(LOCAL_PROFILE_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def get_kernel_bandwidth_proof():
    """Reads kernel /proc/net/dev counters to prevent Sybil DePIN bandwidth spoofing."""
    interfaces = {}
    if os.path.exists("/proc/net/dev"):
        try:
            with open("/proc/net/dev", "r") as f:
                for line in f.readlines()[2:]:
                    if ":" in line:
                        iface, data = line.split(":", 1)
                        iface = iface.strip()
                        fields = data.split()
                        if len(fields) >= 9 and iface != "lo":
                            rx_bytes = int(fields[0])
                            tx_bytes = int(fields[8])
                            interfaces[iface] = {"rx_mb": round(rx_bytes / 1048576, 2), "tx_mb": round(tx_bytes / 1048576, 2)}
        except Exception:
            pass
    total_tx_mb = round(sum(v["tx_mb"] for v in interfaces.values()), 2)
    return {
        "verified_kernel_tx_mb": total_tx_mb,
        "proof_of_bandwidth_valid": total_tx_mb > 0 or platform.system() != "Linux",
        "active_interfaces": interfaces
    }

def get_network_planes():
    profile = load_local_profile()
    outbound_ip = profile.get("preferred_outbound_ip")
    if not outbound_ip:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            outbound_ip = s.getsockname()[0]
        except Exception:
            outbound_ip = "127.0.0.1"
        finally:
            s.close()

    inbound_ip = profile.get("preferred_inbound_ip")
    if not inbound_ip:
        ssh_conn = os.environ.get("SSH_CONNECTION", "")
        if ssh_conn and len(ssh_conn.split()) >= 3:
            inbound_ip = ssh_conn.split()[2]

    all_ips = []
    if shutil.which("hostname"):
        try:
            out = subprocess.check_output(["hostname", "-I"], stderr=subprocess.DEVNULL).decode().split()
            all_ips = [ip for ip in out if not ip.startswith("127.") and not ip.startswith("172.17.")]
        except Exception:
            pass

    if not inbound_ip:
        for ip in all_ips:
            if ip != outbound_ip:
                inbound_ip = ip
                break
    if not inbound_ip:
        inbound_ip = outbound_ip

    return {
        "inbound_ip": inbound_ip,
        "outbound_ip": outbound_ip,
        "dual_homed": inbound_ip != outbound_ip,
        "all_ips": all_ips or [outbound_ip]
    }

def get_os_capabilities():
    sys_name = platform.system()
    tcp_cc = "standard"
    if os.path.exists("/proc/sys/net/ipv4/tcp_congestion_control"):
        try:
            tcp_cc = open("/proc/sys/net/ipv4/tcp_congestion_control").read().strip()
        except Exception:
            pass
    return {
        "os": sys_name,
        "has_dev_shm": os.path.isdir("/dev/shm") and os.access("/dev/shm", os.W_OK),
        "has_systemd": bool(shutil.which("systemctl")),
        "has_ufw": bool(shutil.which("ufw")),
        "has_fail2ban": bool(shutil.which("fail2ban-client")),
        "has_apparmor": os.path.exists("/sys/module/apparmor"),
        "has_docker": bool(shutil.which("docker")),
        "tcp_congestion_control": tcp_cc,
        "has_termux": bool(os.environ.get("PREFIX", "").endswith("com.termux/files/usr")),
        "has_gui_display": bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") or sys_name in ("Windows", "Darwin"))
    }

def get_host_info():
    planes = get_network_planes()
    caps = get_os_capabilities()
    bw = get_kernel_bandwidth_proof()
    return {
        "os": caps["os"],
        "release": platform.release(),
        "arch": platform.machine(),
        "ip": planes["outbound_ip"],
        "inbound_ip": planes["inbound_ip"],
        "outbound_ip": planes["outbound_ip"],
        "dual_homed": planes["dual_homed"],
        "capabilities": caps,
        "bandwidth_proof": bw
    }

def get_ram_ledger_dir():
    if os.path.isdir("/dev/shm") and os.access("/dev/shm", os.W_OK):
        return "/dev/shm"
    prefix_tmp = os.environ.get("PREFIX", "")
    if prefix_tmp and os.path.isdir(os.path.join(prefix_tmp, "tmp")):
        return os.path.join(prefix_tmp, "tmp")
    return tempfile.gettempdir()

def connect_wal_db(db_name):
    ledger_dir = get_ram_ledger_dir()
    db_path = os.path.join(ledger_dir, db_name)
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
    except sqlite3.OperationalError:
        uid = os.getuid() if hasattr(os, "getuid") else "user"
        db_path = os.path.join(ledger_dir, f"sos_{uid}_{db_name}")
        conn = sqlite3.connect(db_path, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA mmap_size=16777216;")
    conn.execute("PRAGMA journal_size_limit=5242880;")
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    if os.name == "posix" and os.path.exists(db_path):
        try:
            os.chmod(db_path, 0o600)
        except PermissionError:
            pass
    return conn
