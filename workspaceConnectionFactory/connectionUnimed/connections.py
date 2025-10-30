import os
from reportUnimed import global_logger
logger = global_logger()
from sqlalchemy import create_engine
import sqlalchemy
from minio import Minio
from minio.error import S3Error
import trino


def get_env(var_name, default=None):
    value = os.environ.get(var_name, default)
    if value is None:
        logger.warning(f"Environment variable {var_name} not set!")
    return value

def conectSQLServer(server_name=None, db_name=None, username=None, password=None):
    """Conexão com SQL Server DW Unimed"""
    try:
        vServerName = server_name#get_env("SQLSERVER_HOST_DW")
        vDBName     = db_name#get_env("SQLSERVER_DATABASE_DW")
        vUserName   = username#get_env("SQLSERVER_USER_DW")
        vPassword   = password #get_env("SQLSERVER_PASSWORD_DW")
        vPort = '1433'
        
        vUrl = f'mssql+pymssql://{vUserName}:{vPassword}@{vServerName}:{vPort}/{vDBName}'
        engine = create_engine(vUrl)
        logger.warning(f"📡 Connected to {vDBName}...")

        return engine

    except Exception as e:
        logger.error(f'{e} - ERROR CONEXAO DWUNIMED')
        raise e

def connectionOracle(server_name=None, db_name=None, username=None, password=None):
    """Conexão com Oracle DYAD"""
    try:
        vHost = server_name#get_env("ORACLE_DYAD_HOST")
        vBase = db_name#get_env("ORACLE_DYAD_DATABASE")
        vUser = username#get_env("ORACLE_DYAD_USER") 
        vPassword = password#get_env("ORACLE_DYAD_PASSWORD")  

        vURL = f'oracle+cx_oracle://{vUser}:{vPassword}@{vHost}/?service_name={vBase}'
        engine = sqlalchemy.create_engine(vURL, arraysize=1000)

        logger.warning(f"📡 Connected to {vBase}...")
        return engine

    except Exception as e:
        logger.error(f'{e} - ERROR CONEXAO ORACLEDYAD')
        raise e

def connectionMySQL(server_name=None, db_name=None, username=None, password=None):
    try:
        vServerName     = server_name#os.environ.get("MYSQL_ZABBIX_HOST")
        vDBName         = db_name#os.environ.get("MYSQL_ZABBIX_DATABASE")
        vUserName       = username#os.environ.get("MYSQL_ZABBIX_USER")
        vPassword       = password#os.environ.get("MYSQL_ZABBIX_PASSWORD")
        vPort           = '3306'#os.environ.get("MYSQL_ZABBIX_PORT")
    
        from sqlalchemy import create_engine
        vUrl = f"mysql+pymysql://{vUserName}:{vPassword}@{vServerName}:{vPort}/{vDBName}"
        engine = create_engine(vUrl)
        logger.warning(f"📡 Connected to {vDBName}...")
    
        return engine
    

    except Exception as e:
        logger.error(f'{e} - ERROR CONEXAO MySQL')

def connectionTrino(server_name=None, username=None):
    try:

        vHost = server_name #get_env("TRINO_HOST")
        vPort = '8080'
        vUser = username#get_env("TRINO_USER")  
        
        conn = trino.dbapi.connect(
            host=vHost,
            port=vPort,
            user=vUser,
            http_scheme="http"
        )
        logger.info("📡 Connected to Trino...")
        return conn
    except Exception as e:
        logger.error(f"❌ Erro na conexão com DLAKE: {e}")
        raise

def connectionMinio(server_name=None, username=None, password=None):
    """Estabelece conexão com o MinIO usando credenciais do arquivo .env."""
    # Carrega as variáveis do arquivo .env
    # Obtém as credenciais do .env
    MINIO_SECURE = "False"
    minio_endpoint = server_name#os.getenv("MINIO_ENDPOINT")
    minio_access_key = username#os.getenv("MINIO_USER")
    minio_secret_key = password#os.getenv("MINIO_PASSWORD")
    minio_secure =  (MINIO_SECURE or "False").lower() == "true"

    # Valida se as credenciais foram carregadas
    if not all([minio_endpoint, minio_access_key, minio_secret_key]):
        raise ValueError("Erro: Credenciais do MinIO não encontradas no arquivo .env")

    # Cria o cliente MinIO
    try:
        client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=minio_secure
        )
        logger.warning(f"📡 Connected to Minio...")
        return client
    except Exception as e:
        logger.error(f"Erro ao conectar ao MinIO: {e}")
        raise  

def upload_files_to_minio(source_dir, bucket_name, minio_client):
    """Envia arquivos .csv de um diretório local para um bucket no MinIO."""
    vStart=4
    try:
        # Verificando se o bucket existe
        if not minio_client.bucket_exists(bucket_name):
            logger.info(f"📂 Bucket {bucket_name} não encontrado!")
            return
        else:
            logger.info(f"📂 Bucket {bucket_name} já existe.")

        # Iterando sobre todos os arquivos na pasta source_dir
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                vArq = file.replace('.csv','')
                # Filtrando apenas arquivos .csv
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    file_path = file_path.lower()
                    # Definindo o caminho dentro do bucket
                    #object_name = f"{vArq}/{file}"  # Prefixo "landzone"
                    object_name = f"{vArq.upper()}/{file.lower()}"
                    logger.info(f"☁️ Enviando Arquivos para {object_name}...")

                    # Enviar o arquivo para o MinIO
                    minio_client.fput_object(bucket_name, object_name, file_path)
                    logger.info(f"✅ {file} enviado com sucesso!")
                else:
                    logger.info(f"Ignorando {file}: não é um arquivo .csv")
        return vStart
    except S3Error as e:
        logger.error(f"Erro ao acessar o S3Error: {e}")
        vStart=0
    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        vStart=0