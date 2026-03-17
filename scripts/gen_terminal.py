import urllib.request
import json
import datetime

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req).read())

stats = fetch("https://api.github.com/users/plur1bu5")
repos = fetch("https://api.github.com/users/plur1bu5/repos?per_page=100")

stars = sum(r["stargazers_count"] for r in repos)
repo_count = stats["public_repos"]
followers = stats["followers"]
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

lines = [
    ("$", "whoami"),
    ("", "plur1bu5 — red teamer · pentester · researcher"),
    ("", ""),
    ("$", "nmap -sV --open plur1bu5.dev"),
    ("", "PORT     STATE  SERVICE"),
    ("", "443/tcp  open   https → blog active"),
    ("", ""),
    ("$", f"enum4linux -a github.com/plur1bu5"),
    ("", f"[+] public_repos  : {repo_count}"),
    ("", f"[+] total_stars   : {stars}"),
    ("", f"[+] followers     : {followers}"),
    ("", ""),
    ("$", "cat /etc/targets"),
    ("", "AD · web · cloud · k8s · CI/CD"),
    ("", ""),
    ("$", f"date"),
    ("", now),
    ("", ""),
    ("$", "▌"),
]

line_height = 22
padding = 20
width = 620
height = padding * 2 + len(lines) * line_height

svg_lines = []
svg_lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" rx="8" fill="#0d0d0d"/>
  <rect x="0" y="0" width="{width}" height="28" rx="8" fill="#1a1a1a"/>
  <circle cx="16" cy="14" r="5" fill="#ff5f57"/>
  <circle cx="32" cy="14" r="5" fill="#febc2e"/>
  <circle cx="48" cy="14" r="5" fill="#28c840"/>
  <text x="{width//2}" y="18" font-family="monospace" font-size="11" fill="#666" text-anchor="middle">plur1bu5 — bash</text>
  <style>
    .prompt {{ fill: #39FF14; }}
    .text {{ fill: #e0e0e0; }}
    .cursor {{ fill: #39FF14; }}
  </style>''')

y = 28 + padding
for prompt, text in lines:
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if prompt == "$":
        svg_lines.append(
            f'  <text x="{padding}" y="{y}" font-family="Fira Code,monospace" font-size="13">'
            f'<tspan class="prompt">$ </tspan><tspan class="text">{escaped}</tspan></text>'
        )
    elif text == "▌":
        svg_lines.append(
            f'  <text x="{padding}" y="{y}" font-family="Fira Code,monospace" font-size="13" class="cursor">{escaped}</text>'
        )
    else:
        svg_lines.append(
            f'  <text x="{padding + 16}" y="{y}" font-family="Fira Code,monospace" font-size="13" class="text">{escaped}</text>'
        )
    y += line_height

svg_lines.append("</svg>")

with open("dist/terminal.svg", "w") as f:
    f.write("\n".join(svg_lines))

print("terminal.svg generated")
