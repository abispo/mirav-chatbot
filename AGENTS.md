# Projeto

Sistema de chatbot com integração LLM responsável por:

- processamento conversacional
- gerenciamento de contexto
- geração de respostas
- integração com providers de IA
- busca contextual
- exposição de endpoints HTTP

O projeto utiliza FastAPI/Python e possui arquitetura simples baseada em serviços.

---

# Stack

- Linguagem: Python 3.13
- Framework HTTP: FastAPI
- Servidor ASGI: Uvicorn
- LLM Provider: DeepSeek/OpenAI compatível
- Gerenciador de dependências: uv
- Containerização: Docker

---

# Estrutura do projeto

```txt
app/
├── core/
├── db/
├── prompts/
├── routes/
└── services/
```

## app/core

Responsável por:

- configurações
- segurança
- logging
- variáveis de ambiente
- inicialização compartilhada

Arquivos:

- config.py → configurações globais
- logging.py → logging centralizado
- security.py → autenticação/autorização

---

## app/db

Responsável pela camada de banco de dados.

Arquivos:

- connection.py → conexão e gerenciamento do banco

Regras:

- evitar queries fora desta camada
- centralizar conexão
- usar abstrações/repositories futuramente

---

## app/prompts

Responsável pelos prompts utilizados pelos agentes.

Arquivos:

- system_prompt.py → comportamento principal do agente
- user_prompt.py → estruturação de prompts de usuário

Regras:

- evitar prompts hardcoded em services ou routes
- prompts devem ser reutilizáveis
- prompts devem ser versionáveis

---

## app/routes

Responsável pelos endpoints HTTP.

Arquivos:

- chat.py → endpoint principal do chatbot

Regras:

- routes não devem conter lógica de negócio
- routes apenas:
  - validam entrada
  - chamam services
  - retornam respostas

---

## app/services

Responsável pela lógica principal do sistema.

Arquivos:

- llm.py → integração com providers de IA
- search.py → recuperação/busca contextual

Regras:

- services devem ser desacoplados
- evitar lógica diretamente nas rotas
- providers devem ser abstraídos
- preparar estrutura para múltiplos providers

---

# Fluxo principal

1. Usuário envia mensagem
2. Endpoint recebe payload
3. Sistema monta contexto
4. Prompt é estruturado
5. LLM é chamado
6. Resposta é retornada

---

# Diretrizes arquiteturais

## Separação de responsabilidades

- routes → transporte HTTP
- services → lógica de negócio
- prompts → engenharia de prompt
- core → infraestrutura compartilhada
- db → persistência

---

# Providers de IA

O sistema deve permitir múltiplos providers.

Nunca acoplar diretamente:

- DeepSeek
- OpenAI
- Anthropic

Criar abstrações quando necessário.

Exemplo:

- ChatProvider
- EmbeddingProvider
- SearchProvider

---

# Contexto conversacional

O sistema deve ser preparado para:

- histórico de conversa
- memória persistente
- sumarização
- recuperação semântica
- limitação de tokens

Evitar crescimento infinito de contexto.

---

# Logging

Todo fluxo crítico deve possuir logging.

Registrar:

- chamadas de provider
- erros
- timeouts
- falhas de parsing
- falhas de busca

Nunca registrar:

- secrets
- tokens
- chaves privadas

---

# Segurança

- nunca expor chaves em código
- usar variáveis de ambiente
- validar payloads externos
- sanitizar entradas
- evitar prompt injection quando possível

## Estado atual

Atualmente a API principal de mensagens não possui autenticação.

Os endpoints estão acessíveis apenas internamente na infraestrutura atual.

## Direção futura

O sistema deve futuramente implementar:

- autenticação via API Key
- assinatura de webhook
- rate limiting
- validação de origem
- proteção contra replay
- autenticação entre serviços

## Regras importantes

- nunca assumir que endpoints públicos são seguros
- novos endpoints devem ser preparados para autenticação
- evitar lógica acoplada ao mecanismo de autenticação
- preferir middleware para autenticação/autorização

## Integrações internas

Atualmente o chatbot recebe mensagens apenas de:

- workflows n8n

## Toda comunicação futura entre serviços deve considerar autenticação mútua.

# Convenções de código

- código em inglês
- comentários em português
- funções pequenas
- evitar arquivos gigantes
- evitar lógica duplicada
- priorizar legibilidade
- tipar funções quando possível

---

# Regras importantes

- não colocar lógica de negócio em routes
- não colocar prompts dentro de services
- evitar acoplamento entre providers
- evitar variáveis globais mutáveis
- centralizar configurações em core/config.py

---

# Melhorias futuras esperadas

O sistema deve ser preparado para:

- memória persistente
- RAG
- embeddings
- vector database
- múltiplos agentes
- tool calling
- filas assíncronas
- streaming de resposta
- observabilidade

---

# Estrutura recomendada para evolução

```txt
app/
├── agents/
├── core/
├── db/
├── memory/
├── prompts/
├── repositories/
├── routes/
├── schemas/
├── services/
├── tools/
└── workers/
```

---

# Diretrizes para IA

Ao gerar código:

- manter simplicidade
- evitar overengineering
- sugerir modularização quando relevante
- evitar dependências desnecessárias
- priorizar desacoplamento
- considerar escalabilidade futura
- manter compatibilidade com FastAPI
- considerar uso futuro com WhatsApp/n8n

---

# Documentação adicional recomendada

Criar futuramente:

```txt
docs/
├── architecture.md
├── flows.md
├── prompts.md
├── providers.md
├── memory.md
└── deployment.md
```

---

# Observações sobre o projeto atual

O projeto atualmente possui arquitetura enxuta e simples.

Pontos positivos:

- separação inicial entre routes/services/prompts
- organização limpa
- baixo acoplamento inicial
- boa base para evolução

Pontos recomendados para evolução:

- adicionar schemas DTO/Pydantic separados
- adicionar camada repositories
- criar abstrações de provider
- criar sistema de memória conversacional
- criar sistema de agentes especializados
- adicionar observabilidade estruturada
- preparar RAG e embeddings
