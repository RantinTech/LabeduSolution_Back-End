# Labedu Solution Back-End
## 🐍 Configuração do Ambiente Python

Antes de executar este projeto, siga os passos abaixo para configurar corretamente o ambiente de desenvolvimento.

# ⚙️ Projeto Python - Estrutura Modular

Este repositório contém um projeto Python estruturado em módulos organizados por responsabilidades.  
O foco é facilitar a manutenção, escalabilidade e implantação (inclusive na **Vercel**).

---

## 📁 Estrutura do Projeto

```
├── api/
│ ├── init.py
│ ├── login.py
│ ├── register.py
│ └── users.py
│
├── core/
│ ├── init.py
│ ├── config.py
│ ├── database.py
│ └── security.py
│
├── models/
│ ├── init.py
│ └── user_model.py
│
├── services/
│ ├── init.py
│ └── user_service.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── vercel.json
```

### 📦 Descrição dos Diretórios

| Diretório | Descrição |
|------------|------------|
| **api/** | Contém os endpoints e rotas da aplicação (ex: login, registro e listagem de usuários). |
| **core/** | Reúne a configuração principal, conexão com banco de dados e regras de segurança. |
| **models/** | Define os modelos de dados e entidades utilizadas na aplicação. |
| **services/** | Contém a lógica de negócio e serviços de suporte aos endpoints. |
| **requirements.txt** | Lista todas as dependências do projeto. |
| **vercel.json** | Arquivo de configuração para deploy na plataforma Vercel. |

## 🔧 1. Clonar o repositório

Clone este repositório para o seu computador:
```bash
git clone https://github.com/RantinTech/LabeduSolution_Back-End.git
```

Depois, entre na pasta do projeto:
```
cd LabeduSolution_Back-End
``` 
## 🧩 2. (Opcional) Criar um ambiente virtual

É fortemente recomendado criar um ambiente virtual para isolar as dependências do projeto e evitar conflitos com outros pacotes do sistema.

No Windows:
```
python -m venv .venv
.venv\Scripts\activate
``` 
No Linux/macOS:
```
python3 -m venv .venv
source .venv/bin/activate
```

### Se tudo deu certo, você verá o prefixo (.venv) no seu terminal.

## 📦 3. Instalar as dependências

Com o ambiente virtual ativado (ou não, se preferir usar o global), instale as dependências listadas no arquivo requirements.txt:
```
pip install -r requirements.txt
```

## 💡 Caso o pip esteja desatualizado, atualize com:
```
python -m pip install --upgrade pip
```
## 🚀 4. Executar o projeto

Após instalar as dependências, basta rodar o arquivo principal do projeto.
Por exemplo:
```
python main.py
```

### (ajuste o comando conforme o nome do arquivo principal do seu projeto).

## 🧹 5. Dica: adicionar o .venv ao .gitignore

Certifique-se de que o diretório do ambiente virtual não seja enviado para o repositório.
Adicione isso ao seu arquivo .gitignore:
```
# Ambiente virtual
.venv/
venv/
env/
```
## 🧠 Observação

Caso algo não funcione, verifique:

Se o ambiente virtual está ativado ((.venv) aparece no terminal);

Se o Python está instalado corretamente;

Se as dependências foram instaladas sem erro.
