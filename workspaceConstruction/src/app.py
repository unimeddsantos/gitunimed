import os
import subprocess
import sys
import pyfiglet

vLimiteText = 500
vEspaco = 5

def generate_ascii_art_with_border(text):
    # Gerar o texto em ASCII
    ascii_art = pyfiglet.figlet_format(text, width=vLimiteText).rstrip()  # Remove espaços e quebras extras no final
 
    # Quebrar em linhas
    lines = ascii_art.split("\n")
 
    # Encontrar o comprimento máximo da linha
    max_length = max(len(line) for line in lines)
 
    # Adicionar espaços à esquerda e à direita
    padding = vEspaco
    total_length = max_length + (padding * 2)
 
    # Criar a borda superior e inferior
    border = "#" * (total_length + 4)
 
    # Criar a linha extra antes da borda inferior
    extra_line = f"# {' ' * (total_length)} #"
 
    # Criar o texto com bordas laterais e espaços
    framed_text = [f'echo "{border}"']  # Começa com a borda superior
    for line in lines:
        framed_text.append(f'echo "# {" " * padding}{line.ljust(max_length)}{" " * padding} #"')  # Adiciona cada linha do ASCII com bordas laterais
   
    framed_text.append(f'echo "{extra_line}"')  # Adiciona a linha em branco antes da borda inferior
    framed_text.append(f'echo "{border}"')  # Adiciona a borda inferior
 
    return framed_text

def criar_workspace(nome_workspace, base_dir=r"D:\projectPython\schedulersPython", criar_venv=True, criar_requirements=True, cria_md=True, criar_bat=True):
    # Nome da pasta principal (sempre com 'workspace' na frente)
    pasta_principal = os.path.join(base_dir, f"workspace{nome_workspace}")
    
    # Estrutura de subpastas
    subpastas = ["database", "logs", "src", "tests"]

    md_content = """
            
        # PARA CRIAR AMBIENTE VISTUAL CORRETO 

        ## INICIANDO O PROJETO DEVE ATIVAR O AMBIENTE E DEPOIS INSTALAR O REQUIREMENTS.TXT

        
    # APOS CRIAÇÃO DO AMBIENTE VISTUAL ATIVA-LO
    ```bash
    . venv/Scripts/activate
    ```
            
    # DEPOIS DE ATIVAR DEVE INSTALAR O REQUIREMENTS.TXT
    ```bash
    pip install -r requirements.txt
    ```

    ## powerShell
    ```bash
    & "C:\Program Files\Python310\python.exe" -m venv venv
    ```
    ## ou no cmd
    ```bash
    "C:\Program Files\Python310\python.exe" -m venv venv
    ```

       
        """
    
    # Conteúdo do requirements.txt
    requirements_content = """argon2-cffi==25.1.0
argon2-cffi-bindings==25.1.0
certifi==2025.8.3
cffi==1.17.1
greenlet==3.2.4
duckdb>=0.9.0
trino>=0.323.0
PyYAML>=6.0
minio==7.2.16
mysql-connector-python==9.4.0
holidays>=0.28  # versão mínima
numpy==1.26.4
pandas==2.1.4
pycparser==2.22
pycryptodome==3.23.0
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
#pymysql>=1.1.0
pymssql==2.2.7
PyMySQL==1.1.1
pyodbc==5.2.0
oracledb>=1.4.1
cx_Oracle==8.3.0
pyproject_hooks==1.2.0
boto3==1.40.12
botocore==1.40.12
pytz==2025.2
fsspec>=2025.1
six==1.17.0
SQLAlchemy==2.0.43
sqlalchemy-pytds==0.3.1
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
pyarrow>=14.0.0
fastparquet>=2023.10.1
pyfiglet==1.0.2
D:/projectPython/schedulersPython/loggerUnimed/dist/loggerunimed-0.1.2-py3-none-any.whl
D:/projectPython/schedulersPython/workspaceConnectionFactoryUnimed/dist/connectionUnimeddb-0.1.7-py3-none-any.whl
"""
    
    # Verifica se já existe
    if os.path.exists(pasta_principal):
        print(f"⚠️ O projeto '{pasta_principal}' já existe. Encerrando.")
        sys.exit(1)
    
    try:
        # Criar pasta principal
        os.makedirs(pasta_principal)
        
        # Criar subpastas
        for subpasta in subpastas:
            os.makedirs(os.path.join(pasta_principal, subpasta))
        
        print(f"✅ Workspace criado em: {pasta_principal}")
        
        # Criar requirements.txt
        if criar_requirements:
            req_file = os.path.join(pasta_principal, "requirements.txt")
            with open(req_file, "w", encoding="utf-8") as f:
                f.write(requirements_content.strip() + "\n")
            print(f"✅ requirements.txt criado em: {req_file}")

        # Criar .md
        if cria_md:
            req_file = os.path.join(pasta_principal, "ENV_SETUP_GUIDE.md")
            with open(req_file, "w", encoding="utf-8") as f:
                f.write(md_content.strip() + "\n")
            print(f"✅ ENV_SETUP_GUIDE.md criado em: {req_file}")
            
        # Criar .bat
        if criar_bat:
            bat_file = os.path.join(pasta_principal, f"run_{nome_workspace}.bat")
            ascii_art_lines = generate_ascii_art_with_border(nome_workspace)
            bat_content = ["@echo off"] + ascii_art_lines + [
                f'REM Seleciona o Projeto a ser Executado',
                f'cd /d {pasta_principal}',
                f'if not exist venv (',
                f'    echo Criando ambiente virtual... ',
                f'    "C:\Program Files\Python310\python.exe" -m venv venv',
                f')',
                f'REM **************************************************',
                f'REM Ativa o ambiente virtual e executa o .py',
                f'call venv\\Scripts\\activate.bat',
                f'REM pip install D:\\projectPython\\schedulersPython\\loggerUnimed\\dist\\loggerunimed-0.1.1-py3-none-any.whl --force-reinstall',
                f'REM pip install -r requirements.txt',
                f'REM pip install requests',
                f'REM pip install --upgrade pip',
                f'REM pip install --force-reinstall python-dotenv',
                f'python src\\app.py',
                f'echo "processo Finalizado..."',
                f'REM *************************************************',
                f'REM Desativa o ambiente virtual',
                f'deactivate',
                f'REM *************************************************'
            ]
            with open(bat_file, "w", encoding="utf-8") as f:
                f.write("\n".join(bat_content) + "\n")
            print(f"✅ run_{nome_workspace}.bat criado em: {bat_file}")
        
        # Criar app.py na pasta src
        app_py_content = '''import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pyarrow.parquet as pq
import pyarrow as pa
import os
import sys
import time
import math
import threading
from itertools import cycle
from pathlib import Path
from connectionUnimed import connections
from sqlalchemy import types, create_engine, text
import sqlalchemy
from pathlib import Path
from reportUnimed import global_logger
logger = global_logger()
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings('ignore')

"""
    ||#################################################################################
    ||Autor       : autor                                                            ||
    ||Empresa     : UNIMED                                                           ||
    ||Versao      : v1                                                               ||
    ||Data        : yyyy-mm-dd                                                       ||
    ||Projeto     :                                                                  ||
    ||                                                                               ||
    ||Tipo       : Evolutiva                     Evolutiva/Corretiva/Paleativa       ||
    ||------------------------------------------------------------------------------ ||
    ||*****************************   Connections    ********************************||
    ||SQLSERVER - connections.conectSQLServer(vServer,vDBName,vUserName,vPassword)   ||
    ||ORACLE    - connections.connectionOracle(vServer,vDBName,vUserName,vPassword)  ||
    ||MYSQL     - connections.connectionMySQL(vServer,vDBName,vUserName,vPassword)   ||
    ||TRINO     - connections.connectionTrino(vServer,vUserName)                     ||
    ||MINIO     - connections.connectionMinio(vServer,vUserName,vPassword)           ||
    ||MINIOUPLOAD - connections.upload_files_to_minio(dir, bucketname, minio)        ||
    ||------------------------------------------------------------------------------ ||
    ||*****************************  Exemplo Conexão    *****************************||
    ||vServ         = get_env("ORACLE_DYAD_HOST")                                    ||
    ||vBD           = get_env("ORACLE_DYAD_DATABASE")                                ||   
    ||vUser         = get_env("ORACLE_DYAD_USER")                                    || 
    ||vPass         = get_env("ORACLE_DYAD_PASSWORD")                                ||
    ||# Criar engine do Oracle DYAD                                                  ||
    ||engine_oracle = connections.connectionOracle(vServ,vBD,vUser,vPass)            ||
    ################################################################################### 
    ||***********************************    ****************************************||
    ||  ALTERACOES :                                                                 ||
    ||    DATA        VERSAO      RESPONSAVEL        TIPO     MOTIVO                 ||                           
    ||  ----------    ------     -----------------   ----     -----------------------||
    ||  dd/mm/yyyy     v2        *************                                       ||
    ||*******************************************************************************||
"""

# Caminho do arquivo .env (ajuste se não estiver no mesmo diretório)
load_dotenv('.env', override=True)
# 🔹 CONFIGURAÇÕES RETORNO HH24:MI:SS
def segundos_para_hms(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return f"Horas {int(horas):02d}: Minutos {int(minutos):02d}: Segundos {segundos:.2f}"

# 🔹 CONFIGURAÇÕES CURSOR ANIMADO
def loading_animation(stop_event):
    spinner = cycle(["/", "-", "\", "|"])  # Caracteres para a animação
    while not stop_event.is_set():
        sys.stdout.write(f'\\rCarregando {next(spinner)}')  # Escreve o caractere rotativo
        sys.stdout.flush()  # Força a atualização do console
        time.sleep(0.1)  # Controla a velocidade da animação
    sys.stdout.write('\\r')  # Limpa a linha ao parar
    sys.stdout.flush()

# 🔹 CONFIGURAÇÕES GET .ENV
def get_env(var_name):
    load_dotenv(override=True)
    value = os.environ.get(var_name)
    if value is None:
        logger.error(f"❌ Variável de ambiente {var_name} não encontrada")
        raise ValueError(f"Variável de ambiente {var_name} não encontrada")
    return value

def main():
    # Iniciar a animação em uma thread separada
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    animation_thread.start()
    tempo_total = 0
    inicio = time.time()
    try:
        logger.warning(f"======================= >> PIPELINE PROCESS #1 << ==========================")

        logger.warning(f"======================= >> FINALIZANDO PROCESS  << ==========================")
        fim = time.time()
        vRetTemp = fim - inicio
        tempo_formatado = segundos_para_hms(vRetTemp)
        logger.info(f"       >> O Processo:  levou {tempo_formatado}  para executar...") 
        logger.info(f"       >> ************************************************************") 

    except Exception as e:
        logger.error(f"{e} - ERROR FUNCTION PROCESSING")
        return 0 
    finally:
        # Parar a animação quando o programa terminar
        stop_event.set()
        animation_thread.join()  # Aguarda a thread da animação terminar
        logger.info(f"✅ Processo finalizado ...")    

if __name__ == "__main__":
    inicio = time.time()
    vInicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.warning(f" >> START PIPELINE <-> {vInicio} ...")
    """**************************************************************"""
    main()
    logger.warning(f" >> FINALIZANDO PIPELINE ...")
    fim = time.time()
    vRest = fim - inicio
    tempo_formatado = segundos_para_hms(vRest)
    vFim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.warning(f" >> FINALIZANDO PIPELINE <-> {vFim}...")

'''
        app_py_file = os.path.join(pasta_principal, "src", "app.py")
        with open(app_py_file, "w", encoding="utf-8") as f:
            f.write(app_py_content)
        print(f"✅ app.py criado em: {app_py_file}")
        
        # Criar venv dentro do workspace
        if criar_venv:
            venv_path = os.path.join(pasta_principal, "venv")
            print("⏳ Criando ambiente virtual (venv)...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print(f"✅ Ambiente virtual criado em: {venv_path}")
    
    except Exception as e:
        print(f"❌ Erro ao criar workspace: {e}")
        sys.exit(1)

if __name__ == "__main__":
    nome_projeto = input("Digite o nome do projeto para criar o workspace: ").strip()
    if nome_projeto:
        criar_workspace(nome_projeto)
    else:
        print("❌ Nome do projeto não pode ser vazio.")
        sys.exit(1)