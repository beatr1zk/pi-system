# Prompt de Estruturação --- Projeto Bealz

> **Objetivo deste documento:** fornecer contexto completo para outra IA
> compreender, organizar e documentar a estrutura do projeto Bealz antes
> de qualquer implementação.
>
> **Importante:** neste momento, **não gere código, arquivos, SQL,
> templates, rotas ou componentes**. A tarefa é somente estruturar a
> documentação, dependências, ordem de desenvolvimento e regras do
> projeto. Quando uma etapa futura for solicitada, siga a ordem e as
> convenções definidas aqui.

------------------------------------------------------------------------

# 1. Contexto geral do projeto

O projeto se chama **Portfólio Beatriz** e será um portfólio profissional de Design
Gráfico com uma área pública e uma área administrativa.

A aplicação terá duas partes principais:

``` text
BEALZ
│
├── Landing Page pública
│
└── Sistema administrativo
```

A Landing Page será voltada para apresentação profissional e captação de
clientes/contratantes.

A área administrativa será voltada para gerenciamento de:

-   Leads
-   Clientes
-   Projetos
-   Categorias
-   futuramente indicadores no Dashboard

O projeto deve demonstrar integração entre:

-   Design
-   UI/UX
-   HTML
-   CSS
-   JavaScript
-   Python
-   Flask
-   MySQL
-   Git/GitHub
-   futuramente deploy

O objetivo não é criar apenas um CRUD isolado. O projeto deve demonstrar
a integração entre **design, front-end, back-end, banco de dados e
organização de software**.

------------------------------------------------------------------------

# 2. Tecnologias e ferramentas definidas

## Backend

-   Python
-   Flask
-   mysql-connector-python

## Banco de dados

-   MySQL
-   MySQL Workbench

## Front-end

-   HTML semântico
-   CSS
-   JavaScript

Não utilizar React como tecnologia principal neste projeto neste
momento.

## Ambiente

-   VS Code
-   ambiente virtual `venv`
-   Git
-   GitHub

------------------------------------------------------------------------

# 3. Estrutura atual do projeto

A estrutura de pastas existente deve ser preservada e evoluída sem
reorganizações desnecessárias:

``` text
pi-system/
│
├── banco/
│   └── db.py
│
├── models/
│   ├── categoria.py
│   ├── cliente.py
│   ├── lead.py
│   └── projeto.py
│
├── repositories/
│   ├── rep_categorias.py
│   ├── rep_clientes.py
│   ├── rep_leads.py
│   └── rep_projetos.py
│
├── routes/
│   ├── admin.py
│   └── public.py
│
├── static/
│   ├── css/
│   ├── img/
│   └── js/
│
├── templates/
│
├── venv/
│
├── app.py
├── README.md
└── requirements.txt
```

## Convenção obrigatória dos repositories

Os arquivos de repository devem seguir o padrão:

``` text
rep_(nome_da_tabela)
```

Exemplos:

``` text
rep_categorias.py
rep_clientes.py
rep_leads.py
rep_projetos.py
```

Não alterar essa convenção sem uma necessidade explícita.

------------------------------------------------------------------------

# 4. Arquitetura desejada

A aplicação deve manter separação clara de responsabilidades:

``` text
HTML / templates
        ↓
      Flask
        ↓
     Routes
        ↓
      Models
        ↓
   Repositories
        ↓
   mysql.connector
        ↓
      MySQL
```

## Responsabilidades

### `routes/`

Responsável pelas rotas, requisições, renderização de templates e
ligação entre interface e regras do sistema.

### `models/`

Responsável pela representação das entidades como objetos Python.

Os Models podem conter:

- atributos
- `@property`
-   setters
-   métodos próprios da entidade
-   regras simples diretamente relacionadas ao objeto

Não colocar consultas SQL diretamente nos Models.

### `repositories/`

Responsável pela comunicação com o banco e pelas operações SQL.

Cada tabela deverá possuir seu repository correspondente.

### `banco/db.py`

Responsável pela conexão centralizada com o MySQL.

### `templates/`

Responsável pela estrutura HTML renderizada pelo Flask.

### `static/css/`

Responsável pelos estilos.

### `static/js/`

Responsável pelas interações e comportamentos no navegador.

### `static/img/`

Responsável pelas imagens e recursos visuais.

------------------------------------------------------------------------

# 5. Regra de ouro sobre a ordem de desenvolvimento

A ordem de desenvolvimento deve respeitar as dependências entre
entidades.

Não implementar uma entidade que depende de outra antes que sua
dependência esteja definida.

Dependências principais:

``` text
CATEGORIAS ─────────┐
                    │
                    ▼
                 PROJETOS
                    ▲
                    │
CLIENTES ───────────┘
   ▲
   │
   └──── LEADS
```

Mais especificamente:

``` text
CLIENTES
    ↓
LEADS
```

porque um Lead pode possuir `cliente_id`.

E:

``` text
CATEGORIAS
    ↓
PROJETOS
    ↑
CLIENTES
```

porque um Projeto depende de `cliente_id` e `categoria_id`.

Portanto:

``` text
1. Clientes
2. Leads
3. Categorias
4. Projetos
```

Para evitar qualquer problema com chaves estrangeiras, **Clientes e
Categorias devem estar definidos antes de Projetos**.

------------------------------------------------------------------------

# 6. Ordem geral das fases

A documentação deve dividir o desenvolvimento em fases independentes e
ordenadas.

## FASE 01 --- Planejamento e estrutura

Antes de implementar qualquer funcionalidade:

- consolidar requisitos;
-   confirmar entidades;
-   confirmar relacionamentos;
-   confirmar rotas;
-   confirmar estrutura de templates;
-   confirmar estrutura de arquivos;
-   identificar dependências;
-   identificar o que será estático e o que será dinâmico.

Nesta fase, não criar funcionalidades desnecessárias.

------------------------------------------------------------------------

# 7. FASE 02 --- Estrutura semântica da Landing Page

Esta será a primeira grande etapa de implementação visual.

Criar inicialmente somente a estrutura semântica básica do HTML adaptada
ao Flask.

Usar textos grandes temporários com `Lorem ipsum` quando o conteúdo
definitivo não for necessário.

O objetivo desta etapa é:

-   estruturar semanticamente;
-   definir hierarquia;
-   criar as seções;
-   preparar os templates;
-   evitar retrabalho futuro.

Não criar ainda uma implementação visual complexa.

------------------------------------------------------------------------

# 8. Regras para o HTML da Landing Page

O HTML deve ser semântico.

Evitar uso excessivo e desnecessário de `<div>`.

Utilizar elementos adequados ao significado do conteúdo, quando fizer
sentido:

``` html
<header>
<nav>
<main>
<section>
<article>
<figure>
<figcaption>
<form>
<label>
<footer>
```

`<div>` pode ser utilizado quando realmente representar um agrupamento
semântico inexistente ou uma necessidade estrutural.

Não utilizar elementos semânticos apenas por aparência.

Priorizar:

-   acessibilidade;
-   hierarquia correta de headings;
-   navegação clara;
-   labels associados aos campos;
-   estrutura preparada para responsividade;
-   facilidade de manutenção no Flask.

------------------------------------------------------------------------

# 9. Estrutura da Landing Page

A Landing Page deverá seguir a ordem:

``` text
Header
   ↓
Hero
   ↓
Quem sou eu + habilidades
   ↓
Galeria / Projetos
   ↓
Contato + formulário
   ↓
Footer
```

------------------------------------------------------------------------

# 10. Header

Estrutura conceitual:

``` text
LOGO | Home | Quem sou | Projetos | Contato [CTA]
```

Deve conter:

-   logo;
-   navegação principal;
-   link para Home;
-   link para Quem sou;
-   link para Projetos;
-   link para Contato;
-   CTA de contato.

A navegação deve ser planejada para funcionar com âncoras/seções da
Landing Page quando apropriado.

------------------------------------------------------------------------

# 11. Hero

Conteúdo principal:

``` text
PORTFÓLIO

Beatriz Kava

Designer gráfico
```

A estrutura deve priorizar a apresentação imediata da profissional e do
propósito do site.

O conteúdo definitivo poderá ser refinado posteriormente.

Nesta etapa, usar texto provisório quando necessário.

------------------------------------------------------------------------

# 12. Seção "Quem sou eu + habilidades"

A seção deverá possuir espaço para:

-   fotografia;
-   texto de apresentação;
-   estudos/formação;
-   experiências;
-   habilidades.

Estrutura conceitual:

``` text
[ FOTO ]

Texto sobre mim

Estudos
Experiências

Habilidades
● ● ● ● ●
● ● ● ● ○
...
```

Os níveis de habilidade deverão ser futuramente representados de forma
acessível e preferencialmente com HTML/CSS, e não como imagens.

A representação visual com círculos é apenas uma referência visual; a
documentação não deve assumir que ela precisa permanecer exatamente
assim.

------------------------------------------------------------------------

# 13. Galeria / Projetos da Landing Page

A galeria terá espaço para **6 projetos/elementos visuais**.

A referência visual apresentada nos anexos indica uma composição
semelhante a um moodboard/editorial, e não uma simples grade de cards
idênticos.

A composição pode utilizar:

-   imagens maiores;
-   imagens menores;
-   títulos;
-   textos;
-   diferentes proporções;
-   composição assimétrica;
-   agrupamentos visuais.

Cada painel/projeto deve possuir, de maneira semanticamente adequada:

-   imagem;
-   título;
-   pequeno texto/descrição.

A estrutura deve ser preparada para receber os conteúdos reais
posteriormente.

## Importante

A galeria pública será inicialmente **estática**.

Não criar, nesta primeira versão, uma dependência obrigatória entre os
cards da galeria e os projetos do banco de dados.

A área administrativa de Projetos e a galeria pública podem permanecer
independentes inicialmente.

Uma integração futura pode ser considerada, mas não deve aumentar a
complexidade da primeira versão.

------------------------------------------------------------------------

# 14. Contato

Título:

``` text
Vamos conversar?
```

Texto de apoio:

``` text
fazer funcionar para clientes e contratantes
```

Campos:

``` text
Nome
E-mail
Telefone (opcional)
Serviço
Mensagem
```

Botão:

``` text
Enviar
```

Também deverão existir links para:

``` text
Behance
LinkedIn
E-mail
```

O formulário será futuramente conectado ao sistema de Leads.

Fluxo esperado:

``` text
Visitante
    ↓
Formulário
    ↓
POST
    ↓
Flask
    ↓
Lead
    ↓
MySQL
```

Nesta fase inicial, documentar a integração, mas não inventar detalhes
de implementação que ainda não foram solicitados.

------------------------------------------------------------------------

# 15. Footer

Estrutura:

``` text
[ LOGO ]

Links para o Header
Links para Contato

Todos os direitos reservados.
```

O Footer deve possuir estrutura semântica e links reais quando os
destinos já estiverem definidos.

------------------------------------------------------------------------

# 16. FASE 03 --- Planejamento de todas as rotas

Antes de construir as páginas administrativas, mapear todas as rotas
para evitar conflitos futuros.

Existem dois grupos:

``` text
PUBLIC
ADMIN
```

## Rotas públicas

Planejar pelo menos:

``` text
/
```

Landing Page.

Caso sejam necessárias páginas públicas adicionais no futuro,
documentá-las antes de criá-las.

## Rotas administrativas

Planejar:

``` text
/admin
/admin/leads
/admin/clientes
/admin/projetos
/admin/categorias
```

O Dashboard (`/admin`) deve ser planejado desde o começo, mas sua
implementação visual/funcional ficará para o final da primeira versão
administrativa.

------------------------------------------------------------------------

# 17. FASE 04 --- Estrutura base das páginas administrativas

Antes de criar CRUDs completos, criar somente a estrutura das páginas.

Objetivo:

-   definir templates;
-   definir navegação administrativa;
-   definir tabelas;
-   definir áreas de ações;
-   evitar retrabalho visual.

As páginas devem inicialmente poder existir com conteúdo vazio ou dados
de exemplo temporários.

------------------------------------------------------------------------

# 18. Página de Leads

Objetivo:

Visualizar os leads recebidos pelo formulário da Landing Page.

Estrutura base da tabela:

``` text
ID
Nome
E-mail
Telefone
Serviço
Status
Data de cadastro
Ações
```

Ações futuras:

``` text
Visualizar
Editar
Excluir
Converter em cliente
```

Status previstos:

``` text
novo
em_contato
perdido
convertido
```

------------------------------------------------------------------------

# 19. Página de Clientes

Objetivo:

Visualizar e futuramente administrar os clientes.

Estrutura base:

``` text
ID
Nome
E-mail
Telefone
Data de cadastro
Data de atualização
Status
Ações
```

A página deve ser conectada posteriormente aos Projetos.

Relacionamento:

``` text
Cliente 1 ───── N Projetos
```

------------------------------------------------------------------------

# 20. Página de Categorias

Objetivo:

Administrar categorias de projetos.

Exemplos:

``` text
Identidade Visual
UI/UX
Web Design
Social Media
Editorial
Beleza
```

A lista deve permitir futuramente:

``` text
Criar
Visualizar
Editar
Excluir
```

As categorias devem ser criadas **antes dos Projetos**, pois Projetos
dependerão de `categoria_id`.

------------------------------------------------------------------------

# 21. Página de Projetos

Objetivo:

Visualizar e administrar os projetos.

A estrutura base da tabela deverá contemplar:

``` text
ID
Nome do projeto
Cliente
Categoria
Escopo
Data do pedido
Data de entrega
Prioridade
Status
Ações
```

Relacionamentos:

``` text
Projeto → Cliente
Projeto → Categoria
```

Portanto, a implementação desta entidade só deverá ocorrer depois que:

``` text
Clientes
```

e:

``` text
Categorias
```

estiverem estruturados.

------------------------------------------------------------------------

# 22. FASE 05 --- Banco de dados

O banco utilizado será MySQL.

A conexão ficará centralizada em:

``` text
banco/db.py
```

O padrão de conexão será baseado em `mysql.connector`.

Não colocar credenciais reais em documentação pública, README ou código
versionado quando houver alternativa segura.

------------------------------------------------------------------------

# 23. Entidades do banco

As quatro entidades principais são:

``` text
clientes
leads
categorias
projetos
```

------------------------------------------------------------------------

# 24. Estrutura conceitual de Clientes

A tabela `clientes` deve representar pessoas que efetivamente se
tornaram clientes.

Campos planejados:

``` text
id
nome
email
telefone
data_cadastro
data_atualizacao
status
```

------------------------------------------------------------------------

# 25. Estrutura conceitual de Leads

A tabela `leads` deve representar pessoas que demonstraram interesse em
contratar um serviço.

Campos planejados:

``` text
id
nome
email
telefone
servico
mensagem
status
data_cadastro
cliente_id
```

`cliente_id` será opcional/nulo enquanto o Lead ainda não tiver sido
convertido.

Relacionamento:

``` text
Cliente 1 ───── N Leads
```

A implementação deve preservar o histórico do Lead.

Quando convertido:

``` text
Lead
status = convertido
cliente_id = ID do cliente
```

Não excluir automaticamente o Lead durante a conversão.

------------------------------------------------------------------------

# 26. Estrutura conceitual de Categorias

A tabela `categorias` representa as categorias de projetos.

Campos:

``` text
id
nome
descricao
```

`nome` deve ser único.

------------------------------------------------------------------------

# 27. Estrutura conceitual de Projetos

Campos planejados:

``` text
id
cliente_id
categoria_id
nome
escopo
data_pedido
data_entrega
prioridade
status
```

Chaves estrangeiras:

``` text
cliente_id → clientes.id
categoria_id → categorias.id
```

Relacionamentos:

``` text
Cliente 1 ───── N Projetos

Categoria 1 ─── N Projetos
```

------------------------------------------------------------------------

# 28. Ordem de criação do banco

A ordem de dependências deve ser obrigatoriamente respeitada:

``` text
1. clientes
2. leads
3. categorias
4. projetos
```

Justificativa:

### Clientes antes de Leads

Leads podem possuir referência para um cliente após conversão.

### Clientes antes de Projetos

Projetos possuem `cliente_id`.

### Categorias antes de Projetos

Projetos possuem `categoria_id`.

Portanto:

``` text
CLIENTES ───────┐
                ├──→ PROJETOS
CATEGORIAS ─────┘

CLIENTES ───→ LEADS
```

------------------------------------------------------------------------

# 29. FASE 06 --- Models

Depois da definição das tabelas e repositories, estruturar os Models:

``` text
models/
├── cliente.py
├── lead.py
├── categoria.py
└── projeto.py
```

Cada classe deve representar sua entidade.

Não criar lógica SQL dentro dos Models.

A definição de `@property` e métodos deve seguir o padrão já utilizado
no aprendizado do projeto.

------------------------------------------------------------------------

# 30. FASE 07 --- Repositories

Os repositories devem seguir exatamente a convenção:

``` text
repositories/
├── rep_clientes.py
├── rep_leads.py
├── rep_categorias.py
└── rep_projetos.py
```

Cada repository deverá concentrar as operações SQL de sua tabela.

Operações gerais:

``` text
CREATE
READ
UPDATE
DELETE
```

A ordem didática recomendada dentro de cada repository é:

``` text
1. criar/listar estrutura da tabela
2. INSERT
3. SELECT geral
4. SELECT específico
5. UPDATE
6. DELETE
```

Depois adicionar consultas específicas de relacionamento.

------------------------------------------------------------------------

# 31. Uso do cursor

A arquitetura deve utilizar o padrão:

``` text
conectar()
    ↓
cursor = conexao.cursor()
    ↓
cursor.execute()
    ↓
commit(), quando necessário
    ↓
fechar conexão
```

Operações de leitura devem utilizar métodos apropriados como:

``` text
fetchone()
fetchall()
```

Operações com parâmetros devem utilizar placeholders do connector,
evitando concatenação insegura de strings SQL.

Exemplo conceitual:

``` text
INSERT ... VALUES (%s, %s)
```

Não montar SQL concatenando diretamente valores fornecidos pelo usuário.

------------------------------------------------------------------------

# 32. FASE 08 --- CRUD

Depois da base de Models e Repositories:

``` text
Clientes
    ↓
Leads
    ↓
Categorias
    ↓
Projetos
```

Cada entidade deverá receber seu CRUD conforme sua dependência.

Não implementar Projetos antes de Clientes e Categorias.

------------------------------------------------------------------------

# 33. FASE 09 --- Integração Flask

Depois de Models e Repositories estruturados:

``` text
app.py
```

deverá registrar as rotas.

A aplicação deverá separar:

``` text
routes/public.py
routes/admin.py
```

Evitar concentrar todas as rotas em `app.py`.

`app.py` deve ser responsável principalmente pela criação/configuração
da aplicação e registro das rotas.

------------------------------------------------------------------------

# 34. FASE 10 --- Integração do formulário com Leads

Depois que:

-   banco estiver pronto;
-   Model Lead estiver pronto;
-   repository de Leads estiver pronto;
-   rota pública estiver preparada;

integrar:

``` text
Landing Page
    ↓
<form>
    ↓
POST
    ↓
public.py
    ↓
Lead
    ↓
rep_leads.py
    ↓
MySQL
```

O objetivo é transformar cada envio válido do formulário em um Lead.

------------------------------------------------------------------------

# 35. FASE 11 --- Área administrativa funcional

Depois dos CRUDs:

``` text
/admin/leads
/admin/clientes
/admin/categorias
/admin/projetos
```

deverão passar a utilizar dados reais do banco.

A estrutura visual criada anteriormente deve ser mantida.

------------------------------------------------------------------------

# 36. FASE 12 --- Dashboard

O Dashboard deve ser implementado **por último dentro da primeira versão
funcional do administrativo**.

Motivo:

Ele depende dos dados das outras entidades.

Somente depois de existirem:

``` text
Leads
Clientes
Projetos
Categorias
```

faz sentido calcular:

``` text
Total de Leads
Total de Clientes
Total de Projetos
Projetos por categoria
Projetos por status
Leads por status
Conversões
```

Não antecipar a implementação de gráficos ou métricas antes da base de
dados estar funcional.

------------------------------------------------------------------------

# 37. FASE 13 --- CSS e identidade visual

Depois que o HTML semântico estiver definido:

-   estilizar a Landing Page;
-   criar identidade visual;
-   criar responsividade;
-   definir tipografia;
-   criar composição da galeria;
-   trabalhar estados de hover/focus;
-   organizar o administrativo.

A identidade visual do portfólio deve ser profissional, artística e
contemporânea.

Há interesse em:

-   cores vibrantes;
-   elementos fluidos;
-   composição gráfica;
-   elementos desenhados;
-   movimento;
-   interação;
-   efeitos de mouse.

Evitar deixar o projeto com aparência de template administrativo
genérico na Landing Page.

------------------------------------------------------------------------

# 38. FASE 14 --- JavaScript e interações

Somente depois da estrutura HTML e CSS:

-   animações;
-   interações;
-   hover;
-   efeitos de mouse;
-   comportamento da galeria;
-   validações de interface;
-   elementos fluidos.

A ideia de efeitos de água/ondas/ripple pode ser explorada com
JavaScript e CSS.

Não adicionar bibliotecas desnecessárias sem justificativa.

------------------------------------------------------------------------

# 39. Acessibilidade

Desde a estrutura inicial, considerar:

-   HTML semântico;
-   hierarquia correta de títulos;
-   `alt` em imagens;
-   labels nos formulários;
-   foco visível;
-   navegação por teclado;
-   contraste adequado;
-   não depender apenas de cor para comunicar estados;
-   textos legíveis;
-   botões e links claramente identificáveis.

Acessibilidade deve fazer parte da estrutura e não ser uma correção
posterior.

------------------------------------------------------------------------

# 40. Responsividade

A estrutura deve ser preparada para:

``` text
Desktop
Tablet
Mobile
```

Não criar uma estrutura que funcione somente em desktop.

A galeria, especialmente, deverá possuir estratégia responsiva sem
perder a proposta visual.

------------------------------------------------------------------------

# 41. O que não fazer

A IA responsável pelo projeto não deve:

-   gerar código antes de ser solicitado;
-   alterar a arquitetura sem justificar;
-   criar novas tecnologias sem necessidade;
-   transformar tudo em `<div>`;
-   utilizar React sem solicitação;
-   misturar SQL diretamente nas rotas;
-   colocar SQL nos Models;
-   colocar credenciais reais no código público;
-   criar Projetos antes de Clientes e Categorias;
-   integrar a galeria ao banco sem solicitação;
-   criar um Dashboard complexo antes dos CRUDs;
-   criar arquivos duplicados com nomes diferentes para a mesma
    responsabilidade;
-   alterar a convenção `rep_(nome_da_tabela)`;
-   implementar funcionalidades futuras antes da etapa correta.

------------------------------------------------------------------------

# 42. Ordem final consolidada

A ordem recomendada para execução é:

``` text
01. Planejamento e documentação
        ↓
02. Estrutura semântica da Landing Page
        ↓
03. Planejamento completo das rotas
        ↓
04. Estrutura base das páginas administrativas
        ↓
05. Definição/validação das entidades e relacionamentos
        ↓
06. Model Cliente
        ↓
07. Repository Cliente
        ↓
08. CRUD Cliente
        ↓
09. Model Lead
        ↓
10. Repository Lead
        ↓
11. CRUD Lead
        ↓
12. Model Categoria
        ↓
13. Repository Categoria
        ↓
14. CRUD Categoria
        ↓
15. Model Projeto
        ↓
16. Repository Projeto
        ↓
17. CRUD Projeto
        ↓
18. Integração Flask
        ↓
19. Formulário → Leads
        ↓
20. Área administrativa funcional
        ↓
21. Dashboard
        ↓
22. CSS / identidade visual
        ↓
23. JavaScript / interações
        ↓
24. Acessibilidade e responsividade
        ↓
25. Segurança/autenticação
        ↓
26. Testes
        ↓
27. Git/GitHub
        ↓
28. Deploy
```

------------------------------------------------------------------------

# 43. Dependências críticas

Antes de executar qualquer etapa, verificar:

``` text
Projetos
├── depende de Clientes
└── depende de Categorias

Leads
└── pode depender de Clientes para conversão

Dashboard
├── depende de Leads
├── depende de Clientes
├── depende de Projetos
└── depende de Categorias

Formulário
└── depende da estrutura de Leads

Deploy
└── depende da aplicação funcional
```

------------------------------------------------------------------------

# 44. Estado desejado ao final da primeira versão

A primeira versão funcional deverá possuir:

``` text
LANDING PAGE
✓ Header
✓ Hero
✓ Quem sou eu
✓ Habilidades
✓ Galeria com 6 elementos
✓ Contato
✓ Formulário
✓ Links externos
✓ Footer

ADMIN
✓ Dashboard
✓ Leads
✓ Clientes
✓ Categorias
✓ Projetos

BACKEND
✓ Flask
✓ Routes
✓ Models
✓ Repositories
✓ MySQL

INTEGRAÇÕES
✓ Formulário → Leads
✓ Clientes → Projetos
✓ Categorias → Projetos
✓ Leads → Clientes

QUALIDADE
✓ HTML semântico
✓ Responsividade
✓ Acessibilidade básica
✓ Organização de código
✓ Git/GitHub
```

------------------------------------------------------------------------

# 45. Instrução final

Ao receber este documento, trate-o como a **especificação-base do
projeto Bealz**.

Antes de sugerir implementação:

1.  respeite a estrutura de pastas existente;
2.  respeite as convenções de nomes;
3.  respeite a ordem de dependências;
4.  não antecipe funcionalidades de fases futuras;
5.  mantenha Landing Page e área administrativa separadas
    conceitualmente;
6.  mantenha a galeria inicialmente independente do banco;
7.  utilize HTML semântico;
8.  evite `<div>` sem necessidade;
9.  mantenha SQL nos repositories;
10. mantenha Models separados dos repositories;
11. mantenha as rotas separadas em `public.py` e `admin.py`;
12. não implemente código quando o objetivo da solicitação for apenas
    planejamento/documentação;
13. quando uma implementação for solicitada, explique primeiro em qual
    fase ela se encaixa e quais dependências já precisam estar prontas;
14. caso uma nova solicitação entre em conflito com esta documentação,
    sinalize o conflito antes de modificar a arquitetura;
15. sempre priorize uma solução simples e compatível com o nível atual
    do projeto, evitando complexidade desnecessária.

## Regra principal

**Construir em ordem, respeitando dependências e evitando criar
funcionalidades antes da base necessária estar pronta.**

``` text
ESTRUTURA
    ↓
DEPENDÊNCIAS
    ↓
BANCO
    ↓
MODELS
    ↓
REPOSITORIES
    ↓
CRUD
    ↓
FLASK
    ↓
INTEGRAÇÃO
    ↓
INTERFACE
    ↓
INTERAÇÕES
    ↓
TESTES
    ↓
DEPLOY
```

Este documento deve ser utilizado como referência para todas as próximas
etapas do desenvolvimento do Bealz.