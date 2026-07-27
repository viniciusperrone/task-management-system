# 📋 Kanban / Task Management Application

Aplicação Web full-stack para gerenciamento de tarefas em formato Kanban / To-Do List. O sistema conta com uma API REST robusta em **Django REST Framework** no back-end (containerizada com **Docker** e hospedada na **AWS**) e uma interface reativa em **React** no front-end (hospedada na **Vercel**).

---

## 🚀 Tecnologias Utilizadas

### Back-end

* **Python 3.11+** & **Django / Django REST Framework**
* **PostgreSQL**: Banco de dados relacional.
* **Pytest**: Suíte de testes unitários e de integração.
* **JWT (JSON Web Tokens)**: Autenticação e autorização seguras.
* **Docker**: Containerização do ambiente de desenvolvimento e produção.

### Front-end

* **React.js**
* **Axios / Context API**: Gerenciamento de estado e consumo de requisições HTTP.

### DevOps & Infraestrutura

* **AWS (Amazon Web Services)**: Hospedagem e deploy do container/serviço do Back-end.
* **Vercel**: Deploy automatizado e hospedagem de alta performance do Front-end em React.
* **GitHub Actions**: Pipeline de CI/CD para execução automática de testes e rotinas de deploy.

---

## 🏛️ Arquitetura e Decisões de Design

A arquitetura do projeto foi estruturada para manter o desacoplamento total entre o cliente (React) e o servidor (Django), aplicando boas práticas de engenharia de software:

* **SOLID**:
* *Single Responsibility Principle (SRP)*: Separação clara entre Controllers/Views, Services (regras de negócio) e Serializers.
* *Open/Closed Principle (OCP)*: Estrutura extensível de filtros e rotas sem modificação de código legado.


* **DRY (Don't Repeat Yourself)**:
* Abstrações de filtros e *mixins* reutilizáveis no Django.
* Componentes e hooks customizados no React para consumo de endpoints da API.


* **KISS (Keep It Simple, Stupid)**:
* Modelagem de dados direta e desacoplada.
* Interface limpa e objetiva focada na experiência do usuário.



---

## ✨ Funcionalidades Principais

* **Autenticação de Usuários**: Cadastro, login e gestão de sessão baseada em tokens JWT.
* **CRUD de Tarefas**: Adição, leitura, edição e exclusão de tarefas.
* **Status da Tarefa**: Alternância entre tarefas concluídas e não concluídas.
* **Categorias**: Criação e associação de categorias para organização das tarefas.
* **Compartilhamento**: Possibilidade de compartilhar tarefas com outros usuários cadastrados.
* **Filtros e Paginação**: Busca e filtragem avançada (por status, categoria, etc.) combinadas com paginação dos resultados no back-end.
* **Integrador de API Externa**: Integração com serviço externo para enriquecimento dos dados da aplicação.

---

## 🛠️ Como Executar o Projeto

### Back-end (com Docker)

1. **Clone o repositório:**
```bash
git clone https://github.com/viniciusperrone/task-management-system.git
cd task-management-system/backend

```


2. **Crie o arquivo `.env**` (com base no `.env.example`):
```bash
cp .env.example .env

```


3. **Suba os containers com Docker:**
```bash
docker compose up --build

```


A API estará disponível em `http://localhost:8000/api/`.

---

### Front-end (Local)

1. **Acesse a pasta do front-end:**
```bash
cd ../frontend

```


2. **Instale as dependências e inicie o servidor de desenvolvimento:**
```bash
npm install
npm start # ou npm run dev

```


A interface estará disponível em `http://localhost:3000`.

---

## 🧪 Executando os Testes

### Testes Unitários e de Integração (Pytest)

Para rodar a suíte de testes do back-end no container Docker:

```bash
docker compose exec backend pytest

```

---

## 🔄 Pipeline de CI/CD

O repositório utiliza o **GitHub Actions** (`.github/workflows/ci-cd.yml`) para garantir a qualidade e a integração contínua:

1. **CI (Back-end)**: Execução automática da suíte de testes com `pytest` a cada *push* ou *pull request*.
2. **CD (Front-end - Vercel)**: Build e deploy automático da aplicação React a cada atualização na branch principal (`main`/`master`).
3. **CD (Back-end - AWS)**: Atualização da aplicação no ambiente da AWS.

---

## 📂 Estrutura do Repositório

```text
.
├── .github/
│   └── workflows/          # Workflows de CI/CD (GitHub Actions)
├── backend/                # Aplicação Django REST Framework
│   ├── apps/               # Módulos do sistema (tasks, users, categories)
│   ├── tests/              # Testes automatizados com pytest
│   ├── Dockerfile          # Imagem Docker do back-end
│   ├── docker-compose.yml  # Configuração dos serviços do back-end e banco de dados
│   └── requirements.txt
├── frontend/               # Aplicação React
│   ├── src/                # Componentes, Hooks e Contextos
│   └── package.json
└── README.md

```

---

## 📝 Historico de Commits

O projeto foi construído utilizando mensagens de commit curtas e semânticas (*Conventional Commits*) para facilitar a auditoria e revisão:

* `feat(backend): add JWT authentication and user routes`
* `feat(tasks): implement filtering and pagination for the tasks endpoint`
* `test(pytest): add integration tests for the task CRUD`
* `ci: configure GitHub Actions pipeline to run pytest`
* `deploy: adjust configuration for deployment on AWS and Vercel`
