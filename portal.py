from flask import Flask
import paramiko
import re

app = Flask(__name__)

HOSTNAME_MAP = {
    '192.168.1.100': 'percom25-pc-01',
    '192.168.1.101': 'rs500',
    '192.168.1.102': 'pixel-9-pro-xl',
    '192.168.1.103': 'unitree',
    '192.168.1.104': 'iphone',
    '192.168.1.105': 'mpsc-aorus-15p-yd',
    '192.168.1.106': 'mac',
    '192.168.1.107': 'anuradha',
    '192.168.1.108': 'jumman-desktop-nvidia-isaac',
    '192.168.1.109': 'milind-hp-envy-desktop',
    '192.168.1.110': 'laptop-9mscefqt',
    '192.168.1.120': 'milind-s-tab-active3',
}

def get_devices():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.1.1', username='admin', password='mpsc1234',
                   allow_agent=False, look_for_keys=False, timeout=30,
                   disabled_algorithms={'kex': ['diffie-hellman-group-exchange-sha256']})
    stdin, stdout, stderr = client.exec_command('arp -a')
    output = stdout.read().decode()
    client.close()

    online = {}
    for line in output.split('\n'):
        ip = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', line)
        mac = re.search(r'at ([0-9a-f:]{17})', line)
        if ip and mac and ip.group(1).startswith('192.168.1.') and ip.group(1) != '192.168.1.1':
            i = ip.group(1)
            online[i] = mac.group(1)

    active = sorted([{'ip': ip, 'mac': mac, 'hostname': HOSTNAME_MAP.get(ip, 'unknown')}
                     for ip, mac in online.items()], key=lambda x: x['ip'])
    offline = sorted([{'ip': ip, 'hostname': name}
                      for ip, name in HOSTNAME_MAP.items() if ip not in online],
                     key=lambda x: x['ip'])
    return active, offline

@app.route('/')
def index():
    active, offline = get_devices()

    active_rows = ''
    for d in active:
        active_rows += f"<tr><td class='hostname'>{d['hostname']}</td><td class='ip'>{d['ip']}</td><td class='mac'>{d['mac']}</td></tr>"

    offline_rows = ''
    for d in offline:
        offline_rows += f"<tr><td class='hostname'>{d['hostname']}</td><td class='ip'>{d['ip']}</td><td class='mac'>—</td></tr>"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta http-equiv="refresh" content="30"/>
  <title>CYPRESS / TRACE</title>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
    body{{font-family:"Courier New",monospace;background:#f7f7f5;color:#1a1a1a;padding:48px 32px;}}
    header{{margin-bottom:40px;border-bottom:1px solid #d4d4d0;padding-bottom:20px;}}
    header h1{{font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;}}
    header p{{font-size:11px;color:#888;margin-top:6px;}}
    .stats{{display:flex;gap:32px;margin-bottom:40px;}}
    .stat{{display:flex;flex-direction:column;gap:2px;}}
    .stat .num{{font-size:22px;font-weight:700;}}
    .stat .label{{font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#999;}}
    h2{{font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#888;margin-bottom:12px;}}
    table{{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:48px;}}
    thead tr{{border-bottom:1px solid #1a1a1a;}}
    thead th{{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;padding:0 0 10px 0;color:#888;font-weight:600;}}
    tbody tr{{border-bottom:1px solid #e8e8e5;}}
    tbody tr:last-child{{border-bottom:none;}}
    tbody td{{padding:12px 0;}}
    .hostname{{font-weight:600;}}
    .ip,.mac{{color:#555;}}
    .offline .hostname,.offline .ip,.offline .mac{{color:#999;font-weight:400;}}
    footer{{margin-top:8px;font-size:10px;color:#bbb;}}
  </style>
</head>
<body>
  <header>
    <h1>CYPRESS / TRACE Lab — Network Devices</h1>
    <p>Auto-refreshes every 30 seconds · UMBC ITE 457</p>
  </header>
  <div class="stats">
    <div class="stat"><span class="num">{len(active)}</span><span class="label">Online</span></div>
    <div class="stat"><span class="num">{len(offline)}</span><span class="label">Offline</span></div>
  </div>
  <h2>Online</h2>
  <table>
    <thead><tr><th>Hostname</th><th>IP Address</th><th>MAC Address</th></tr></thead>
    <tbody>{active_rows}</tbody>
  </table>
  <h2>Offline</h2>
  <table>
    <thead><tr><th>Hostname</th><th>IP Address</th><th>MAC Address</th></tr></thead>
    <tbody class="offline">{offline_rows}</tbody>
  </table>
  <footer>CYPRESS TRACE VPN Portal · pfSense 192.168.1.1</footer>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
