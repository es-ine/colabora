"""
Actualiza las etiquetas <!-- AUTO:ultima-actualizacion --> en README.md
consultando la API pública de GitHub.
"""
import re, os, urllib.request, json, datetime

TOKEN = os.environ.get('GH_TOKEN', '')
ARCHIVO = 'README.md'
PATRON_URL = re.compile(r'https://github\.com/([^/]+/[^/)\s]+)')
PATRON_TAG = re.compile(r'<!--\s*AUTO:ultima-actualizacion\s*-->.*?(?=\||$)', re.DOTALL)

def obtener_ultimo_push(repo_path):
  url = f'https://api.github.com/repos/{repo_path}'
  req = urllib.request.Request(url,
        headers = {'Authorization':f'Bearer {TOKEN}',
                   'Accept':'application/vnd.github+json'})
  with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
  pushed = data.get('pushed_at', '')[:10] # YYYY-MM-DD
  return pushed

with open(ARCHIVO, 'r', encoding = 'utf-8') as f:
  contenido = f.read()

repos = PATRON_URL.findall(contenido)
for repo in repos:
  print('Actualizando repositorio:', repo)
  try:
    fecha = obtener_ultimo_push(repo)
    print('Ultima actualizacion:', fecha)
    contenido = re.sub(
      repo + r'(.*)\*\*\s*Última actualización\*\*:\s*.*<!-- AUTO:ultima-actualizacion -->.*',
      f'{repo}\1**Última actualización**: {fecha} <!-- AUTO:ultima-actualizacion --> ',
      contenido
      )
  except Exception as e:
    print(f'Aviso: no se pudo actualizar {repo}: {e}')
    
with open(ARCHIVO, 'w', encoding='utf-8') as f:
  f.write(contenido)
  
print('Actualización completada:', datetime.date.today())
