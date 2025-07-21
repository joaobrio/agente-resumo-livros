#!/usr/bin/env python3
"""
Formatador de Transcrições para Markdown
Aplica boas práticas de formatação nas transcrições de livros
"""

import re
import os
from pathlib import Path
from typing import List, Tuple

class TranscricaoFormatter:
    """Formata transcrições seguindo boas práticas de Markdown"""
    
    def __init__(self):
        self.capitulos = []
        self.partes = []
        self.secoes = []
        
    def detectar_hierarquia(self, linha: str) -> Tuple[str, str]:
        """
        Detecta o tipo de hierarquia do texto
        Retorna: (tipo, texto_limpo)
        """
        linha = linha.strip()
        
        # Padrões de detecção
        patterns = {
            'parte': r'^PARTE\s+(UM|DOIS|TRÊS|QUATRO|CINCO|I|II|III|IV|V)',
            'capitulo': r'^Capítulo\s+\d+',
            'secao_maiuscula': r'^[A-Z][A-Z\s]+$',  # Todo em maiúsculas
            'citacao': r'^["""].*["""].*–',
            'lista_numerada': r'^\d+[\.\)]\s+',
            'lista_bullet': r'^[•·\-\*]\s+',
            'paragrafo_indentado': r'^[\s\t]+\S',
        }
        
        for tipo, pattern in patterns.items():
            if re.match(pattern, linha):
                return tipo, linha
                
        # Se não corresponder a nenhum padrão
        if linha and not linha.startswith('---') and not linha.startswith('##'):
            return 'paragrafo', linha
            
        return 'outro', linha
        
    def formatar_linha(self, linha: str, tipo: str) -> str:
        """Formata linha baseado no tipo detectado"""
        
        if tipo == 'parte':
            # PARTE UM -> ## PARTE UM
            return f"\n## {linha}\n"
            
        elif tipo == 'capitulo':
            # Capítulo 1 -> ## Capítulo 1
            return f"\n## {linha}\n"
            
        elif tipo == 'secao_maiuscula' and len(linha) > 3:
            # INTRODUÇÃO -> ### Introdução
            return f"\n### {linha.title()}\n"
            
        elif tipo == 'citacao':
            # Formatar citações com > 
            return f"\n> {linha}\n"
            
        elif tipo == 'lista_numerada':
            # Manter listas numeradas
            return linha
            
        elif tipo == 'lista_bullet':
            # Converter para formato padrão de lista
            linha_limpa = re.sub(r'^[•·\-\*]\s+', '- ', linha)
            return linha_limpa
            
        elif tipo == 'paragrafo':
            # Parágrafos normais
            return linha
            
        return linha
        
    def processar_arquivo(self, caminho_entrada: str, caminho_saida: str):
        """Processa um arquivo de transcrição"""
        
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        linhas_formatadas = []
        em_bloco_codigo = False
        paragrafo_buffer = []
        
        for i, linha in enumerate(linhas):
            linha_stripped = linha.strip()
            
            # Ignorar separadores de página
            if linha_stripped == '---' or linha_stripped.startswith('## Página'):
                continue
                
            # Detectar blocos de código
            if linha_stripped.startswith('```'):
                em_bloco_codigo = not em_bloco_codigo
                linhas_formatadas.append(linha)
                continue
                
            if em_bloco_codigo:
                linhas_formatadas.append(linha)
                continue
                
            # Processar linha normal
            tipo, texto = self.detectar_hierarquia(linha_stripped)
            
            # Se for título/seção, processar parágrafo acumulado primeiro
            if tipo in ['parte', 'capitulo', 'secao_maiuscula'] and paragrafo_buffer:
                paragrafo_completo = ' '.join(paragrafo_buffer)
                if paragrafo_completo:
                    linhas_formatadas.append(paragrafo_completo + '\n\n')
                paragrafo_buffer = []
                
            # Processar linha atual
            if tipo == 'paragrafo' and texto:
                # Acumular parágrafos quebrados
                paragrafo_buffer.append(texto)
            else:
                # Processar parágrafo acumulado
                if paragrafo_buffer:
                    paragrafo_completo = ' '.join(paragrafo_buffer)
                    if paragrafo_completo:
                        linhas_formatadas.append(paragrafo_completo + '\n\n')
                    paragrafo_buffer = []
                    
                # Adicionar linha formatada
                if texto:
                    linha_formatada = self.formatar_linha(texto, tipo)
                    linhas_formatadas.append(linha_formatada)
                    
        # Processar último parágrafo se houver
        if paragrafo_buffer:
            paragrafo_completo = ' '.join(paragrafo_buffer)
            if paragrafo_completo:
                linhas_formatadas.append(paragrafo_completo + '\n\n')
                
        # Limpar espaços extras e escrever arquivo
        conteudo_final = ''.join(linhas_formatadas)
        
        # Limpar múltiplas quebras de linha
        conteudo_final = re.sub(r'\n{4,}', '\n\n\n', conteudo_final)
        
        # Adicionar metadados no início
        metadados = self.gerar_metadados(caminho_entrada)
        conteudo_final = metadados + conteudo_final
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo_final)
            
        print(f"✅ Arquivo formatado: {caminho_saida}")
        
    def gerar_metadados(self, caminho_arquivo: str) -> str:
        """Gera cabeçalho com metadados do arquivo"""
        
        nome_arquivo = Path(caminho_arquivo).stem
        paginas_match = re.search(r'paginas-(\d+)-(\d+)', nome_arquivo)
        
        if paginas_match:
            inicio, fim = paginas_match.groups()
            return f"""# Transcrição Formatada - Páginas {inicio} a {fim}

> **Arquivo original**: {Path(caminho_arquivo).name}  
> **Processado com**: formatar_transcricoes.py  
> **Data**: {Path(caminho_arquivo).stat().st_mtime}

---

"""
        return ""
        
    def processar_diretorio(self, diretorio: str):
        """Processa todos os arquivos de transcrição em um diretório"""
        
        dir_path = Path(diretorio)
        arquivos_transcricao = list(dir_path.glob('transcricao-paginas-*.md'))
        
        if not arquivos_transcricao:
            print("❌ Nenhum arquivo de transcrição encontrado")
            return
            
        print(f"📚 Encontrados {len(arquivos_transcricao)} arquivos para processar")
        
        # Criar subdiretório para arquivos formatados
        output_dir = dir_path / 'formatadas'
        output_dir.mkdir(exist_ok=True)
        
        for arquivo in sorted(arquivos_transcricao):
            nome_saida = arquivo.stem + '-formatado.md'
            caminho_saida = output_dir / nome_saida
            
            print(f"\n📄 Processando: {arquivo.name}")
            self.processar_arquivo(str(arquivo), str(caminho_saida))
            
        print(f"\n✨ Processamento concluído! Arquivos salvos em: {output_dir}")
        

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
    parser.add_argument(
        '-o', '--output',
        help='Arquivo ou diretório de saída (padrão: adiciona "-formatado" ao nome)'
    )
    
    args = parser.parse_args()
    
    formatter = TranscricaoFormatter()
    
    if os.path.isdir(args.caminho):
        formatter.processar_diretorio(args.caminho)
    elif os.path.isfile(args.caminho):
        if args.output:
            output_path = args.output
        else:
            base_name = Path(args.caminho).stem
            output_path = Path(args.caminho).parent / f"{base_name}-formatado.md"
            
        formatter.processar_arquivo(args.caminho, str(output_path))
    else:
        print(f"❌ Caminho não encontrado: {args.caminho}")
        

if __name__ == "__main__":
    main()