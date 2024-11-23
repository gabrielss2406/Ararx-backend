
# Ararx

Atividade prática de C214-L1. Criamos uma versão minimalista do famoso site X (antigo twitter), onde é possível criar posts, comentar, seguir usuários, dar likes, etc.


## 🌟 Funcionalidades

- 🔐 Registro e login de usuários
- 📝 Publicação de posts com texto
- 📰 Visualização do feed de posts
- ❤️ Curtir e comentar em posts
- 💬 Responder e curtir comentários
- 👤 Visualização de perfis de usuários
- ➕ Seguir outros usuários

## 🛠️ Stack utilizada
**Backend:** Python, FastAPI
**Database:** MongoDB

## 🚀 Instalação e execução local
Para instalar as dependências do projeto
```bash
  pip install -r requirements.txt
```
Para rodar o servidor use o comando abaixo:
```bash
  python -m uvicorn api.api:app --reload
```

## 🚀Rodando os testes
Estando com o projeto rodando, teremos que instalar outras ferramentas
```bash
  npm install -g newman newman-reporter-html
```

Para rodar os testes gerando o relatório no prompt e em um html
```bash
  newman run tests/Routes.postman_collection.json -e tests/local.postman_environment.json --reporters cli,html --reporter-html-export tests/reports/report.html
```

## 🔧 Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`MONGO_URI`
`API_KEY`
`SECRET_KEY`
`ALGORITHM`
`ACCESS_TOKEN_EXPIRE_MINUTES`
`APP_HOST`

## 🔗 Projetos Relacionados
Este projeto é consumido por uma aplicação web, que também faz parte do projeto da disciplina. Confira o Frontend do Ararx:

- [Ararx Frontend](https://github.com/gabrielss2406/Ararx-Frontend)


## 👥 Autores
- [Samuel Freitas](https://github.com/SamuelFreitasSoares)
- [João Marcos](https://github.com/markinh00)
- [Gabriel Siqueira](https://github.com/gabrielss2406/)
- [Ewel - (Testes)](https://github.com/Ewel10/)


