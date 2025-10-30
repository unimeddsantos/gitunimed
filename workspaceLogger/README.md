
# 🧠 Logger Avançado para Python

Um logger altamente personalizável com suporte a **emojis**, **cores vibrantes**, **múltiplos handlers** e **gerenciamento automático de arquivos de log**. Ideal para projetos que exigem **logs claros, organizados e visualmente agradáveis**.

---

## 📦 Instalação

1. Copie o código do logger para o arquivo `custom_logger.py` no seu projeto.
2. Importe no seu código Python:

```python
from custom_logger import global_logger
```

---

## 🚀 Primeiros Passos

### Uso Básico

Utilize o logger com métodos intuitivos:

```python
global_logger.start("Iniciando aplicação")
global_logger.info("Configuração carregada com sucesso")
global_logger.warning("Alerta: desempenho abaixo do esperado")
global_logger.error("Erro crítico na conexão com o banco")
global_logger.end("Aplicação finalizada")
```

### Exemplo de Saída no Console

```text
🚀 2025-06-18 03:27:00 - START   - Iniciando aplicação
ℹ️  2025-06-18 03:27:01 - INFO    - Configuração carregada com sucesso
⚠️  2025-06-18 03:27:02 - WARNING - Alerta: desempenho abaixo do esperado
❌  2025-06-18 03:27:03 - ERROR   - Erro crítico na conexão com o banco
✅  2025-06-18 03:27:04 - END     - Aplicação finalizada
```

---

## ✨ Funcionalidades

### 🎨 Níveis de Log com Cores e Emojis

| Nível     | Emoji | Cor (tema escuro) | Exemplo                                   |
|-----------|--------|-------------------|--------------------------------------------|
| DEBUG     | 🐛     | Amarelo Claro     | `🐛 Mensagem de debug`                     |
| INFO      | ℹ️     | Verde             | `ℹ️ Informação`                           |
| WARNING   | ⚠️     | Amarelo           | `⚠️ Alerta`                               |
| ERROR     | ❌     | Vermelho          | `❌ Erro crítico`                          |
| START     | 🚀     | Verde Escuro      | `🚀 Processo iniciado`                    |
| END       | ✅     | Verde Escuro      | `✅ Processo concluído`                   |

---

### 🔍 Emojis Automáticos Contextuais

O logger adiciona emojis baseados no conteúdo da mensagem:

```python
global_logger.info("Lendo arquivo de configuração")  # 📖 Lendo arquivo de configuração
global_logger.warning("Conexão com o servidor perdida")  # 🔴 Conexão com o servidor perdida
global_logger.error("Falha no processamento de dados")  # 🚫 Falha no processamento de dados
```

---

## ⚙️ Configuração Flexível

### Personalização de Cores

Você pode alterar a cor de qualquer nível:

```python
from custom_logger import ColorLogger

ColorLogger.set_color('ERROR', '\033[38;5;129m')  # Roxo para erros
```
| Nome da Cor   | ANSI (8-bit)     | HEX       | Cor (Visualização)                                                                                          |
| ------------- | ---------------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| Vermelho      | `\033[38;5;196m` | `#FF0000` | <span style="display:inline-block;width:20px;height:20px;background:#FF0000;border:1px solid #000;"></span> |
| Verde         | `\033[38;5;46m`  | `#00FF00` | <span style="display:inline-block;width:20px;height:20px;background:#00FF00;border:1px solid #000;"></span> |
| Azul          | `\033[38;5;21m`  | `#0000FF` | <span style="display:inline-block;width:20px;height:20px;background:#0000FF;border:1px solid #000;"></span> |
| Amarelo       | `\033[38;5;226m` | `#FFFF00` | <span style="display:inline-block;width:20px;height:20px;background:#FFFF00;border:1px solid #000;"></span> |
| Ciano         | `\033[38;5;51m`  | `#00FFFF` | <span style="display:inline-block;width:20px;height:20px;background:#00FFFF;border:1px solid #000;"></span> |
| Magenta       | `\033[38;5;201m` | `#FF00FF` | <span style="display:inline-block;width:20px;height:20px;background:#FF00FF;border:1px solid #000;"></span> |
| Preto         | `\033[38;5;16m`  | `#000000` | <span style="display:inline-block;width:20px;height:20px;background:#000000;border:1px solid #ccc;"></span> |
| Branco        | `\033[38;5;231m` | `#FFFFFF` | <span style="display:inline-block;width:20px;height:20px;background:#FFFFFF;border:1px solid #000;"></span> |
| Cinza         | `\033[38;5;244m` | `#808080` | <span style="display:inline-block;width:20px;height:20px;background:#808080;border:1px solid #000;"></span> |
| Marrom        | `\033[38;5;94m`  | `#A52A2A` | <span style="display:inline-block;width:20px;height:20px;background:#A52A2A;border:1px solid #000;"></span> |
| Rosa          | `\033[38;5;218m` | `#FFC0CB` | <span style="display:inline-block;width:20px;height:20px;background:#FFC0CB;border:1px solid #000;"></span> |
| Roxo          | `\033[38;5;129m` | `#800080` | <span style="display:inline-block;width:20px;height:20px;background:#800080;border:1px solid #000;"></span> |
| Laranja       | `\033[38;5;208m` | `#FFA500` | <span style="display:inline-block;width:20px;height:20px;background:#FFA500;border:1px solid #000;"></span> |
| Amarelo claro | `\033[38;5;229m` | `#E9E784` | <span style="display:inline-block;width:20px;height:20px;background:#E9E784;border:1px solid #000;"></span> |

### Diretório de Logs

Defina o diretório de logs ou desative completamente a gravação:

```python
logger = ColorLogger.setup_logger(log_dir="logs/meus_logs")  # Salva em arquivos
logger = ColorLogger.setup_logger(log_dir=None)              # Apenas console
```

---

## 📁 Organização de Logs

### Estrutura de Pastas

```
projeto/
├── logs/
│   ├── health_alerts_20250618.log
│   ├── health_alerts_20250619.log
└── main.py
```

### Formato dos Arquivos

```text
2025-06-18 03:27:00 - INFO    - ℹ️ Sistema iniciado
2025-06-18 03:30:00 - WARNING - ⚠️ Alta carga de CPU
2025-06-18 03:35:00 - ERROR   - ❌ Falha na conexão com o banco
```

---

## 💡 Boas Práticas

### Marcar Início e Fim de Processos

```python
global_logger.start("Iniciando processamento de dados")
# ... execução ...
global_logger.end("Processamento concluído com sucesso")
```

### Adicionar Contexto aos Erros

```python
try:
    process_file("dados.csv")
except Exception as e:
    global_logger.error(f"Falha ao processar 'dados.csv': {e}")
```

### Utilizar Placeholders

```python
global_logger.info("Processados %d registros de %s", total, arquivo)
```

---

## 🛠️ API Completa

### Métodos Disponíveis

```python
global_logger.debug(msg, *args, **kwargs)    # Log de depuração
global_logger.info(msg, *args, **kwargs)     # Log informativo
global_logger.warning(msg, *args, **kwargs)  # Log de aviso
global_logger.error(msg, *args, **kwargs)    # Log de erro
global_logger.critical(msg, *args, **kwargs) # Log crítico
global_logger.start(msg, *args, **kwargs)    # Início de processo
global_logger.end(msg, *args, **kwargs)      # Fim de processo
```

### Adição de Handlers

```python
import logging
from custom_logger import ColorLogger

handler = logging.StreamHandler()
handler.setFormatter(ColorLogger.get_formatter())
global_logger.addHandler(handler)
```

---

## 📝 Notas de Versão

### Versão 1.0.0

- Emojis automáticos
- Cores ANSI no console
- Geração automática de arquivos diários

### Planejado para versões futuras

- Suporte a logs assíncronos
- Integração com ferramentas como **Sentry** e **ELK**
- Configuração via arquivos **YAML** ou **JSON**

---

## Pacote Instalável

### Solução 1: Pacote Instalável (Recomendado)

1 - Crie uma estrutura de pacote:
```
workspaceTasy/
├── logger/
│   ├── __init__.py
│   ├── reportUnimed.py
│   └── setup.py
└── outros_projetos/
```
2 - Crie logger/setup.py:
```python
from setuptools import setup, find_packages

setup(
    name="tasy_logger",
    version="0.1",
    packages=find_packages(),
)
```

3 - Instale o pacote (dentro da pasta logger):
```python
pip install -e .
```

4 - Agora importe de qualquer lugar:
```python
from logger.reportUnimed import global_logger
```

---

## 📄 Licença

Distribuído sob a **MIT License** — livre para uso, modificação e redistribuição.

---

## ❓ Suporte

Para dúvidas, sugestões ou problemas, abra uma *issue* no repositório ou participe da comunidade no Discord da **xAI**.

---

Desenvolvido com 💖 pela comunidade Python.

-----INSTALANDO PACOTE GLOBAL
1 - 
D:\projectPython\schedulersPython\loggerUnimed
& "C:\Program Files\Python310\python.exe" setup.py sdist bdist_wheel

2 - 
& "C:\Program Files\Python310\python.exe" -m pip install D:\projectPython\schedulersPython\loggerUnimed\dist\loggerUnimed-0.1-py3-none-any.whl

3 -
Use em qualquer projeto
from reportUnimed import global_logger
logger = global_logger()


# RECOMPILAR O PROJETO
1. Verifique as alterações no projeto
Antes de recompilar, confirme que todas as alterações no código (como no reportUnimed.py, __init__.py ou outros arquivos) foram feitas e testadas. Se você alterou a versão no setup.py (como explicado na pergunta anterior), certifique-se de que a nova versão está correta.
Por exemplo, no setup.py, a linha da versão deve refletir a versão desejada:

```python
version='0.1.1',  # Ou a versão que você escolheu
```

2. Limpe os arquivos de build anteriores
Para evitar conflitos com arquivos de builds anteriores, remova as pastas build, dist e loggerUnimed.egg-info. No terminal, navegue até a raiz do projeto:
```bash
cd D:\projectPython\schedulersPython\loggerUnimed
```
Em seguida, execute:
```bash
rmdir /s /q build dist loggerUnimed.egg-info
```
No powershell execute:
```bash
Remove-Item -Path build,dist,loggerUnimed.egg-info -Recurse -Force -ErrorAction SilentlyContinue
```

3 - Gere os novos arquivos de distribuição:
Certifique-se de que as ferramentas wheel e setuptools estão instaladas:
```bash
pip install wheel setuptools
```
Em seguida, gere os arquivos .whl e .tar.gz:
```bash
python setup.py sdist bdist_wheel
```
4 -Verifique os arquivos gerados:
Liste os arquivos na pasta dist para confirmar que os novos arquivos foram criados:
```bash
Get-ChildItem -Path .\dist
```

5 -Teste a instalação da nova versão:
Instale o pacote gerado
```bash
pip install .\dist\loggerUnimed-0.1.1-py3-none-any.whl
```


Remove-Item -Path build,dist,loggerUnimed.egg-info -Recurse -Force -ErrorAction SilentlyContinue

rmdir /s /q build dist loggerUnimed.egg-info



----------------------------------
Para Instalar em outros PROJETOS

cd D:\projectPython\schedulersPython\loggerUnimed\dist
pip install loggerunimed-0.1.1-py3-none-any.whl

D:\projectPython\schedulersPython\loggerUnimed\dist\loggerunimed-0.1.1-py3-none-any.whl

