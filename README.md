# pi-system-portfolio
Sistema de gerenciamento para designers freelancers.

Repositório: https://github.com/beatr1zk/pi-system


# Sobre o projeto
O `pi-system-portfolio` é um sistema de gerenciamento desenvolvido como Projeto Integrador do curso de Desenvolvedor de Sistemas do SENAC.

O projeto foi desenvolvido com o objetivo de facilitar o gerenciamento de clientes e projetos para designers freelancers, centralizando informações que normalmente poderiam ficar espalhadas em diversas planilhas e arquivos.

A aplicação reúne, em um único sistema, recursos para gerenciamento de clientes, leads, projetos, contatos, categorias, prioridades e status, proporcionando uma organização mais prática das informações.

Embora o sistema tenha sido desenvolvido inicialmente para uso próprio, sua estrutura também pode ser utilizada por outros designers freelancers que precisem centralizar e organizar seus processos de trabalho.


# Objetivos
O principal objetivo do projeto é desenvolver uma aplicação web capaz de centralizar o gerenciamento de informações relacionadas ao trabalho de um designer freelancer.

Durante o desenvolvimento, foram aplicados e aprofundados conhecimentos adquiridos ao longo do curso, principalmente nas áreas de desenvolvimento back-end, banco de dados, desenvolvimento web, organização de projetos e testes automatizados.


# Tecnologias utilizadas
* Python 3.13.14
* Flask 3.1.3
* MySQL
* MySQL Connector/Python
* HTML5
* CSS3
* JavaScript
* Jinja2
* python-dotenv
* Pytest
* Git
* GitHub
* Visual Studio Code


# Funcionalidades
O sistema possui uma área pública e uma área administrativa.

Na aplicação, é possível trabalhar com:
* Clientes
* Leads
* Projetos
* Contatos
* Categorias
* Prioridades de projetos
* Status de clientes
* Status de leads
* Status de projetos
* Autenticação administrativa
* Dashboard administrativo
* Gerenciamento de informações por meio da área administrativa


# Estrutura do projeto
A aplicação foi desenvolvida de forma modular, separando responsabilidades entre banco de dados, modelos, repositórios, rotas, arquivos estáticos, templates, testes e utilitários.

```text
pi-system-portfolio/
│
├── banco/
│   └── Arquivos relacionados à conexão e gerenciamento do banco de dados
│
├── models/
│   └── Modelos utilizados pela aplicação
│
├── repositories/
│   └── Operações de acesso e manipulação dos dados
│
├── routes/
│   └── Rotas e endpoints da aplicação
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/
│   ├── admin/
│   ├── componentes/
│   └── index/
│
├── tests/
│   ├── test_cliente.py
│   ├── test_contato.py
│   ├── test_validacao.py
│   └── test_lead.py
│
├── utils/
│   └── Funções auxiliares e formatação de dados
│
├── app.py
├── seed.py
├── requirements.txt
├── LICENSE
└── README.md
```


# Banco de dados
O sistema utiliza o MySQL como banco de dados.

O banco utilizado pela aplicação possui o nome:

```text
pi_data_base
```

A conexão é configurada por meio de variáveis de ambiente armazenadas no arquivo `.env`.
O projeto possui um script de inicialização (`seed.py`) responsável por preparar o banco de dados para utilização.


# Configuração do ambiente
Antes de executar o projeto, é necessário ter instalado:
* Python 3.13.14
* MySQL
* Git

O MySQL deve estar instalado e em execução na máquina.


# Clonando o projeto
Clone o repositório:

```bash
git clone https://github.com/beatr1zk/pi-system.git
```

Entre na pasta do projeto:

```bash
cd pi-system
```


# Criando o ambiente virtual
Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.\.venv\Scripts\activate
```

Se der erro no seu dispositivo, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


# Instalando as dependências
Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```


# Configurando o arquivo .env
Crie um arquivo chamado `.env` na raiz do projeto.

Utilize as seguintes variáveis:

```env
SECRET_KEY=

DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=pi_data_base
```

O arquivo `.env` não deve ser enviado para o repositório, pois contém informações de configuração e credenciais do banco de dados.

Para evitar o envio de arquivos desnecessários ou que contenham informações sensíveis, crie um arquivo chamado `.gitignore` na raiz do projeto.

Você pode utilizar o [Gitignore Generator](https://www.toptal.com/developers/gitignore) para gerar uma lista de arquivos que devem ser ignorados pelo Git.

Para este projeto, recomenda-se selecionar:
* Python
* Flask
* dotenv
* VisualStudioCode
* Windows

Copie e cole o conteúdo gerado no arquivo `.gitignore`. Dessa forma, arquivos de configuração e credenciais locais não serão enviados para o GitHub.


# Preparando o banco de dados
Depois de configurar o `.env` e garantir que o MySQL esteja em execução, execute:

```bash
python seed.py
```

O `seed.py` realiza a preparação inicial do sistema.

Durante sua execução, ele:

* Cria o banco `pi_data_base`, caso ele ainda não exista;
* Cria as tabelas necessárias;
* Insere os dados iniciais de status, prioridades e categorias;
* Verifica se já existe um administrador;
* Solicita um usuário e uma senha para criar o administrador inicial.

A senha do administrador deve possuir pelo menos 10 caracteres.

Caso o banco e as tabelas já existam, o script evita recriar dados que já estejam cadastrados.


# Executando a aplicação
Depois de executar o `seed.py`, inicie a aplicação com:

```bash
python app.py
```

A aplicação será disponibilizada localmente pelo Flask.

Por padrão, o acesso pode ser realizado em:

```text
http://127.0.0.1:5000/
```


# Testes
O projeto utiliza o Pytest para testes automatizados.

Para executar os testes, utilize:

```bash
python -m pytest
```

Atualmente, os testes abrangem:
* Clientes
* Contatos
* Validações
* Leads

Os arquivos de teste estão localizados na pasta `tests/`.


# Modularização
A aplicação foi organizada de maneira modular para facilitar a manutenção e a separação das responsabilidades.

* `models/` → concentra os modelos utilizados pelo sistema.
* `repositories/` → concentra as operações relacionadas ao acesso e manipulação dos dados.
* `routes/` → contém as rotas responsáveis pelo funcionamento das diferentes partes da aplicação.
* `banco/` → concentra os recursos relacionados à conexão com o MySQL.
* `templates/` → contém as páginas HTML utilizadas pela aplicação, separadas entre a interface administrativa e a interface principal.
* `static/` → contém os arquivos estáticos, como CSS, JavaScript e imagens.
* `utils/` → reúne funções auxiliares utilizadas pela aplicação, incluindo funções relacionadas à formatação e tratamento de dados.
* `tests/` → contém os testes automatizados desenvolvidos com Pytest.


# Seed
O arquivo `seed.py` foi desenvolvido para facilitar a configuração inicial do projeto.

Em vez de exigir que o usuário crie manualmente o banco de dados e todas as tabelas, o script realiza essa preparação automaticamente.

O fluxo de inicialização é:

```text
python seed.py
     │
     ├── Criação do banco de dados
     │
     ├── Criação das tabelas
     │
     ├── Inserção dos dados iniciais
     │
     └── Criação do administrador
```


# Desenvolvimento
O projeto foi desenvolvido individualmente como parte do curso de Desenvolvedor de Sistemas do SENAC.

Ao longo do desenvolvimento, foram aplicados conhecimentos relacionados a desenvolvimento back-end com Python e Flask, desenvolvimento de interfaces web, banco de dados MySQL, organização modular de aplicações, variáveis de ambiente e testes automatizados.

O projeto também foi utilizado para aprofundar conhecimentos sobre a integração entre diferentes camadas de uma aplicação web.


# Versionamento
O código-fonte do projeto é versionado utilizando Git e armazenado no GitHub.

O versionamento permite acompanhar as alterações realizadas durante o desenvolvimento e manter o histórico do projeto.


# Licença
Este projeto está licenciado sob a licença MIT.

Consulte o arquivo `LICENSE` para obter mais informações sobre os termos da licença.
