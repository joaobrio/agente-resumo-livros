#!/usr/bin/env python3
"""
Formatador Avançado de Transcrições para Markdown v2
Aplica boas práticas de formatação nas transcrições de livros
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict
import unicodedata

class TranscricaoFormatterV2:
    """Formata transcrições seguindo boas práticas de Markdown"""
    
    def __init__(self):
        self.estrutura_livro = {
            'titulo': '',
            'autor': '',
            'partes': {},
            'capitulos': {},
            'secoes': {}
        }
        self.pagina_atual = 0
        
    def limpar_texto(self, texto: str) -> str:
        """Remove caracteres indesejados e normaliza espaços"""
        # Normalizar unicode
        texto = unicodedata.normalize('NFKD', texto)
        
        # Remover múltiplos espaços
        texto = re.sub(r'\s+', ' ', texto)
        
        # Remover espaços no início e fim
        texto = texto.strip()
        
        return texto
        
    def detectar_tipo_conteudo(self, linha: str) -> Tuple[str, str]:
        """
        Detecta o tipo de conteúdo da linha
        Retorna: (tipo, texto_limpo)
        """
        linha_limpa = self.limpar_texto(linha)
        
        # Ignorar linhas vazias ou muito curtas
        if not linha_limpa or len(linha_limpa) < 2:
            return 'vazio', ''
            
        # Padrões específicos do livro
        patterns = {
            # Estrutura principal
            'parte': (r'^PARTE\s+(UM|DOIS|TRÊS|QUATRO|CINCO|I|II|III|IV|V)', '##'),
            'titulo_parte': (r'^(A base|O método|A mudança)', '###'),
            'subtitulo_parte': (r'^(Entendendo|As quatro|Fazendo)', '####'),
            
            # Capítulos
            'capitulo': (r'^Capítulo\s+\d+', '##'),
            'titulo_capitulo': (r'^(Onde tudo começou|O que é um Segundo Cérebro|Como funciona)', '###'),
            
            # Seções
            'secao': (r'^[A-Z][a-z\s]+:$', '###'),
            'subsecao': (r'^[A-Z][a-z\s]+\s+[a-z]+.*:$', '####'),
            
            # Elementos especiais
            'citacao': (r'^[""].*[""].*[–—]\s*\w+', '>'),
            'nota_rodape': (r'^\*\s+.+', '_Nota:_'),
            'lista_numerada': (r'^\d+[\.\)]\s+', ''),
            'lista_bullet': (r'^[•·▪▫◦‣⁃]\s+', '-'),
            
            # Metadados
            'sumario': (r'^SUMÁRIO$', '## Sumário'),
            'introducao': (r'^INTRODUÇÃO$|^Introdução$', '## Introdução'),
            'referencias': (r'^(Notas|Referências|Bibliografia)$', '## $1'),
        }
        
        for tipo, (pattern, prefixo) in patterns.items():
            match = re.match(pattern, linha_limpa, re.IGNORECASE)
            if match:
                if prefixo and not prefixo.startswith('$'):
                    return tipo, f"{prefixo} {linha_limpa}"
                elif prefixo.startswith('$'):
                    # Substituição com grupo capturado
                    return tipo, re.sub(pattern, prefixo, linha_limpa, flags=re.IGNORECASE)
                else:
                    return tipo, linha_limpa
                    
        # Se não corresponder a nenhum padrão específico
        if re.match(r'^[A-Z\s]+$', linha_limpa) and len(linha_limpa) > 5:
            # Provavelmente um título em maiúsculas
            return 'titulo_maiusculo', f"### {linha_limpa.title()}"
            
        # Parágrafo normal
        return 'paragrafo', linha_limpa
        
    def processar_paginas(self, linhas: List[str]) -> List[str]:
        """Processa as linhas removendo marcadores de página e organizando conteúdo"""
        
        conteudo_processado = []
        buffer_paragrafo = []
        em_citacao = False
        pulando_cabecalho = True
        
        for i, linha in enumerate(linhas):
            # Detectar e pular páginas iniciais (capa, ficha catalográfica, etc.)
            if pulando_cabecalho:
                if any(palavra in linha.upper() for palavra in ['SUMÁRIO', 'INTRODUÇÃO', 'CAPÍTULO']):
                    pulando_cabecalho = False
                elif self.pagina_atual < 10:
                    continue
                    
            # Ignorar marcadores de página
            if linha.strip().startswith('## Página') or linha.strip() == '---':
                self.pagina_atual += 1
                continue
                
            # Ignorar cabeçalhos/rodapés repetitivos
            if self.eh_cabecalho_rodape(linha):
                continue
                
            tipo, texto_formatado = self.detectar_tipo_conteudo(linha)
            
            # Processar buffer de parágrafo quando encontrar novo elemento estrutural
            if tipo in ['parte', 'capitulo', 'secao', 'titulo_maiusculo'] and buffer_paragrafo:
                paragrafo_completo = ' '.join(buffer_paragrafo)
                if len(paragrafo_completo) > 20:  # Ignorar parágrafos muito curtos
                    conteudo_processado.append(paragrafo_completo + '\n')
                buffer_paragrafo = []
                # Adicionar linha em branco antes de títulos
                conteudo_processado.append('\n')
                
            # Processar conteúdo baseado no tipo
            if tipo == 'vazio':
                if buffer_paragrafo:
                    paragrafo_completo = ' '.join(buffer_paragrafo)
                    if len(paragrafo_completo) > 20:
                        conteudo_processado.append(paragrafo_completo + '\n\n')
                    buffer_paragrafo = []
            elif tipo == 'paragrafo' and texto_formatado:
                buffer_paragrafo.append(texto_formatado)
            elif tipo == 'citacao':
                if buffer_paragrafo:
                    paragrafo_completo = ' '.join(buffer_paragrafo)
                    if paragrafo_completo:
                        conteudo_processado.append(paragrafo_completo + '\n\n')
                    buffer_paragrafo = []
                conteudo_processado.append(f"\n{texto_formatado}\n\n")
            else:
                if texto_formatado:
                    conteudo_processado.append(texto_formatado + '\n')
                    
        # Processar último parágrafo
        if buffer_paragrafo:
            paragrafo_completo = ' '.join(buffer_paragrafo)
            if len(paragrafo_completo) > 20:
                conteudo_processado.append(paragrafo_completo + '\n')
                
        return conteudo_processado
        
    def eh_cabecalho_rodape(self, linha: str) -> bool:
        """Detecta se a linha é um cabeçalho ou rodapé repetitivo"""
        linha_limpa = linha.strip().lower()
        
        padroes_ignorar = [
            r'^\d+$',  # Apenas números (páginas)
            r'^criando um segundo cérebro',  # Título do livro repetido
            r'^tiago forte',  # Nome do autor repetido
            r'copyright',
            r'todos os direitos',
            r'^capítulo \d+$',  # Apenas "Capítulo X" sem título
        ]
        
        for padrao in padroes_ignorar:
            if re.search(padrao, linha_limpa):
                return True
                
        return False
        
    def criar_indice(self, conteudo: List[str]) -> str:
        """Cria um índice/sumário baseado nos títulos encontrados"""
        indice = ["## Índice\n"]
        
        for linha in conteudo:
            if linha.startswith('## ') and not linha.startswith('## Índice'):
                # Parte ou Capítulo
                titulo = linha.replace('##', '').strip()
                indice.append(f"- **{titulo}**")
            elif linha.startswith('### '):
                # Seção
                titulo = linha.replace('###', '').strip()
                indice.append(f"  - {titulo}")
                
        if len(indice) > 1:
            return '\n'.join(indice) + '\n\n---\n\n'
        return ''
        
    def formatar_arquivo(self, caminho_entrada: str, caminho_saida: str):
        """Processa e formata um arquivo de transcrição"""
        
        print(f"📖 Lendo arquivo: {Path(caminho_entrada).name}")
        
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        # Processar conteúdo
        conteudo_processado = self.processar_paginas(linhas)
        
        # Criar índice se houver estrutura suficiente
        indice = self.criar_indice(conteudo_processado)
        
        # Montar documento final
        documento_final = []
        
        # Adicionar cabeçalho
        documento_final.append(self.gerar_cabecalho(caminho_entrada))
        
        # Adicionar índice se existir
        if indice:
            documento_final.append(indice)
            
        # Adicionar conteúdo
        documento_final.extend(conteudo_processado)
        
        # Limpar formatação final
        texto_final = ''.join(documento_final)
        
        # Remover múltiplas quebras de linha (máximo 2)
        texto_final = re.sub(r'\n{4,}', '\n\n\n', texto_final)
        
        # Garantir espaço adequado antes de títulos
        texto_final = re.sub(r'([^\n])\n(#{1,4}\s)', r'\1\n\n\2', texto_final)
        
        # Salvar arquivo formatado
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(texto_final)
            
        print(f"✅ Arquivo formatado salvo: {Path(caminho_saida).name}")
        
        # Estatísticas
        self.exibir_estatisticas(texto_final)
        
    def gerar_cabecalho(self, caminho_arquivo: str) -> str:
        """Gera cabeçalho com metadados do arquivo"""
        
        nome_arquivo = Path(caminho_arquivo).stem
        paginas_match = re.search(r'paginas-(\d+)-(\d+)', nome_arquivo)
        
        cabecalho = [
            "# Criando um Segundo Cérebro - Tiago Forte\n",
            "*Transcrição Formatada*\n\n"
        ]
        
        if paginas_match:
            inicio, fim = paginas_match.groups()
            total = int(fim) - int(inicio) + 1
            cabecalho.append(f"**Páginas**: {inicio} a {fim} (Total: {total} páginas)\n\n")
            
        cabecalho.append("---\n\n")
        
        return ''.join(cabecalho)
        
    def exibir_estatisticas(self, texto: str):
        """Exibe estatísticas sobre o documento processado"""
        
        linhas = texto.split('\n')
        palavras = len(texto.split())
        caracteres = len(texto)
        
        # Contar elementos estruturais
        partes = len([l for l in linhas if l.startswith('## PARTE')])
        capitulos = len([l for l in linhas if l.startswith('## Capítulo')])
        secoes = len([l for l in linhas if l.startswith('###')])
        
        print(f"\n📊 Estatísticas:")
        print(f"   - Palavras: {palavras:,}")
        print(f"   - Caracteres: {caracteres:,}")
        print(f"   - Partes: {partes}")
        print(f"   - Capítulos: {capitulos}")
        print(f"   - Seções: {secoes}")
        
    def processar_diretorio(self, diretorio: str):
        """Processa todos os arquivos de transcrição em um diretório"""
        
        dir_path = Path(diretorio)
        arquivos_transcricao = sorted(dir_path.glob('transcricao-paginas-*.md'))
        
        if not arquivos_transcricao:
            print("❌ Nenhum arquivo de transcrição encontrado")
            return
            
        print(f"\n📚 Processando {len(arquivos_transcricao)} arquivos de transcrição...\n")
        
        # Criar diretório de saída
        output_dir = dir_path / 'formatadas-v2'
        output_dir.mkdir(exist_ok=True)
        
        for arquivo in arquivos_transcricao:
            nome_saida = arquivo.stem.replace('transcricao-', '') + '-formatado.md'
            caminho_saida = output_dir / nome_saida
            
            self.formatar_arquivo(str(arquivo), str(caminho_saida))
            print()  # Linha em branco entre arquivos
            
        print(f"✨ Processamento concluído!")
        print(f"📁 Arquivos salvos em: {output_dir}")
        

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Formata transcrições de livros seguindo boas práticas de Markdown'
    )
    parser.add_argument(
        'caminho',
        help='Arquivo ou diretório para processar'
    )
    
    args = parser.parse_args()
    
    formatter = TranscricaoFormatterV2()
    
    if os.path.isdir(args.caminho):
        formatter.processar_diretorio(args.caminho)
    elif os.path.isfile(args.caminho):
        base_name = Path(args.caminho).stem
        output_path = Path(args.caminho).parent / f"{base_name}-formatado-v2.md"
        formatter.formatar_arquivo(args.caminho, str(output_path))
    else:
        print(f"❌ Caminho não encontrado: {args.caminho}")
        

if __name__ == "__main__":
    main()