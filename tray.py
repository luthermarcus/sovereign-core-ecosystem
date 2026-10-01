"""Sovereign Core OS - Optional GUI System Tray & Headless Status Adapter"""
from sos_platform import get_host_info

def get_tray_summary():
    info = get_host_info()
    mode = "GUI_TRAY_READY" if info["capabilities"]["has_gui_display"] else "HEADLESS_CLI_MODE"
    return f"SOS {info['os']} [{mode}] | In:{info['inbound_ip']} Out:{info['outbound_ip']}"
