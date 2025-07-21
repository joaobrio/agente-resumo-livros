# Agente Resumo Livros - Contexto para Claude Code

## 🎯 Objetivo do Projeto
Sistema inteligente para processar, transcrever e criar resumos estruturados de livros usando IA. Foco em metodologias como CODE (Capturar, Organizar, Destilar, Expressar) e técnicas de aprendizagem ativa.

## 📚 Status Atual do Projeto

### ✅ Livro Completado: "Criando um Segundo Cérebro" (Tiago Forte)
- **Páginas processadas**: 1-280 (livro completo)
- **Versões finais**: Organizadas em `resumos/criando-segundo-cerebro/versoes-finais/`
- **Estrutura hierárquica**: Markdown com headers, citações e listas formatadas corretamente
- **Capítulos 4-7**: Formatados individualmente com máxima qualidade

### 📁 Estrutura de Versões:
- **USAR**: `versoes-finais/` - Versões corretas e atuais (8 arquivos)
- **REVISAR**: `versoes-para-revisao/` - Versões obsoletas para exclusão (22 arquivos)

## 🛠️ Comandos Essenciais

### Para Linting/Verificação:
```bash
# Verificar se há comandos específicos no package.json ou README
npm run lint        # Se disponível
npm run typecheck   # Se disponível  
python -m ruff .    # Para Python
```

### Para Commits:
- NUNCA commit automaticamente - só quando explicitamente solicitado
- Usar formato padrão com 🤖 Generated with [Claude Code]

## 🔄 Processo de Formatação de Capítulos

### 1. Identificar Capítulos:
```bash
grep -n "^## Capítulo\|^# Capítulo" arquivo-transcricao.md
```

### 2. Extrair Conteúdo por Capítulo:
- Usar `sed` ou `Read` tool para extrair seções específicas
- Manter estrutura original do livro

### 3. Aplicar Formatação Hierárquica:
- **H1**: Parte do livro
- **H2**: Capítulos 
- **H3**: Seções principais
- **H4**: Subseções
- **Citações**: `> "texto"`
- **Listas**: Numeradas ou bullet points
- **Ênfase**: `**termos importantes**`

### 4. Nomenclatura de Arquivos:
```
transcricao-capitulo-X-formatado.md
transcricao-paginas-X-Y-revisada.md (para seções já revisadas)
```

## 📋 Workflow Típico para Novos Livros

### Fase 1 - Preparação:
1. Criar pasta em `resumos/nome-livro/`
2. Transcrever PDFs para Markdown usando `scripts/`
3. Dividir por seções lógicas (introdução, partes, capítulos)

### Fase 2 - Formatação:
1. Aplicar hierarquia Markdown correta
2. Formatar citações e listas  
3. Dividir capítulos longos individualmente
4. Criar versões revisadas quando necessário

### Fase 3 - Organização:
1. Criar `versoes-finais/` com arquivos prontos
2. Mover obsoletas para `versoes-para-revisao/`
3. Documentar com README em cada pasta

### Fase 4 - Resumos (Opcional):
1. Gerar resumo executivo
2. Criar flashcards e mapas mentais
3. Desenvolver templates práticos

## 🎯 Próximos Passos Sugeridos

### Imediato:
1. **Revisar versões obsoletas** em `versoes-para-revisao/` e excluir se corretas
2. **Escolher próximo livro** para processar
3. **Formatar capítulos restantes** se houver (cap. 1-3, 8-10, etc.)

### Melhorias do Sistema:
1. **Script automatizado** para formatação hierárquica
2. **Template padrão** para novos livros
3. **Validação de qualidade** das transcrições

## 💡 Dicas Importantes

### Ao Continuar Formatação:
- Sempre verificar versões existentes primeiro
- Usar `TodoWrite` para rastrear progresso
- Processar capítulo por capítulo para manter foco
- Confirmar cada etapa com o usuário

### Padrão de Qualidade:
- Headers hierárquicos consistentes
- Citações sempre com `>` 
- Listas bem estruturadas
- Termos importantes em **negrito**
- Quebras de linha adequadas entre seções

### Organização:
- Versões finais sempre em pasta separada
- README explicativo em cada pasta
- Nomenclatura consistente de arquivos
- Backup de versões antes de excluir

---

**Última atualização**: 21 de julho de 2025
**Status do projeto**: Pronto para próximo livro ou melhorias do sistema