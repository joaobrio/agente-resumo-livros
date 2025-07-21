#!/usr/bin/env python3
"""
Kindle Finder - Encontra e lista livros do Kindle no computador
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
import shutil

class KindleFinder:
    """Localiza e identifica livros do Kindle"""
    
    def __init__(self):
        self.kindle_paths = self._get_kindle_paths()
        self.books = []
        
    def _get_kindle_paths(self) -> List[Path]:
        """Retorna possíveis localizações dos livros Kindle"""
        paths = []
        
        # macOS
        mac_path = Path.home() / "Library/Containers/com.amazon.Kindle/Data/Library/Application Support/Kindle/My Kindle Content"
        if mac_path.exists():
            paths.append(mac_path)
            
        # Windows
        win_path = Path.home() / "Documents/My Kindle Content"
        if win_path.exists():
            paths.append(win_path)
            
        # Linux (Kindle via Wine)
        linux_path = Path.home() / ".wine/drive_c/users" / os.environ.get('USER', '') / "My Documents/My Kindle Content"
        if linux_path.exists():
            paths.append(linux_path)
            
        return paths
    
    def _read_kindle_db(self, db_path: Path) -> Dict[str, Dict]:
        """Lê metadados do banco de dados do Kindle"""
        metadata = {}
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Tentar diferentes queries dependendo da versão
            queries = [
                """SELECT ASIN, Title, Authors, Publisher 
                   FROM book_metadata""",
                """SELECT ASIN, title, authors, publisher 
                   FROM Books""",
                """SELECT id, title, author, publisher 
                   FROM kindle_books"""
            ]
            
            for query in queries:
                try:
                    cursor.execute(query)
                    for row in cursor.fetchall():
                        asin = row[0]
                        metadata[asin] = {
                            'title': row[1] or 'Unknown Title',
                            'author': row[2] or 'Unknown Author',
                            'publisher': row[3] or ''
                        }
                    break
                except sqlite3.OperationalError:
                    continue
                    
            conn.close()
        except Exception as e:
            print(f"Aviso: Não foi possível ler banco de dados: {e}")
            
        return metadata
    
    def find_books(self) -> List[Dict]:
        """Encontra todos os livros Kindle disponíveis"""
        self.books = []
        
        for kindle_path in self.kindle_paths:
            print(f"\n📂 Procurando em: {kindle_path}")
            
            # Ler metadados do banco se disponível
            db_path = kindle_path / "book_asset.db"
            metadata = {}
            if db_path.exists():
                metadata = self._read_kindle_db(db_path)
                print(f"   ✓ Banco de dados encontrado com {len(metadata)} registros")
            
            # Procurar arquivos de livros
            for item in kindle_path.iterdir():
                if item.is_dir() and '_EBOK' in item.name:
                    # É uma pasta de livro
                    asin = item.name.replace('_EBOK', '')
                    book_files = list(item.glob('*.azw*')) + list(item.glob('*.mobi'))
                    
                    if book_files:
                        main_file = max(book_files, key=lambda f: f.stat().st_size)
                        
                        book_info = {
                            'asin': asin,
                            'path': str(main_file),
                            'format': main_file.suffix,
                            'size_mb': round(main_file.stat().st_size / 1024 / 1024, 2),
                            'folder': str(item)
                        }
                        
                        # Adicionar metadados se disponível
                        if asin in metadata:
                            book_info.update(metadata[asin])
                        else:
                            # Tentar extrair do nome do arquivo
                            book_info['title'] = main_file.stem
                            book_info['author'] = 'Unknown'
                        
                        self.books.append(book_info)
        
        # Ordenar por título
        self.books.sort(key=lambda x: x.get('title', 'Unknown'))
        return self.books
    
    def list_books(self, detailed: bool = False) -> None:
        """Lista todos os livros encontrados"""
        if not self.books:
            self.find_books()
        
        print(f"\n📚 Encontrados {len(self.books)} livros:\n")
        
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.get('title', 'Unknown Title')}")
            print(f"   Autor: {book.get('author', 'Unknown')}")
            print(f"   Formato: {book['format']} ({book['size_mb']} MB)")
            
            if detailed:
                print(f"   ASIN: {book['asin']}")
                print(f"   Caminho: {book['path']}")
            print()
    
    def export_book(self, book_index: int, output_dir: str = None) -> str:
        """Exporta um livro para processamento"""
        if not self.books:
            self.find_books()
            
        if book_index < 1 or book_index > len(self.books):
            raise ValueError(f"Índice inválido. Escolha entre 1 e {len(self.books)}")
        
        book = self.books[book_index - 1]
        
        # Diretório de saída
        if output_dir is None:
            output_dir = Path.home() / "KindleBooks" / "input"
        else:
            output_dir = Path(output_dir)
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar arquivo
        source = Path(book['path'])
        filename = f"{book.get('title', 'Unknown').replace('/', '-')}_{book.get('author', 'Unknown').replace('/', '-')}{source.suffix}"
        destination = output_dir / filename
        
        print(f"\n📤 Exportando livro...")
        print(f"   De: {source}")
        print(f"   Para: {destination}")
        
        shutil.copy2(source, destination)
        
        print(f"\n✅ Livro exportado com sucesso!")
        print(f"\nPara processar, execute:")
        print(f"   python kindle_processor.py \"{destination}\"")
        
        return str(destination)
    
    def export_all(self, output_dir: str = None) -> List[str]:
        """Exporta todos os livros"""
        if not self.books:
            self.find_books()
            
        exported = []
        
        print(f"\n📤 Exportando {len(self.books)} livros...")
        
        for i, book in enumerate(self.books, 1):
            try:
                path = self.export_book(i, output_dir)
                exported.append(path)
            except Exception as e:
                print(f"❌ Erro ao exportar {book.get('title', 'Unknown')}: {e}")
        
        print(f"\n✅ {len(exported)} livros exportados com sucesso!")
        return exported


def main():
    """Interface de linha de comando"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Encontra e exporta livros do Kindle"
    )
    parser.add_argument(
        'action',
        choices=['list', 'export', 'export-all'],
        help='Ação a executar'
    )
    parser.add_argument(
        '-i', '--index',
        type=int,
        help='Índice do livro para exportar (use com export)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Diretório de saída'
    )
    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Mostrar informações detalhadas'
    )
    
    args = parser.parse_args()
    
    finder = KindleFinder()
    
    if args.action == 'list':
        finder.list_books(detailed=args.detailed)
        
    elif args.action == 'export':
        if not args.index:
            # Modo interativo
            finder.list_books()
            try:
                index = int(input("Digite o número do livro para exportar: "))
                finder.export_book(index, args.output)
            except (ValueError, KeyboardInterrupt):
                print("\nOperação cancelada.")
        else:
            finder.export_book(args.index, args.output)
            
    elif args.action == 'export-all':
        finder.export_all(args.output)


if __name__ == "__main__":
    main()