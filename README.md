
# Ararx

Atividade prática de C214-L1. Criamos uma versão minimalista do famoso site X (antigo twitter), onde é possível criar posts, comentar, seguir usuários, dar likes, etc.


## 🌟Funcionalidades

- 🔐 Registro e login de usuários
- 📝 Publicação de posts com texto
- 📰 Visualização do feed de posts
- ❤️ Curtir e comentar em posts
- 💬 Responder e curtir comentários
- 👤 Visualização de perfis de usuários
- ➕ Seguir outros usuários

## 🛠️ Stack utilizada
**back end:** Python, FastAPI

## Rodando os testes
Para instalar as dependências do projeto
```bash
  pip install -r requirements.txt
```
Para rodar o servidor use o comando abaixo:
```bash
  python -m uvicorn api.api:app --reload
```

## 🔧 Variáveis de Ambiente
Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`MONGO_URI`
`API_KEY`
`SECRET_KEY`
`ALGORITHM`
`ACCESS_TOKEN_EXPIRE_MINUTES`
`APP_HOST`

## 🔗 Projetos Relacionados
Este projeto consome uma API desenvolvida para a mesma disciplina. Confira o Frontend do Ararx:

- [Ararex Frontend](https://github.com/gabrielss2406/Ararx-Frontend)


## 👥 Autores
- [Samuel Freitas](https://github.com/SamuelFreitasSoares)
- [João Marcos](https://github.com/markinh00)


