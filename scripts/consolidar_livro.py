#!/usr/bin/env python3
"""
Consolidador de Transcrições de Livro
Combina múltiplos arquivos de transcrição em um único documento bem formatado
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple
import unicodedata

class ConsolidadorLivro:
    """Consolida e formata transcrições de livro em um único documento"""
    
    def __init__(self):
        self.estrutura = {
            'titulo': 'Criando um Segundo Cérebro',
            'autor': 'Tiago Forte',
            'partes': {},
            'capitulos': {},
            'secoes': {}
        }
        self.conteudo_consolidado = []
        self.indice = []
        
    def processar_diretorio(self, diretorio: str) -> str:
        """Processa todos os arquivos de transcrição e retorna o documento consolidado"""
        
        dir_path = Path(diretorio)
        arquivos = sorted(dir_path.glob('transcricao-paginas-*.md'))
        
        if not arquivos:
            raise FileNotFoundError("Nenhuma transcrição encontrada")
            
        print(f"📚 Processando {len(arquivos)} arquivos...")
        
        # Processar cada arquivo
        for arquivo in arquivos:
            print(f"  📄 {arquivo.name}")
            self._processar_arquivo(arquivo)
            
        # Gerar documento final
        return self._gerar_documento()
        
    def _processar_arquivo(self, arquivo: Path):
        """Processa um arquivo de transcrição"""
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        # Remover marcadores de página e metadados
        conteudo = self._limpar_conteudo(conteudo)
        
        # Processar estrutura
        self._extrair_estrutura(conteudo)
        
    def _limpar_conteudo(self, texto: str) -> str:
        """Limpa o conteúdo removendo elementos desnecessários"""
        
        # Remover cabeçalhos de página
        texto = re.sub(r'^## Página \d+\n', '', texto, flags=re.MULTILINE)
        texto = re.sub(r'^---\n', '', texto, flags=re.MULTILINE)
        
        # Remover metadados do início
        texto = re.sub(r'^# Transcrição:.*?\n\n', '', texto)
        
        # Remover informações de publicação repetitivas
        texto = re.sub(r'dLivros\s+Livros.*?Converted by convertEPub', '', texto, flags=re.DOTALL)
        texto = re.sub(r'Copyright.*?GMT Editores.*?\.com\.br', '', texto, flags=re.DOTALL)
        
        return texto
        
    def _extrair_estrutura(self, texto: str):
        """Extrai a estrutura hierárquica do livro"""
        
        linhas = texto.split('\n')
        buffer = []
        
        for linha in linhas:
            tipo, conteudo = self._classificar_linha(linha)
            
            if tipo == 'sumario':
                self._processar_sumario(linhas[linhas.index(linha):])
            elif tipo in ['parte', 'capitulo', 'secao']:
                if buffer:
                    self._adicionar_paragrafo(' '.join(buffer))
                    buffer = []
                self._adicionar_elemento(tipo, conteudo)
            elif tipo == 'paragrafo' and conteudo:
                buffer.append(conteudo)
            elif tipo == 'citacao':
                if buffer:
                    self._adicionar_paragrafo(' '.join(buffer))
                    buffer = []
                self._adicionar_citacao(conteudo)
            elif not linha.strip() and buffer:
                self._adicionar_paragrafo(' '.join(buffer))
                buffer = []
                
        if buffer:
            self._adicionar_paragrafo(' '.join(buffer))
            
    def _classificar_linha(self, linha: str) -> Tuple[str, str]:
        """Classifica o tipo de linha e retorna conteúdo limpo"""
        
        linha = linha.strip()
        
        # Padrões de identificação
        if re.match(r'^SUMÁRIO$', linha):
            return 'sumario', linha
            
        if re.match(r'^PARTE\s+(UM|DOIS|TRÊS|QUATRO|CINCO)', linha):
            return 'parte', linha
            
        if re.match(r'^Capítulo\s+\d+$', linha):
            return 'capitulo', linha
            
        if re.match(r'^[A-Z][a-z]+.*[a-z]+$', linha) and len(linha) > 10 and len(linha) < 50:
            # Possível título de seção
            proxima_linha = self._verificar_proxima_linha(linha)
            if proxima_linha and len(proxima_linha) > 50:
                return 'secao', linha
                
        if linha.startswith('"') and '"' in linha[1:] and '–' in linha:
            return 'citacao', linha
            
        return 'paragrafo', linha
        
    def _verificar_proxima_linha(self, linha_atual: str) -> str:
        """Verifica a próxima linha para determinar contexto"""
        # Implementação simplificada
        return ""
        
    def _processar_sumario(self, linhas: List[str]):
        """Processa o sumário do livro"""
        
        for linha in linhas[:50]:  # Limitar busca
            linha = linha.strip()
            
            # Identificar itens do sumário
            if re.match(r'^\d+\s+\w+', linha):
                # Capítulo numerado
                self.indice.append(linha)
            elif re.match(r'^[A-Z]{2,}', linha) and len(linha) < 50:
                # Seção em maiúsculas
                self.indice.append(linha)
                
    def _adicionar_elemento(self, tipo: str, conteudo: str):
        """Adiciona elemento estrutural ao documento"""
        
        if tipo == 'parte':
            nivel = '##'
        elif tipo == 'capitulo':
            nivel = '##'
        elif tipo == 'secao':
            nivel = '###'
        else:
            nivel = '####'
            
        self.conteudo_consolidado.append(f"\n{nivel} {conteudo}\n")
        
    def _adicionar_paragrafo(self, texto: str):
        """Adiciona parágrafo ao documento"""
        
        texto = texto.strip()
        if len(texto) > 50:  # Ignorar parágrafos muito curtos
            self.conteudo_consolidado.append(f"{texto}\n\n")
            
    def _adicionar_citacao(self, texto: str):
        """Adiciona citação formatada"""
        
        self.conteudo_consolidado.append(f"\n> {texto}\n\n")
        
    def _gerar_documento(self) -> str:
        """Gera o documento final consolidado"""
        
        documento = []
        
        # Cabeçalho
        documento.append(f"# {self.estrutura['titulo']}\n")
        documento.append(f"**{self.estrutura['autor']}**\n\n")
        documento.append("---\n\n")
        
        # Índice (se houver)
        if self.indice:
            documento.append("## Sumário\n\n")
            for item in self.indice[:30]:  # Limitar tamanho
                documento.append(f"- {item}\n")
            documento.append("\n---\n\n")
            
        # Conteúdo
        documento.extend(self.conteudo_consolidado)
        
        # Limpar formatação final
        texto_final = ''.join(documento)
        
        # Remover quebras excessivas
        texto_final = re.sub(r'\n{4,}', '\n\n\n', texto_final)
        
        # Garantir espaçamento antes de títulos
        texto_final = re.sub(r'([^\n])\n(#{2,4}\s)', r'\1\n\n\2', texto_final)
        
        return texto_final
        

def formatar_metodo_code(texto: str) -> str:
    """Formata especificamente o método CODE"""
    
    # Identificar e formatar o método CODE
    texto = re.sub(
        r'(C\s*[-–—]\s*Capturar)',
        r'\n**C - Capturar**',
        texto
    )
    texto = re.sub(
        r'(O\s*[-–—]\s*Organizar)',
        r'\n**O - Organizar**',
        texto
    )
    texto = re.sub(
        r'(D\s*[-–—]\s*Destilar)',
        r'\n**D - Destilar**',
        texto
    )
    texto = re.sub(
        r'(E\s*[-–—]\s*Expressar)',
        r'\n**E - Expressar**',
        texto
    )
    
    # Formatar PARA
    texto = re.sub(
        r'(P\s*[-–—]\s*Projetos)',
        r'\n**P - Projetos**',
        texto
    )
    texto = re.sub(
        r'(A\s*[-–—]\s*Áreas)',
        r'\n**A - Áreas**',
        texto
    )
    texto = re.sub(
        r'(R\s*[-–—]\s*Recursos)',
        r'\n**R - Recursos**',
        texto
    )
    texto = re.sub(
        r'(A\s*[-–—]\s*Arquivos)',
        r'\n**A - Arquivos**',
        texto
    )
    
    return texto


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Consolida transcrições de livro em documento único'
    )
    parser.add_argument(
        'diretorio',
        help='Diretório com as transcrições'
    )
    parser.add_argument(
        '-o', '--output',
        default='livro-completo.md',
        help='Arquivo de saída (padrão: livro-completo.md)'
    )
    
    args = parser.parse_args()
    
    consolidador = ConsolidadorLivro()
    
    try:
        print("🚀 Iniciando consolidação...")
        documento = consolidador.processar_diretorio(args.diretorio)
        
        # Aplicar formatações específicas
        documento = formatar_metodo_code(documento)
        
        # Salvar arquivo
        output_path = Path(args.diretorio) / args.output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(documento)
            
        # Estatísticas
        palavras = len(documento.split())
        caracteres = len(documento)
        
        print(f"\n✅ Documento consolidado criado: {output_path}")
        print(f"📊 Estatísticas:")
        print(f"   - Palavras: {palavras:,}")
        print(f"   - Caracteres: {caracteres:,}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())