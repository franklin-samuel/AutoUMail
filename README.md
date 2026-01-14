# AutoUMail

Sistema inteligente de classificação automática de emails utilizando IA.

## Sobre o Projeto

Solução desenvolvida para automatizar a triagem de emails em empresas do setor financeiro. O sistema utiliza inteligência artificial para:

- **Classificar** emails em **Produtivo** ou **Improdutivo**
- **Gerar respostas automáticas** personalizadas
- **Aceitar múltiplos formatos**: texto direto, .txt ou .pdf
- **Processar linguagem natural** (NLP) com remoção de stop words e lemmatização

## Arquitetura

O projeto segue os princípios da **Arquitetura Hexagonal**, garantindo:

- **Baixo acoplamento** entre camadas
- **Fácil substituição** de serviços (IA, NLP, etc.)
- **Testabilidade** e manutenibilidade
- **Separação clara** de responsabilidades

## Tecnologias Utilizadas

- **Backend**: Python 3.12+ | FastAPI | Uvicorn
- **Frontend**: HTML5 | **Tailwind CSS** | JavaScript
- **Template Engine**: Jinja2
- **IA**: Google Gemini 3 Flash (API gratuita)
- **NLP**: NLTK (Natural Language Toolkit)
- **Processamento de Arquivos**: PyPDF2

## Pré-requisitos

- Python 3.12 ou superior
- Conta no Google AI Studio (para API Key gratuita)

## Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/franklin-samuel/AutoUMail.git
cd AutoUMail
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` e adicione sua API Key do Gemini:

```env
GEMINI_API_KEY=sua_api_key_aqui
```

**Como obter a API Key gratuita:**
1. Acesse: https://aistudio.google.com/app/apikey
2. Crie uma nova API Key
3. Copie e cole no arquivo `.env`

### 5. Execute a aplicação

```bash
python app.web.main.py
```

A aplicação estará disponível em: **http://localhost:8000**

## Como Usar

1. **Acesse a home**: http://localhost:8000
2. **Clique em "Começar Agora"** ou acesse `/classifier`
3. **Escolha o método de entrada**:
   - **Texto**: Cole o conteúdo do email diretamente
   - **Arquivo**: Faça upload de .txt ou .pdf
4. **Clique em "Classificar Email"**
5. **Visualize o resultado**:
   - Categoria (Produtivo/Improdutivo)
   - Resposta sugerida (com botão para copiar)

## Exemplos de Uso

### Email Produtivo
```
Prezado suporte,

Gostaria de solicitar uma atualização sobre o caso #12345 
que abri na semana passada referente ao problema no sistema 
de pagamentos.

Aguardo retorno.

Atenciosamente,
João Silva
```

**Resultado esperado**: `Categoria: Produtivo` + Resposta profissional

### Email Improdutivo
```
Olá equipe!

Feliz Natal e um próspero Ano Novo para todos!
Desejo muita saúde e felicidade.

Abraços,
Maria
```

**Resultado esperado**: `Categoria: Improdutivo` + Resposta de agradecimento

## Deploy (Render)

### Fluxo Deploy:
1 - Github Actions é disparada com push na main  
2 - Sistema atualiza a imagem no Docker Hub  
3 - Dispara Trigger Render  
4 - Render faz o Re-deploy da nova imagem  


## Diferenciais do Projeto

### 1. Arquitetura Hexagonal
- **Injeção de Dependências** com FastAPI Depends
- Fácil substituição da IA (Gemini → OpenAI → Hugging Face)
- Testabilidade aprimorada
- Baixo acoplamento entre camadas

### 2. Processamento NLP
- Remoção de stop words (português)
- Limpeza e normalização de texto
- Preparação adequada para análise por IA

### 3. Interface Moderna
- Design responsivo e intuitivo com **Tailwind CSS**
- Suporte a drag-and-drop
- Feedback visual em tempo real
- Animações suaves e gradientes modernos
- 
### 4. Múltiplos Formatos
- Texto direto (textarea)
- Arquivos .txt
- Documentos .pdf

## Fluxo de Dados

```
1. Usuario → Upload/Texto
2. Controller (FastAPI) → Recebe requisição
3. Dependencies → Injeta Use Cases e Adapters
4. FileReaderAdapter → Lê arquivo (se necessário)
5. EmailClassifierAdapter (Use Case) → Orquestra processamento
6. TextProcessorAdapter → Limpa texto (NLP)
7. GeminiAdapter (AI Service) → Classifica + Gera resposta
8. Controller → Retorna JSON
9. Frontend → Exibe resultado
```

## Licença

Este projeto foi desenvolvido como case técnico para processo seletivo.

##  Autor

**Samuel Franklin**
- GitHub: [@franklin-samuel](https://github.com/franklin-samuel)
- LinkedIn: [in/samuelfranklindev](https://linkedin.com/in/samuelfranklindev)

## Agradecimentos

- AutoU pela oportunidade do desafio
- Google pela API Gemini gratuita
- Comunidade FastAPI
