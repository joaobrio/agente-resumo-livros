# Templates de Prompts para Resumo de Livros

## Template Base para Resumo Executivo

```
Você está analisando o livro "{titulo}" de {autor}.

Por favor, crie um resumo executivo seguindo esta estrutura:

1. **Visão Geral** (1 parágrafo): Apresente a tese principal e o propósito do livro
2. **Principais Argumentos** (3-5 pontos): Liste os argumentos centrais com breve explicação
3. **Evidências e Exemplos**: Destaque 2-3 exemplos mais impactantes usados pelo autor
4. **Insights Práticos**: Identifique 3-5 aplicações práticas dos conceitos
5. **Público-Alvo**: Para quem este livro é mais relevante e por quê
6. **Limitações**: Mencione 1-2 pontos fracos ou limitações da obra

Mantenha o resumo entre 500-750 palavras. Use linguagem clara e acessível.
```

## Template para Resumo por Capítulo

```
Para o capítulo {numero} - "{titulo_capitulo}" do livro "{titulo_livro}":

Crie um resumo estruturado contendo:

<chapter_summary>
  <main_idea>Ideia principal em 1-2 frases</main_idea>
  <key_points>
    - Ponto chave 1
    - Ponto chave 2
    - Ponto chave 3
  </key_points>
  <supporting_evidence>Evidência ou exemplo mais relevante</supporting_evidence>
  <connection>Como este capítulo se conecta com o anterior/próximo</connection>
</chapter_summary>

Limite: 150 palavras por capítulo.
```

## Template para Análise Temática

```
Analise o livro "{titulo}" identificando seus temas principais.

Para cada tema encontrado, forneça:

<theme_analysis>
  <theme name="{nome_do_tema}">
    <description>Descrição do tema em 2-3 frases</description>
    <occurrences>Capítulos/seções onde aparece</occurrences>
    <development>Como o tema evolui ao longo do livro</development>
    <significance>Por que este tema é importante para a mensagem geral</significance>
    <quotes>1-2 citações que exemplificam o tema</quotes>
  </theme>
</theme_analysis>

Identifique entre 3-5 temas principais.
```

## Template para Extração de Conceitos

```
Extraia os conceitos-chave do livro "{titulo}".

Para cada conceito:

<concept>
  <n>{Nome do Conceito}</n>
  <definition>Definição clara e concisa</definition>
  <context>Contexto onde é introduzido</context>
  <examples>2-3 exemplos do livro</examples>
  <related_concepts>Outros conceitos relacionados</related_concepts>
  <practical_application>Como aplicar na prática</practical_application>
</concept>

Foque nos 5-10 conceitos mais importantes.
```

## Template para Livros Técnicos

```
Analisando o livro técnico "{titulo}":

1. **Pré-requisitos Técnicos**
   - Conhecimentos necessários
   - Tecnologias/ferramentas mencionadas

2. **Conceitos Técnicos Principais**
   - Liste com definições precisas
   - Inclua complexidade (básico/intermediário/avançado)

3. **Implementações e Código**
   - Principais padrões/algoritmos apresentados
   - Linguagens de programação usadas
   - Complexidade das implementações

4. **Casos de Uso**
   - Aplicações práticas demonstradas
   - Problemas resolvidos

5. **Recursos Adicionais**
   - Links, repositórios, ferramentas mencionadas

Mantenha precisão técnica e inclua snippets de código quando relevante.
```

## Template para Livros de Ficção

```
Para a obra de ficção "{titulo}" de {autor}:

<fiction_analysis>
  <plot_summary>
    Resumo da trama principal sem spoilers excessivos (200 palavras)
  </plot_summary>
  
  <characters>
    <protagonist>
      Nome, motivações, desenvolvimento
    </protagonist>
    <supporting>
      Personagens secundários importantes
    </supporting>
  </characters>
  
  <themes>
    Temas literários explorados
  </themes>
  
  <literary_devices>
    Técnicas narrativas utilizadas
  </literary_devices>
  
  <setting>
    Tempo, lugar, contexto
  </setting>
  
  <style>
    Estilo de escrita e tom
  </style>
</fiction_analysis>
```

## Template para Comparação de Livros

```
Compare os livros:
1. "{titulo1}" de {autor1}
2. "{titulo2}" de {autor2}

Estruture a comparação assim:

<comparison>
  <similarities>
    - Temas em comum
    - Abordagens similares
    - Públicos sobrepostos
  </similarities>
  
  <differences>
    - Perspectivas contrastantes
    - Metodologias diferentes
    - Conclusões divergentes
  </differences>
  
  <complementarity>
    Como os livros se complementam
  </complementarity>
  
  <recommendation>
    Qual ler primeiro e por quê
    Situações onde cada um é mais apropriado
  </recommendation>
</comparison>
```

## Template para Criação de Flashcards

```
Crie flashcards de estudo para o livro "{titulo}".

Formato para cada card:

<flashcard>
  <id>{numero}</id>
  <difficulty>{facil|medio|dificil}</difficulty>
  <category>{categoria}</category>
  <front>{Pergunta ou prompt}</front>
  <back>{Resposta completa mas concisa}</back>
  <hint>{Dica opcional}</hint>
  <page_ref>{Página de referência}</page_ref>
</flashcard>

Crie 20-30 flashcards cobrindo:
- Conceitos principais (40%)
- Exemplos e aplicações (30%)
- Detalhes importantes (20%)
- Conexões entre ideias (10%)
```

## Template para Plano de Estudo

```
Crie um plano de estudo para o livro "{titulo}" considerando:
- Tempo disponível: {X semanas}
- Objetivo: {objetivo_especifico}
- Nível de conhecimento prévio: {iniciante|intermediario|avancado}

<study_plan>
  <week number="{numero}">
    <reading>Capítulos a ler</reading>
    <focus>Conceitos principais para focar</focus>
    <exercises>Exercícios práticos</exercises>
    <review>Material para revisar</review>
    <milestone>O que deve ser alcançado</milestone>
  </week>
</study_plan>

Inclua:
- Divisão realista de leitura
- Pontos de revisão
- Exercícios práticos
- Avaliações de progresso
```

## Template para Meta-Prompt (Melhorar Resumos)

```
Avalie o resumo abaixo do livro "{titulo}" e sugira melhorias:

[RESUMO ATUAL]

Por favor, analise:
1. **Completude**: Algum aspecto importante foi omitido?
2. **Clareza**: Há partes confusas ou mal explicadas?
3. **Precisão**: Existem erros ou má interpretações?
4. **Utilidade**: O resumo é prático e aplicável?
5. **Estrutura**: A organização poderia ser melhorada?

Forneça:
- Pontos fortes do resumo atual
- Áreas específicas para melhoria
- Versão revisada das seções problemáticas
- Sugestões de informações adicionais
```

## Dicas para Uso dos Templates

1. **Adaptação**: Sempre adapte o template ao tipo específico de livro
2. **Contexto**: Forneça contexto adicional quando necessário
3. **Exemplos**: Inclua exemplos do próprio livro quando possível
4. **Linguagem**: Ajuste o nível de linguagem ao público-alvo
5. **Foco**: Priorize informações mais relevantes para o objetivo do usuário

## Combinação de Templates

Para análises completas, combine múltiplos templates:

```
1. Comece com o Template Base para visão geral
2. Use Template por Capítulo para detalhamento
3. Aplique Template de Conceitos para aprofundamento
4. Finalize com Template de Flashcards para estudo
```