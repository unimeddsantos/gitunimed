import os
import streamlit as st
import pandas as pd
import yaml
from datetime import datetime, date, timedelta
from collections import deque
from streamlit_autorefresh import st_autorefresh

# ---------------------------
# ⚙️ Configurações da Página
# ---------------------------
st.set_page_config(page_title="Monitor de Processos - Unimed", layout="wide")

# Adiciona o autorefresh para atualizar a cada 10 minutos (600000 ms)
st_autorefresh(interval=600000, key="monitor_unimed")

# 🌙 Estilo visual refinado (modo escuro e cards coloridos)
st.markdown("""
    <style>
    body { background-color: #0e1117; color: #fafafa; }
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { font-size: 3rem; font-weight: bold; }
    .success { background: linear-gradient(90deg, #007b55, #00c16a); padding: 1.2rem; border-radius: 12px; color: white; text-align: center; font-weight: bold; }
    .warning { background: linear-gradient(90deg, #b8860b, #ffca28); padding: 1.2rem; border-radius: 12px; color: black; text-align: center; font-weight: bold; }
    .error { background: linear-gradient(90deg, #9b1b30, #ff5252); padding: 1.2rem; border-radius: 12px; color: white; text-align: center; font-weight: bold; }
    .info { background: linear-gradient(90deg, #0d47a1, #42a5f5); padding: 1.2rem; border-radius: 12px; color: white; text-align: center; font-weight: bold; }
    .kpi-box { padding: 10px 18px; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 🔧 Configurações locais
# ---------------------------
root_dir = r'D:\projectPython\schedulersPython'
config_path = r"D:\projectPython\schedulersPython\workspaceUnimedProcess\config.yml"

if not os.path.exists(config_path):
    st.error(f"Config file not found at {config_path}")
    st.stop()

with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# normalize projects_to_check: support both formats
raw_projects = config.get("projects", [])
projects_to_check = []
projects_schedule_map = {}  # name -> schedule (if provided)

for p in raw_projects:
    if isinstance(p, dict):
        name = p.get("name") or p.get("project") or p.get("project_name")
        if name:
            projects_to_check.append(name)
            if "schedule" in p:
                projects_schedule_map[name] = p["schedule"]
    elif isinstance(p, str):
        projects_to_check.append(p)
    else:
        continue

if not projects_to_check:
    st.error("Nenhum projeto encontrado em config.yml (chave 'projects').")
    st.stop()

# ---------------------------
# 🧰 Funções utilitárias
# ---------------------------
def get_last_lines(file_path, n=50):
    """Retorna as últimas n linhas do arquivo (string)."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return ''.join(deque(f, n))
    except Exception:
        return ""

def find_latest_log(project_path):
    """Procura recursivamente por arquivos .log e retorna (latest_log_path, latest_mtime) ou (None, None)."""
    log_paths = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.lower().endswith('.log'):
                log_paths.append(os.path.join(root, file))
    if not log_paths:
        return None, None
    mod_times = [os.path.getmtime(p) for p in log_paths]
    latest_index = int(mod_times.index(max(mod_times)))
    return log_paths[latest_index], mod_times[latest_index]

def classify_status_from_log_text(last_text, latest_date, today_date):
    """Classifica status a partir do texto das últimas linhas já em lowercase."""
    if not last_text:
        return None
    if 'error' in last_text or 'erro' in last_text:
        return "Erro"
    success_phrases = [
        'não há arquivos em', 'processo finalizado', 'sem arquivos',
        'nenhum arquivo', 'processo concluído', 'tarefa finalizada',
        'success', 'sucesso'
    ]
    if any(p in last_text for p in success_phrases):
        return "Executado com Sucesso"
    return "Executado com Sucesso"

# ---------------------------
# 🔎 Varre cada projeto e monta lista de statuses
# ---------------------------
today_date = date.today()
yesterday_date = today_date - timedelta(days=1)

statuses = []

for project in projects_to_check:
    project_path = os.path.join(root_dir, project)
    if not os.path.isdir(project_path):
        statuses.append({
            "Project": project,
            "Status": "Directory not found",
            "Log File": "",
            "Agendamento": projects_schedule_map.get(project, "não informado"),
            "Última Execução": "-"
        })
        continue

    latest_log, latest_mtime = find_latest_log(project_path)

    if not latest_log:
        # Redireciona "No logs found" para "Sem Atualização"
        days_without = (today_date - date(1970, 1, 1)).days
        statuses.append({
            "Project": project,
            "Status": f"Sem Atualização ({days_without} dias)",
            "Log File": "",
            "Agendamento": projects_schedule_map.get(project, "não informado"),
            "Última Execução": "-"
        })
        continue

    latest_date = datetime.fromtimestamp(latest_mtime).date()
    last_text = get_last_lines(latest_log, n=50).lower()

    if latest_date in (today_date, yesterday_date):
        status = classify_status_from_log_text(last_text, latest_date, today_date)
        if status is None:
            status = "Executado com Sucesso"
    else:
        days_without = (today_date - latest_date).days
        status = f"Sem Atualização ({days_without} dias)"

    last_exec_str = datetime.fromtimestamp(latest_mtime).strftime("%d/%m/%Y %H:%M")
    statuses.append({
        "Project": project,
        "Status": status,
        "Log File": latest_log,
        "Agendamento": projects_schedule_map.get(project, "não informado"),
        "Última Execução": last_exec_str
    })

# ---------------------------
# 📊 DataFrame final
# ---------------------------
df = pd.DataFrame(statuses)

# ---------------------------
# 🎯 KPIs
# ---------------------------
total_processos = len(df)
executado_sucesso = (df["Status"] == "Executado com Sucesso").sum()
sem_atualizacao = df["Status"].str.contains("Sem Atualização", case=False, na=False).sum()
erros = (df["Status"] == "Erro").sum()

# Verificar se a soma bate com o total
total_status = executado_sucesso + sem_atualizacao + erros
if total_status != total_processos:
    st.warning(f"Discrepância na contagem: Total esperado ({total_processos}) não bate com a soma dos status ({total_status}). Verifique os logs ou a classificação dos projetos.")

# ---------------------------
# 🎯 Cabeçalho com data e hora de atualização
# ---------------------------
update_time = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"## 📈 Monitor de Processos - Unimed (Atualizado em {update_time})")

# ---------------------------
# 🎯 Filtros laterais
# ---------------------------
st.sidebar.header("🔍 Filtros")
# Filtro por projeto
projects = ["Todos"] + sorted(df["Project"].unique().tolist())
selected_project = st.sidebar.selectbox("Filtrar por Projeto", projects)
# Filtro por status (removido "Sem Dados")
status_options = ["Todos", "Executado com Sucesso", "Sem Atualização", "Erro"]
selected_status = st.sidebar.selectbox("Filtrar por Status", status_options)

# ---------------------------
# 📊 Aplica filtros
# ---------------------------
df_filtered = df.copy()
if selected_project != "Todos":
    df_filtered = df_filtered[df_filtered["Project"] == selected_project]
if selected_status != "Todos":
    df_filtered = df_filtered[df_filtered["Status"].str.contains(selected_status, case=False, na=False)]

# ---------------------------
# 🎯 KPIs display
# ---------------------------
col1, col2, col3, col4 = st.columns(4)  # Ajustado para 4 colunas
with col1:
    st.markdown(f"<div class='info'>📦 Total<br><span style='font-size: 2.8rem;'>{total_processos}</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='success'>✅ Executado com Sucesso<br><span style='font-size: 2.8rem;'>{executado_sucesso}</span></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='warning'>⚠️ Sem Atualização<br><span style='font-size: 2.8rem;'>{sem_atualizacao}</span></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='error'>❌ Erros<br><span style='font-size: 2.8rem;'>{erros}</span></div>", unsafe_allow_html=True)

st.write("")  # Espaço em branco
st.write("")  # Espaço em branco
# ---------------------------
# 📊 Tabela resumida
# ---------------------------
st.dataframe(df_filtered, width="stretch")

# ---------------------------
# 📋 Detalhes do Projeto Selecionado
# ---------------------------
st.markdown("### 🗂️ Detalhes do Projeto Selecionado")

if not df_filtered.empty:
    detalhes_projects = df_filtered["Project"].unique().tolist()
    selected_detail_project = st.selectbox("Selecione o projeto para ver detalhes:", detalhes_projects)

    row = df_filtered[df_filtered["Project"] == selected_detail_project].iloc[0]

    project = row["Project"]
    status = row["Status"]
    log_file = row["Log File"]
    agendamento = row["Agendamento"]
    ultima = row["Última Execução"]

    with st.expander(f"📁 {project} — {status}"):
        st.markdown(f"**🕒 Agendamento:** {agendamento}")
        st.markdown(f"**📆 Última Execução:** {ultima}")
        st.markdown(f"**📄 Log File:** `{log_file}`")

        if log_file and os.path.exists(log_file):
            st.markdown("**Últimas 50 linhas:**")
            st.code(get_last_lines(log_file, n=50), language="bash")
            if st.button(f"Mostrar log completo — {project}", key=f"full_{project}_detail"):
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    st.text_area("📜 Log completo", f.read(), height=400)
        else:
            st.warning("⚠️ Arquivo de log não encontrado.")
else:
    st.info("Nenhum projeto disponível para exibir detalhes.")