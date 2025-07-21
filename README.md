# 📚 Agente de Resumo de Livros

> 🤖 Sistema automatizado para processar transcrições e gerar resumos estruturados de livros usando Claude AI

## 🎯 Visão Geral

Este projeto automatiza o processo de transformar transcrições brutas de livros em resumos bem estruturados e formatados. Ideal para processar conteúdo do Kindle, audiolivros transcritos ou qualquer texto longo que precise ser resumido de forma inteligente.

## ✨ Funcionalidades

- 📄 **Processamento de Transcrições**: Limpa e organiza transcrições brutas
- 🧩 **Detecção de Capítulos**: Identifica automaticamente divisões de capítulos
- 🤖 **Integração com Claude**: Usa IA para gerar resumos contextualizados
- 📊 **Múltiplos Formatos**: Suporta saída em Markdown, texto plano e JSON
- 🔄 **Processamento em Lote**: Processa múltiplos capítulos automaticamente
- 💾 **Cache Inteligente**: Evita reprocessamento desnecessário

## 📁 Estrutura do Projeto

```
agente-resumo-livros/
├── CLAUDE.md              # Contexto e instruções para o Claude
├── README.md              # Este arquivo
├── .gitignore            # Arquivos ignorados pelo Git
├── main.py               # Script principal
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de configuração
│
├── resumos/             # Resumos processados
│   ├── formatados/      # Versões finais
│   └── versoes_antigas/ # Versões anteriores
│
├── configuracoes/       # Arquivos de configuração
├── templates/           # Templates de formatação
├── scripts/            # Scripts auxiliares
└── exemplos/           # Exemplos de uso
```

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8+
- Conta na Anthropic (Claude API)
- Transcrições em formato texto

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/joaobrio/agente-resumo-livros.git
cd agente-resumo-livros
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com sua API key do Claude
```

### Uso Básico

```bash
# Processar uma transcrição
python main.py processar "caminho/para/transcricao.txt"

# Resumir capítulos específicos
python main.py resumir --capitulos 1-5

# Gerar resumo completo
python main.py resumo-completo
```

## 📝 Exemplos

### Entrada (Transcrição Bruta)
```text
Capítulo 1 Este é o início do livro onde...
```

### Saída (Resumo Formatado)
```markdown
# Capítulo 1: Introdução

## Resumo
Este capítulo apresenta os conceitos fundamentais...

## Pontos-Chave
- Conceito A explicado
- Importância do tema B
- Conexão com C

## Citações Relevantes
> "A melhor forma de prever o futuro é criá-lo"
```

## 🛠️ Desenvolvimento

### Estrutura do Código

- `main.py`: Orquestra todo o processo
- `processors/`: Módulos de processamento
- `utils/`: Funções auxiliares
- `templates/`: Templates de formatação

### Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Add nova feature'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**João Rovere**
- GitHub: [@joaobrio](https://github.com/joaobrio)

## 🙏 Agradecimentos

- Claude AI por possibilitar resumos inteligentes
- Comunidade open source pelos exemplos e inspiração

---

⭐ Se este projeto foi útil, considere dar uma estrela!
