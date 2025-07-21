#!/usr/bin/env python3
"""
Processador de Livros Kindle para Agente de Resumo
Automatiza extração, conversão e resumo de livros do Kindle
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KindleProcessor:
    """Processa livros do Kindle para resumo automático"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa o processador
        
        Args:
            config_path: Caminho para arquivo de configuração customizado
        """
        self.config = self._load_config(config_path)
        self.calibre_path = self._find_calibre()
        self.processed_cache = self._load_cache()
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Carrega configurações"""
        default_config = {
            "input_formats": [".azw", ".azw3", ".mobi", ".epub", ".pdf"],
            "output_format": "txt",
            "output_dir": "~/KindleBooks/output",
            "processed_dir": "~/KindleBooks/processed",
            "cache_file": "~/.kindle_processor_cache.json",
            "calibre_options": [
                "--enable-heuristics",
                "--unwrap-lines",
                "--normalize-text"
            ],
            "agente_config": {
                "tipo_resumo": "completo",
                "incluir_flashcards": True,
                "incluir_questoes": True
            }
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                
        return default_config
    
    def _find_calibre(self) -> str:
        """Encontra o executável do Calibre"""
        possible_paths = [
            "/Applications/calibre.app/Contents/MacOS/ebook-convert",  # macOS
            "/usr/bin/ebook-convert",  # Linux
            "C:\\Program Files\\Calibre2\\ebook-convert.exe",  # Windows
            "C:\\Program Files (x86)\\Calibre2\\ebook-convert.exe"  # Windows 32-bit
        ]
        
        # Verificar se está no PATH
        if subprocess.run(["which", "ebook-convert"], 
                         capture_output=True).returncode == 0:
            return "ebook-convert"
        
        # Verificar caminhos conhecidos
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        raise FileNotFoundError(
            "Calibre não encontrado. Instale em: https://calibre-ebook.com"
        )
    
    def _load_cache(self) -> Dict[str, Dict]:
        """Carrega cache de livros processados"""
        cache_path = Path(self.config["cache_file"]).expanduser()
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """Salva cache de livros processados"""
        cache_path = Path(self.config["cache_file"]).expanduser()
        with open(cache_path, 'w') as f:
            json.dump(self.processed_cache, f, indent=2)
    
    def _get_file_hash(self, filepath: str) -> str:
        """Calcula hash MD5 do arquivo"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def is_processed(self, filepath: str) -> bool:
        """Verifica se arquivo já foi processado"""
        file_hash = self._get_file_hash(filepath)
        return file_hash in self.processed_cache
    
    def convert_to_text(self, input_file: str) -> str:
        """
        Converte arquivo Kindle para texto
        
        Args:
            input_file: Caminho do arquivo de entrada
            
        Returns:
            Caminho do arquivo de texto convertido
        """
        input_path = Path(input_file)
        output_dir = Path(self.config["output_dir"]).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{input_path.stem}.txt"
        
        # Comando Calibre
        cmd = [
            self.calibre_path,
            str(input_path),
            str(output_file)
        ] + self.config["calibre_options"]
        
        logger.info(f"Convertendo: {input_path.name}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Conversão concluída: {output_file}")
            return str(output_file)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro na conversão: {e.stderr}")
            raise
    
    def extract_metadata(self, input_file: str) -> Dict[str, str]:
        """Extrai metadados do livro usando Calibre"""
        cmd = [
            self.calibre_path.replace("ebook-convert", "ebook-meta"),
            input_file
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse básico dos metadados
            metadata = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            return metadata
            
        except:
            logger.warning("Não foi possível extrair metadados")
            return {}
    
    def process_book(self, 
                    input_file: str, 
                    category: str = "general",
                    force: bool = False) -> Dict[str, Any]:
        """
        Processa um livro completo
        
        Args:
            input_file: Caminho do arquivo Kindle
            category: Categoria do livro (technical, business, fiction, etc)
            force: Forçar reprocessamento mesmo se já existe no cache
            
        Returns:
            Dicionário com resultados do processamento
        """
        input_path = Path(input_file)
        
        # Verificar formato suportado
        if input_path.suffix.lower() not in self.config["input_formats"]:
            raise ValueError(
                f"Formato não suportado: {input_path.suffix}\n"
                f"Formatos aceitos: {self.config['input_formats']}"
            )
        
        # Verificar cache
        file_hash = self._get_file_hash(input_file)
        if not force and file_hash in self.processed_cache:
            logger.info(f"Livro já processado: {input_path.name}")
            return self.processed_cache[file_hash]
        
        logger.info(f"Processando: {input_path.name}")
        
        # Extrair metadados
        metadata = self.extract_metadata(input_file)
        
        # Converter para texto
        text_file = self.convert_to_text(input_file)
        
        # Ler conteúdo
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Preparar resultado
        result = {
            "file": input_path.name,
            "hash": file_hash,
            "metadata": metadata,
            "category": category,
            "processed_at": datetime.now().isoformat(),
            "text_file": text_file,
            "content_preview": content[:500] + "...",
            "content_length": len(content),
            "status": "ready_for_agent"
        }
        
        # Salvar no cache
        self.processed_cache[file_hash] = result
        self._save_cache()
        
        # Mover arquivo processado
        if self.config.get("move_processed", True):
            processed_dir = Path(self.config["processed_dir"]).expanduser()
            processed_dir.mkdir(parents=True, exist_ok=True)
            
            new_path = processed_dir / input_path.name
            if not new_path.exists():
                os.rename(input_file, new_path)
                logger.info(f"Arquivo movido para: {new_path}")
        
        return result
    
    def batch_process(self, 
                     input_dir: str,
                     category: str = "general",
                     recursive: bool = True) -> list:
        """
        Processa múltiplos livros de um diretório
        
        Args:
            input_dir: Diretório com arquivos Kindle
            category: Categoria padrão dos livros
            recursive: Buscar em subdiretórios
            
        Returns:
            Lista de resultados processados
        """
        input_path = Path(input_dir).expanduser()
        results = []
        
        # Buscar arquivos
        pattern = "**/*" if recursive else "*"
        for file_path in input_path.glob(pattern):
            if file_path.suffix.lower() in self.config["input_formats"]:
                try:
                    result = self.process_book(str(file_path), category)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Erro processando {file_path}: {e}")
        
        logger.info(f"Processados {len(results)} livros")
        return results
    
    def clean_text(self, text: str) -> str:
        """
        Limpa e normaliza texto extraído
        
        Args:
            text: Texto bruto do livro
            
        Returns:
            Texto limpo e formatado
        """
        import re
        
        # Remover múltiplas quebras de linha
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remover espaços extras
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remover caracteres de controle
        text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
        
        # Remover linhas de cabeçalho/rodapé repetitivas
        lines = text.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            # Pular linhas que parecem números de página
            if re.match(r'^\s*\d+\s*$', line):
                continue
            # Pular linhas muito curtas repetitivas
            if len(line.strip()) < 5 and i > 0 and i < len(lines)-1:
                if lines[i-1].strip() == line.strip():
                    continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def generate_summary_request(self, 
                                text_file: str,
                                metadata: Dict[str, str],
                                category: str) -> Dict[str, Any]:
        """
        Prepara requisição para o agente de resumo
        
        Args:
            text_file: Caminho do arquivo de texto
            metadata: Metadados do livro
            category: Categoria do livro
            
        Returns:
            Dicionário com dados para o agente
        """
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Limpar texto
        content = self.clean_text(content)
        
        return {
            "content": content,
            "metadata": {
                "title": metadata.get("Title", "Unknown"),
                "author": metadata.get("Author(s)", "Unknown"),
                "publisher": metadata.get("Publisher", "Unknown"),
                "language": metadata.get("Languages", "Unknown"),
                "category": category
            },
            "config": self.config["agente_config"],
            "request_type": "full_analysis"
        }


def main():
    """Função principal para uso via CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Processa livros do Kindle para resumo automático"
    )
    parser.add_argument(
        "input",
        help="Arquivo ou diretório de entrada"
    )
    parser.add_argument(
        "-c", "--category",
        default="general",
        choices=["technical", "business", "fiction", "academic", "self_help", "general"],
        help="Categoria do livro"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Forçar reprocessamento"
    )
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="Processar diretório em lote"
    )
    parser.add_argument(
        "--config",
        help="Arquivo de configuração customizado"
    )
    
    args = parser.parse_args()
    
    # Inicializar processador
    processor = KindleProcessor(args.config)
    
    try:
        if args.batch:
            # Processamento em lote
            results = processor.batch_process(
                args.input,
                category=args.category
            )
            
            print(f"\nProcessados {len(results)} livros:")
            for result in results:
                print(f"- {result['file']}: {result['status']}")
        else:
            # Arquivo único
            result = processor.process_book(
                args.input,
                category=args.category,
                force=args.force
            )
            
            print("\nLivro processado com sucesso!")
            print(f"Arquivo: {result['file']}")
            print(f"Texto salvo em: {result['text_file']}")
            print(f"Tamanho: {result['content_length']} caracteres")
            
            if result['metadata']:
                print("\nMetadados:")
                for key, value in result['metadata'].items():
                    if value and value != "Unknown":
                        print(f"  {key}: {value}")
            
            # Gerar requisição para o agente
            agent_request = processor.generate_summary_request(
                result['text_file'],
                result['metadata'],
                args.category
            )
            
            # Salvar requisição
            request_file = Path(result['text_file']).with_suffix('.agent_request.json')
            with open(request_file, 'w', encoding='utf-8') as f:
                json.dump(agent_request, f, ensure_ascii=False, indent=2)
            
            print(f"\nRequisição para agente salva em: {request_file}")
            print("Use este arquivo com o agente de resumo para gerar a análise completa.")
            
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()