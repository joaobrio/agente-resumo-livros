# 🚀 Guia Prático: Como Acessar e Processar Livros do Kindle

## Passo 1: Instalar o Kindle no Computador

### macOS
1. Baixe o Kindle para Mac: https://www.amazon.com.br/kindle-dbs/fd/kcp
2. Faça login com sua conta Amazon
3. Baixe os livros que deseja processar (clique com botão direito → "Baixar")

### Windows
1. Baixe o Kindle para PC: https://www.amazon.com.br/kindle-dbs/fd/kcp
2. Instale e faça login
3. Baixe os livros desejados

## Passo 2: Localizar Seus Livros

### 🔍 Usar nosso Script (Recomendado)

```bash
# 1. Vá para a pasta do agente
cd /Users/joaorovere/Documents/GitHub/second-brain/agente-resumo-livros

# 2. Liste seus livros Kindle
python3 scripts/kindle_finder.py list

# Você verá algo como:
# 📚 Encontrados 4 livros:
# 
# 1. Atomic Habits
#    Autor: James Clear
#    Formato: .azw (3.2 MB)
# 
# 2. The Psychology of Money
#    Autor: Morgan Housel
#    Formato: .azw3 (1.8 MB)
```

### 📂 Localização Manual

**macOS:**
```bash
cd ~/Library/Containers/com.amazon.Kindle/Data/Library/Application\ Support/Kindle/My\ Kindle\ Content/
ls -la
```

**Windows:**
```
C:\Users\[SEU_USUARIO]\Documents\My Kindle Content
```

## Passo 3: Exportar um Livro Específico

### Opção A: Modo Interativo (Mais Fácil)

```bash
# Execute o comando e escolha o número
python3 scripts/kindle_finder.py export

# O script vai:
# 1. Listar todos os seus livros
# 2. Pedir para você digitar o número
# 3. Copiar o livro para uma pasta de trabalho
```

### Opção B: Exportar Direto

```bash
# Se você já sabe o número do livro (da lista)
python3 scripts/kindle_finder.py export -i 1
```

## Passo 4: Processar o Livro

### 🎯 Processo Completo Automatizado

```bash
# 1. Instalar ferramentas (só na primeira vez)
./scripts/setup_kindle_tools.sh

# 2. Processar o livro exportado
python3 scripts/kindle_processor.py ~/KindleBooks/input/[nome-do-livro].azw3 --category business

# O script vai:
# - Converter para texto
# - Extrair metadados
# - Limpar formatação
# - Preparar para o agente de resumo
```

## Passo 5: Gerar Resumo com o Agente

```python
# Use o arquivo gerado (.agent_request.json)
from agente_resumo import AgenteResumoLivros

agente = AgenteResumoLivros()
resultado = agente.processar_arquivo_request("livro.agent_request.json")

# Salvar resumo
with open("resumo_completo.md", "w") as f:
    f.write(resultado.formato_markdown())
```

## 🎮 Exemplo Prático Completo

Vamos processar um livro do início ao fim:

```bash
# 1. Entrar na pasta do projeto
cd /Users/joaorovere/Documents/GitHub/second-brain/agente-resumo-livros

# 2. Listar livros disponíveis
python3 scripts/kindle_finder.py list

# Saída:
# 📚 Encontrados 4 livros:
# 1. Atomic Habits
# 2. The Psychology of Money
# 3. Deep Work
# 4. The Lean Startup

# 3. Exportar o livro #2
python3 scripts/kindle_finder.py export -i 2

# 4. Processar com categoria apropriada
python3 scripts/kindle_processor.py ~/KindleBooks/input/The_Psychology_of_Money_Morgan_Housel.azw3 --category business

# 5. Ver resultado
ls -la ~/KindleBooks/output/
# The_Psychology_of_Money_Morgan_Housel.txt
# The_Psychology_of_Money_Morgan_Housel.agent_request.json
```

## 🤖 Automação Total

### Configurar Monitoramento Automático

```bash
# 1. Criar script de automação
cat > ~/process_new_kindle_book.sh << 'EOF'
#!/bin/bash
BOOK_PATH="$1"
CATEGORY="${2:-general}"

echo "🚀 Processando novo livro: $BOOK_PATH"

# Processar
python3 /path/to/kindle_processor.py "$BOOK_PATH" --category "$CATEGORY"

# Notificar
osascript -e 'display notification "Livro processado e pronto para resumo!" with title "Kindle Processor"'
EOF

chmod +x ~/process_new_kindle_book.sh

# 2. Monitorar pasta
python3 scripts/kindle_finder.py export-all
kindle-watch  # Monitora novos arquivos
```

## 💡 Dicas e Truques

### 1. Processar Vários Livros
```bash
# Exportar todos de uma vez
python3 scripts/kindle_finder.py export-all

# Processar em lote
for book in ~/KindleBooks/input/*.azw*; do
    python3 scripts/kindle_processor.py "$book" --category business
done
```

### 2. Categorias Disponíveis
- `technical` - Livros técnicos/programação
- `business` - Negócios e finanças
- `self_help` - Autoajuda e desenvolvimento pessoal
- `fiction` - Ficção e literatura
- `academic` - Acadêmicos e didáticos
- `general` - Categoria padrão

### 3. Problemas Comuns

**"Livro não encontrado"**
- Certifique-se de que baixou o livro no app Kindle
- Tente sincronizar: No Kindle app → Sync

**"Erro de conversão"**
- Instale o Calibre: `brew install --cask calibre`
- Para livros com DRM, veja o guia completo em `guias/extracao_kindle.md`

**"Texto mal formatado"**
- Use a flag `--force` para reprocessar
- Ajuste as opções no `config.json`

## 📱 Alternativa: Kindle Cloud Reader

Se preferir não instalar o app:

1. Acesse: https://read.amazon.com
2. Abra o livro desejado
3. Use a extensão do Chrome "Kindle Cloud Reader Exporter"
4. Salve como texto e processe

## 🎯 Comandos Rápidos

```bash
# Listar livros
python3 scripts/kindle_finder.py list

# Exportar interativo
python3 scripts/kindle_finder.py export

# Exportar específico
python3 scripts/kindle_finder.py export -i 3

# Processar
python3 scripts/kindle_processor.py [arquivo] --category [categoria]

# Ver resultados
ls -la ~/KindleBooks/output/
```

## 🆘 Precisa de Ajuda?

1. Verifique se o Kindle app está instalado e com livros baixados
2. Confirme que tem Python 3 instalado: `python3 --version`
3. Instale o Calibre se ainda não tem: `brew install --cask calibre`
4. Consulte o guia completo: `guias/extracao_kindle.md`

Agora você está pronto para processar qualquer livro do seu Kindle! 📚✨