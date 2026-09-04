# 🍰 Doce Delícia — Sistema de Gestão para Docerias

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-336791.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#licença)

O **Doce Delícia** é um sistema web desenvolvido para automatizar e otimizar a gestão de encomendas, catálogo de produtos, kits promocionais e perfis de clientes para docerias e confeitarias artesanais. 

 Este projeto foi desenvolvido como **Atividade Prática Avaliativa** para a disciplina de **Linguagem de Programação** do curso de **Análise e Desenvolvimento de Sistemas (ADS)**.

---

## 📌 Objetivos do Projeto

- **Arquitetura Robustecida:** Aplicar o padrão arquitetural **MTV (Model-Template-View)** do Django para construir uma aplicação escalável e bem estruturada.
- **Domínio Completo do CRUD:** Implementar rotas completas de Criação, Leitura, Atualização e Exclusão para 5 entidades do sistema.
- **Integridade e Validação de Dados:** Garantir regras de negócio rígidas (preços não negativos, validações de datas futuras e unicidade de registros) em múltiplas camadas (Models e Forms).
- **Segurança Web:** Utilizar boas práticas de segurança contra vulnerabilidades comuns (SQL Injection via ORM parametrizado, XSS via templates e Hashing de senhas com PBKDF2).
- **Persistência Relacional:** Mapear relacionamentos complexos (1:N e N:M) utilizando PostgreSQL e migrações declarativas.

---

## 🗂️ Modelo de Dados (Entidades)

O sistema conta com 5 entidades interconectadas que compõem a regra de negócio do domínio:

1. **User / Perfil Administradora (`django.contrib.auth`):** Gestão de usuários, permissões, controle de acesso e perfil da administradora.
2. **Categoria:** Classificação dos itens do catálogo (ex: Bolos, Docinhos, Tortas) com geração automática de `slug` único.
3. **Produto:** Cadastro dos itens vendidos individualmente, vinculado a uma Categoria (**1:N**).
4. **Kit:** Montagem de pacotes e combos especiais contendo múltiplos Produtos (**N:M**).
5. **Encomenda:** Registro transacional de pedidos relacionando Clientes/Administradoras com Produtos e Kits (**N:M**).

---

## 🛠️ Tecnologias e Ferramentas

- **Linguagem:** Python 3.10+
- **Framework Web:** Django
- **Banco de Dados:** PostgreSQL (Produção/Desenvolvimento)
- **Driver de Banco:** `psycopg2-binary`
- **Qualidade e Estilo de Código:** `flake8`, `mypy`, `autopep8` (Conformidade com PEP 8)
- **Testes:** `pytest` / `pytest-django`
- **Controle de Versão:** Git & GitHub

---

## ⚙️ Instruções de Instalação e Execução

Siga os passos abaixo para clonar o repositório e executar a aplicação em seu ambiente local.

### 1. Pré-requisitos
- **Python 3.10+** instalado
- **PostgreSQL** instalado e em execução
- **Git** instalado

### 2. Clonar o Repositório
```bash
git clone git@github.com:RafaelaWolffEvangelista/Sistema_Doceria.git
cd Sistema_Doceria

3. Criar e Ativar o Ambiente Virtual (venv)

Windows (PowerShell):
PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
python -m venv venv
.\venv\Scripts\activate

Linux / macOS:
Bash
python3 -m venv venv
source venv/bin/activate
(O prefixo (venv) deverá aparecer no seu terminal confirmando a ativação).

4. Instalar as Dependências
Com o ambiente virtual ativo, execute:

Bash
pip install django psycopg2-binary pytest mypy flake8 autopep8
python -m pip install setuptools wheel --upgrade

5. Configurar o Banco de Dados
Certifique-se de criar um banco de dados no PostgreSQL e atualizar as credenciais no arquivo sistema_doceria/settings.py:

Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seu_banco_de_dados',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
6. Aplicar as Migrações
Gere as tabelas no banco de dados com os comandos:

Bash
python manage.py makemigrations
python manage.py migrate

7. Criar Usuário Administrador
Para acessar o painel administrativo e gerenciar as rotas protegidas:

Bash
python manage.py createsuperuser

8. Executar o Servidor de Desenvolvimento
Bash
python manage.py runserver
Acesse a aplicação no seu navegador pelo endereço: http://127.0.0.1:8000/

🔐 Mecanismos de Segurança Implementados
Proteção contra SQL Injection: Consultas realizadas exclusivamente via Django ORM com Prepared Statements (queries parametrizadas).

Proteção CSRF: Utilização do token {% csrf_token %} em todos os formulários da aplicação.

Autenticação & Sessões: Controle de rotas via decorator @login_required e gerenciamento de expiração de sessão com set_expiry().

Criptografia de Senhas: Armazenamento seguro utilizando PBKDF2 com algoritmo SHA-256.

👤 
Autora: Rafaela Wolff Evangelista

GitHub: @RafaelaWolffEvangelista

Curso: Análise e Desenvolvimento de Sistemas

📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.