import os
import re

VERSIONS_DIR = "versions"
INDEX_FILE = "index.html"

def categorizar_versao(versao):
    """Classifica a versão detetada no nome do ficheiro em categorias lógicas."""
    v_lower = versao.lower()
    if "alpha" in v_lower or "a" in v_lower:
        return "Alfas"
    elif "beta" in v_lower or "b" in v_lower:
        return "Betas"
    elif "rc" in v_lower or "candidate" in v_lower:
        return "Release Candidates"
    else:
        return "Releases Recentes"

def gerar_index():
    print("[*] A analisar e a classificar as versões na pasta 'versions'...")
    
    if not os.path.exists(VERSIONS_DIR):
        os.makedirs(VERSIONS_DIR)
        
    ficheiros = os.listdir(VERSIONS_DIR)
    
    # Dicionário para separar as versões por categoria
    categorias = {
        "Releases Recentes": [],
        "Release Candidates": [],
        "Betas": [],
        "Alfas": []
    }
    
    for f in ficheiros:
        match = re.match(r"PythonOS_(.+)\.py$", f, re.IGNORECASE)
        if match:
            versao = match.group(1)
            cat = categorizar_versao(versao)
            if versao not in categorias[cat]:
                categorias[cat].append(versao)
                
    # Ordenar as versões dentro de cada categoria (da mais recente para a mais antiga)
    for cat in categorias:
        categorias[cat].sort(reverse=True)
        
    total_versoes = sum(len(v) for v in categorias.values())
    
    # Construção do HTML dinâmico
    secções_html = ""
    
    if total_versoes == 0:
        conteudo_corpo = '<div class="no-packages">Ops, desculpe, não tem nenhum pacote disponível para baixar.</div>'
    else:
        # Ordem de exibição das categorias no site
        ordem_categorias = [
            ("🚀 Releases Recentes", "Releases Recentes"),
            ("🎯 Release Candidates (RC)", "Release Candidates"),
            ("🧪 Versões Beta", "Betas"),
            ("🛠️ Versões Alpha", "Alfas")
        ]
        
        for titulo_secção, chave_cat in ordem_categorias:
            lista_v = categorias[chave_cat]
            if not lista_v:
                continue
                
            cards_cat = ""
            for v in lista_v:
                arq_pythonos = f"PythonOS_{v}.py"
                arq_pygui = f"PyGUI_{v}.py"
                
                # Fallback para o PyGUI caso o exato não exista
                if not os.path.exists(os.path.join(VERSIONS_DIR, arq_pygui)):
                    pyguis_disp = [re.match(r"PyGUI_(.+)\.py$", f).group(1) for f in ficheiros if re.match(r"PyGUI_(.+)\.py$", f, re.IGNORECASE)]
                    if pyguis_disp:
                        pyguis_disp.sort(reverse=True)
                        arq_pygui = f"PyGUI_{pyguis_disp[0]}.py"

                # Os 3 botões por versão solicitados
                cards_cat += f"""
        <div class="version-card" data-version="{v}">
          <div class="version-header">
            <span class="version-title">pythonOS v{v}</span>
            <span class="version-badge">{chave_cat}</span>
          </div>
          <div class="bundle-links">
            <a href="build.py" download class="btn-download btn-build">Baixar build.py</a>
            <a href="versions/{arq_pythonos}" download class="btn-download">Baixar pythonOS ({v})</a>
            <a href="versions/{arq_pygui}" download class="btn-download btn-secondary">Baixar Biblioteca PyGUI</a>
          </div>
        </div>
"""
            secções_html += f"""
      <div class="category-section">
        <h2 class="category-title">{titulo_secção}</h2>
        {cards_cat}
      </div>
"""
        conteudo_corpo = secções_html

    # Template do index.html completo e universal
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PythonOS - Central de Versões</title>
  <style>
    * {{ box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    body {{ background-color: #121214; color: #e1e1e6; margin: 0; padding: 2rem; display: flex; flex-direction: column; align-items: center; }}
    .container {{ max-width: 800px; width: 100%; }}
    h1 {{ color: #00d26a; text-align: center; margin-bottom: 0.5rem; }}
    p.subtitle {{ text-align: center; color: #a8a8b3; margin-bottom: 2rem; }}
    .search-box {{ width: 100%; padding: 0.8rem 1.2rem; font-size: 1rem; border-radius: 8px; border: 1px solid #29292e; background-color: #202024; color: #fff; margin-bottom: 1.5rem; outline: none; }}
    .search-box:focus {{ border-color: #00d26a; }}
    .category-section {{ margin-bottom: 2rem; }}
    .category-title {{ color: #00d26a; font-size: 1.2rem; border-bottom: 1px solid #29292e; padding-bottom: 0.5rem; margin-bottom: 1rem; }}
    .version-card {{ background-color: #202024; border: 1px solid #29292e; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; transition: transform 0.2s; }}
    .version-card:hover {{ transform: translateY(-2px); border-color: #00d26a; }}
    .version-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }}
    .version-title {{ font-size: 1.1rem; font-weight: bold; color: #fff; }}
    .version-badge {{ font-size: 0.75rem; background-color: #29292e; color: #00d26a; padding: 0.3rem 0.8rem; border-radius: 12px; }}
    .bundle-links {{ display: flex; gap: 0.8rem; flex-wrap: wrap; }}
    .btn-download {{ background-color: #00d26a; color: #09090a; text-decoration: none; font-weight: bold; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.9rem; transition: background-color 0.2s; }}
    .btn-download:hover {{ background-color: #00b359; }}
    .btn-build {{ background-color: #3b82f6; color: #fff; }}
    .btn-build:hover {{ background-color: #2563eb; }}
    .btn-secondary {{ background-color: #29292e; color: #e1e1e6; }}
    .btn-secondary:hover {{ background-color: #323238; color: #fff; }}
    .no-packages, .no-results {{ text-align: center; color: #737380; margin-top: 2rem; font-size: 1.1rem; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🐍 PythonOS</h1>
    <p class="subtitle">Central oficial de pacotes, builds e versões</p>
    <input type="text" id="searchInput" class="search-box" placeholder="Pesquisar versão (ex: 1.0.0, beta, rc)..." onkeyup="filtrarVersoes()">
    
    <div id="contentList">
      {conteudo_corpo}
    </div>

    <div class="no-results" id="noResults" style="display: none;">Nenhuma versão encontrada para a sua pesquisa.</div>
  </div>
  <script>
    function filtrarVersoes() {{
      const input = document.getElementById('searchInput').value.toLowerCase();
      const cards = document.querySelectorAll('.version-card');
      const sections = document.querySelectorAll('.category-section');
      const noResults = document.getElementById('noResults');
      let visiveis = 0;

      cards.forEach(card => {{
        const versao = card.getAttribute('data-version');
        if (versao && versao.toLowerCase().includes(input)) {{
          card.style.display = 'block';
          visiveis++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      // Oculta secções que fiquem vazias após o filtro
      sections.forEach(sec => {{
        const visiveisNaSecao = sec.querySelectorAll('.version-card[style*="block"], .version-card:not([style*="none"])').length;
        sec.style.display = visiveisNaSecao > 0 ? 'block' : 'none';
      }});

      noResults.style.display = visiveis === 0 ? 'block' : 'none';
    }}
  </script>
</body>
</html>
"""

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"[SUCESSO] O '{INDEX_FILE}' foi gerado e categorizado com sucesso!")

if __name__ == "__main__":
    gerar_index()