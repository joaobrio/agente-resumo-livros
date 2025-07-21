# Guia de Extração e Processamento de Livros do Kindle

## Visão Geral

Este guia detalha métodos para extrair conteúdo de livros do Kindle e processá-los com nosso agente de resumo.

## Métodos de Extração

### 1. Calibre (Recomendado)

**O que é**: Software gratuito e open-source para gerenciamento de e-books.

**Instalação**:
```bash
# macOS
brew install --cask calibre

# Windows/Linux
# Baixar de: https://calibre-ebook.com/download
```

**Processo**:
1. Adicionar livro do Kindle ao Calibre
2. Converter para formato desejado (TXT, PDF, EPUB)
3. Usar DeDRM plugin se necessário (para livros com DRM)

**Configuração do DeDRM**:
```
1. Baixar DeDRM_tools de: https://github.com/apprenticeharper/DeDRM_tools
2. Em Calibre: Preferências > Plugins > Carregar plugin de arquivo
3. Selecionar DeDRM_plugin.zip
4. Reiniciar Calibre
```

### 2. Kindle for PC/Mac + Extração

**Processo**:
1. Instalar Kindle for PC/Mac
2. Baixar livros para leitura offline
3. Localizar arquivos:
   - Windows: `C:\Users\[username]\Documents\My Kindle Content`
   - macOS: `~/Library/Containers/com.amazon.Kindle/Data/Library/Application Support/Kindle/My Kindle Content`
4. Usar KFX Input plugin no Calibre para converter

### 3. Send to Kindle + Email

**Configuração**:
1. Configurar email do Kindle em: https://www.amazon.com/hz/mycd/myx
2. Enviar documento para [seu-email]@kindle.com
3. Baixar do Kindle como PDF

### 4. Kindle Highlights Export

**Para resumos parciais**:
1. Acessar: https://read.amazon.com/notebook
2. Exportar highlights e notas
3. Processar com nosso agente

## Bibliotecas Python para Automação

### 1. kindle-highlights

```python
# Instalação
pip install kindle-highlights

# Uso
from kindle_highlights import get_highlights

highlights = get_highlights(
    email="seu-email@example.com",
    password="sua-senha"
)

for book in highlights:
    print(f"Livro: {book['title']}")
    for highlight in book['highlights']:
        print(f"- {highlight['text']}")
```

### 2. pykindle

```python
# Instalação
pip install pykindle

# Conversão básica
from pykindle import KindleBook

book = KindleBook('caminho/para/arquivo.azw3')
text = book.extract_text()
book.save_as_txt('output.txt')
```

### 3. ebooklib

```python
# Instalação
pip install ebooklib

# Leitura de EPUB
from ebooklib import epub

book = epub.read_epub('livro.epub')
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        content = item.get_content()
        # Processar conteúdo HTML
```

## Integração com o Agente de Resumo

### Script de Pipeline Completo

```python
import os
import subprocess
from pathlib import Path
from agente_resumo import AgenteResumoLivros

class KindleBookProcessor:
    def __init__(self):
        self.calibre_path = "/Applications/calibre.app/Contents/MacOS/ebook-convert"
        self.agente = AgenteResumoLivros()
    
    def convert_kindle_file(self, input_file, output_format='txt'):
        """Converte arquivo Kindle usando Calibre"""
        output_file = Path(input_file).stem + f'.{output_format}'
        
        cmd = [
            self.calibre_path,
            input_file,
            output_file,
            '--enable-heuristics'
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
    
    def process_kindle_book(self, kindle_file, book_category='general'):
        """Pipeline completo: conversão + resumo"""
        # 1. Converter para texto
        print(f"Convertendo {kindle_file}...")
        text_file = self.convert_kindle_file(kindle_file)
        
        # 2. Ler conteúdo
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 3. Processar com agente
        print("Gerando resumo...")
        resultado = self.agente.processar_livro(
            conteudo=content,
            tipo_resumo="completo",
            categoria=book_category
        )
        
        # 4. Limpar arquivo temporário
        os.remove(text_file)
        
        return resultado

# Uso
processor = KindleBookProcessor()
resumo = processor.process_kindle_book(
    'meu_livro.azw3',
    book_category='business'
)
```

### Automação com Watchdog

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class KindleWatcher(FileSystemEventHandler):
    def __init__(self, processor):
        self.processor = processor
    
    def on_created(self, event):
        if event.src_path.endswith(('.azw', '.azw3', '.mobi')):
            print(f"Novo livro detectado: {event.src_path}")
            time.sleep(2)  # Aguardar arquivo ser completamente escrito
            self.processor.process_kindle_book(event.src_path)

# Monitorar pasta do Kindle
observer = Observer()
observer.schedule(
    KindleWatcher(processor),
    path='~/Documents/My Kindle Content',
    recursive=True
)
observer.start()
```

## Considerações Legais e Éticas

### DRM (Digital Rights Management)

1. **Uso Pessoal**: Remover DRM para uso pessoal é geralmente aceito
2. **Backup**: Fazer backup de conteúdo comprado é razoável
3. **Compartilhamento**: NÃO compartilhe conteúdo protegido por direitos autorais
4. **Conformidade**: Verifique leis locais sobre DRM

### Boas Práticas

1. Use apenas com livros que você comprou legalmente
2. Mantenha backups privados
3. Respeite os direitos dos autores
4. Considere alternativas legais (biblioteca, empréstimo)

## Solução de Problemas

### Erro: "DRM protected file"
```bash
# Solução 1: Usar versão antiga do Kindle app
# Kindle for PC 1.17 ou anterior funciona melhor com DeDRM

# Solução 2: Verificar configuração do DeDRM
# Ensure que a chave da sua conta está configurada
```

### Erro: "Calibre não reconhece formato"
```bash
# Instalar plugins adicionais
# KFX Input, KePub Output, etc.
```

### Texto mal formatado após conversão
```python
# Usar opções avançadas do Calibre
subprocess.run([
    calibre_path,
    input_file,
    output_file,
    '--enable-heuristics',
    '--unwrap-lines',
    '--normalize-text'
])
```

## Alternativas e Ferramentas Complementares

### 1. k2pdfopt
- Otimiza PDFs para leitura em Kindle
- Útil para conversão reversa

### 2. Kindle Comic Converter
- Para mangás e quadrinhos
- Mantém formatação visual

### 3. Sigil
- Editor EPUB avançado
- Permite edição manual pós-conversão

## Script de Configuração Rápida

```bash
#!/bin/bash
# setup_kindle_tools.sh

echo "Instalando ferramentas para processamento Kindle..."

# Calibre
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install --cask calibre
else
    echo "Baixe Calibre de: https://calibre-ebook.com"
fi

# Python dependencies
pip install kindle-highlights pykindle ebooklib beautifulsoup4 watchdog

# Criar diretórios
mkdir -p ~/KindleBooks/{input,output,processed}

echo "Configuração completa!"
echo "Próximos passos:"
echo "1. Instalar DeDRM plugin no Calibre"
echo "2. Configurar credenciais do Kindle"
echo "3. Testar com um livro de exemplo"
```

## Exemplo de Uso Completo

```python
# main.py
from kindle_processor import KindleBookProcessor
import json

def main():
    processor = KindleBookProcessor()
    
    # Processar livro
    resultado = processor.process_kindle_book(
        'Clean_Code.azw3',
        book_category='technical'
    )
    
    # Salvar resumo
    with open('Clean_Code_resumo.json', 'w', encoding='utf-8') as f:
        json.dump(resultado.to_dict(), f, ensure_ascii=False, indent=2)
    
    # Gerar flashcards
    flashcards = resultado.flashcards
    with open('Clean_Code_flashcards.txt', 'w', encoding='utf-8') as f:
        for card in flashcards:
            f.write(f"Q: {card['front']}\n")
            f.write(f"A: {card['back']}\n\n")
    
    print("Processamento completo!")
    print(f"Resumo salvo em: Clean_Code_resumo.json")
    print(f"Flashcards salvos em: Clean_Code_flashcards.txt")

if __name__ == "__main__":
    main()
```

## Recursos Adicionais

1. **DeDRM Tools**: https://github.com/apprenticeharper/DeDRM_tools
2. **Calibre Plugins**: https://www.mobileread.com/forums/showthread.php?t=247843
3. **Kindle Tools**: https://github.com/jefftriplett/kindle-tools
4. **Python Kindle**: https://github.com/lxyu/kindle-highlights

## Conclusão

Com essas ferramentas e técnicas, você pode:
1. Extrair conteúdo de livros do Kindle
2. Converter para formatos processáveis
3. Integrar com nosso agente de resumo
4. Automatizar todo o processo

Lembre-se sempre de respeitar os direitos autorais e usar essas ferramentas apenas para fins pessoais e legais.