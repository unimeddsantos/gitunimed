import logging
import os
from datetime import datetime

# Configuração dos níveis personalizados
logging.START = logging.INFO + 5
logging.END = logging.INFO + 6
logging.addLevelName(logging.START, "START")
logging.addLevelName(logging.END, "END")

# Definindo um nível customizado
NOTIFICATION_LEVEL = 25  # entre INFO(20) e WARNING(30)
logging.NOTIFICATION = NOTIFICATION_LEVEL
logging.addLevelName(logging.NOTIFICATION, "NOTIFICATION")

# Função helper para logger
def notification(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.NOTIFICATION):
        self._log(logging.NOTIFICATION, message, args, **kwargs)

logging.Logger.notification = notification

class ColorLogger:
    # Paleta de cores (códigos ANSI)
    COLOR_PALETTE = {
        'DEBUG': '\033[38;5;185m',     # #e9e784 (amarelo claro)
        'START': '\033[38;5;48m',      # #008a5f (verde escuro)
        'INFO': '\033[38;5;158m',       # #62ab66 (verde)
        'WARNING': '\033[38;5;230m',   # #a5ca71 (verde claro)
        'ERROR': '\033[38;5;217m',     # #cc5133 (vermelho)
        'CRITICAL': '\033[38;5;196m',  # Vermelho intenso
        'END': '\033[38;5;48m',        # Igual ao START
        'RESET': '\033[0m'            # Reset de cor
    }

    @staticmethod
    def setup_logger(log_dir="logs", name='reports_alert'):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        class ColorLineFormatter(logging.Formatter):
            # Emojis por nível
            level_emojis = {
                logging.DEBUG: "🐞 ",
                logging.INFO: "ℹ️ ",
                logging.WARNING: "⚠️ ",
                logging.ERROR: "❌ ",
                logging.CRITICAL: "🔥 ",
                logging.START: "🚀 ",
                logging.END: "✅ "
            }
            
            # Emojis por conteúdo
            content_emojis = {
                "arquivos encontrados": "🔍 ",
                "Lendo arquivo": "📖 ",
                "registros encontrados": "📊 ",
                "Resumo": "📊 ",
                "IDATE": "📅 ",
                "IKEY": "🎯 ",
                "conectado": "🟢 ",
                "Desconectado": "🔴 ",
                "conexão perdida": "🔴 ",
                "connection lost": "🔴 ",
                "DROP TABLE": "💥 ",
                "DROP ": "🗑️ ",
                "TRUNCATE TABLE": "✂️ ",
                "TRUNCATE ": "🧽 ",
                "dropando": "💥 ",
                "Executando": "▶ ",
                "drop ": "🗑️ ",
                "truncate ": "✂️ ",
                "CREATE TABLE": "🏗️ ",
                "create table": "🏗️ ",
                "criando tabela": "📋 ",
                "nova tabela": "🆕 ",
                "ALTER TABLE": "🔧 ",
                "alter table": "🔧 ",
                "Atualizacao": "🔄 ",
                "Executando": "🔄 ",
                "Processamento em Andamento": "⏳ ",
                "Salvando": "📤 ",
                "Limpeza": "🧹 ",
                "Compilando": "👨‍💻 ",
                "Localizando": "🔍 ",
                "Configurando": "⚙️ ",
                "Analise": "📈 ",
                "Calculos": "🧮 ",
                "Executando": "▶ ",
                "Server": "🖥️ ",
                "Stop": "🛑 ",
                "Conexao": "📡 ",
                "Alertas": "🚨 ",
                "Verificando": "✔️ ",
                "Pasta": "🗂️ ",
                "Pastas": "📂",
                "Objetivo": "🎯 ",
                "Spark": "🔥 ",
                "Automacao": "🤖 ",
                "Corte": "✂️ ",
                "Encerrado": "✔️ ",
                "Finalizado": "✅ ",
                "Escrevendo": "✍️ ",
                "Registro": "📦 ",
                "Limpando": "🧹 ",
                "Conexao": "📡 ",
                "Inteligencia": "🧠 ",
                "Insights": "💡 ",
                "Database": "🛢️ ",
                "Cloud": "☁️ ",
                "Code": "💻 ",
                "Web": "🌐 ",
                "Encerrado com sucesso": "✔️ ",
                "Finalizado": "🏁 ",
                "Processamento encerrado": "🔚 "
            }
            
            def format(self, record):
                # Determina o emoji apropriado
                emoji = ""
                
                # DEBUG/START/END sempre usam seus emojis próprios
                if record.levelno in [logging.DEBUG, logging.START, logging.END]:
                    emoji = self.level_emojis.get(record.levelno, "")
                else:
                    # Para outros níveis, verifica o conteúdo primeiro
                    msg_lower = record.msg.lower()
                    for pattern, e in self.content_emojis.items():
                        if pattern.lower() in msg_lower:
                            emoji = e
                            break
                    
                    # Se não encontrou no conteúdo, usa o do nível
                    if not emoji:
                        emoji = self.level_emojis.get(record.levelno, "")
                
                # Remove possíveis duplicatas
                if emoji.strip() in record.msg:
                    emoji = ""
                
                # Aplica o emoji
                if emoji:
                    record.msg = f"{emoji}{record.msg.replace(emoji, '').strip()}"
                
                # FORMATO CORRETO: UNIMED-BI - LEVEL - mensagem
                levelname = record.levelname
                base_message = f"UNIMED-BI - {levelname} - {record.msg}"
                
                # Aplica cor a toda a linha
                color = ColorLogger.COLOR_PALETTE.get(record.levelname, '')
                reset = ColorLogger.COLOR_PALETTE['RESET']
                return f"{color}{base_message}{reset}"

        # Formatter para console (com cores)
        console_formatter = ColorLineFormatter()

        # Formatter para arquivo (sem cores e sem timestamp)
        file_formatter = logging.Formatter('UNIMED-BI - %(levelname)s - %(message)s')

        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"health_alerts_{datetime.now().strftime('%Y%m%d')}.log")
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        
        logger.handlers = []
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

    @staticmethod
    def add_custom_methods():
        def start(self, message, *args, **kwargs):
            if self.isEnabledFor(logging.START):
                self._log(logging.START, message, args, **kwargs)
        
        def end(self, message, *args, **kwargs):
            if self.isEnabledFor(logging.END):
                self._log(logging.END, message, args, **kwargs)
        
        logging.Logger.start = start
        logging.Logger.end = end

    @staticmethod
    def set_color(level, color_code):
        """Define uma cor personalizada para um nível de log"""
        ColorLogger.COLOR_PALETTE[level] = color_code

# Configuração inicial
ColorLogger.add_custom_methods()
logger = ColorLogger.setup_logger()

def get_logger(name=None, log_dir="logs"):
    return ColorLogger.setup_logger(log_dir=log_dir, name=name or 'health_alerts')

global_logger = get_logger()
global_logger = lambda: get_logger()