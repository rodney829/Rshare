# Rshare 1.0

Rshare é um aplicativo de compartilhamento de arquivos com uma interface gráfica moderna usando Kivy.

## Demonstração

Veja a demonstração em vídeo abaixo:

<div align="center">
    <iframe width="560" height="315" src="" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## Requisitos

- Python 3.x
- Kivy
- Flask
- Tkinter

## Como Usar

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/Rshare.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd Rshare
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute o aplicativo:
    ```bash
    python server/main.py
    ```

## Estrutura do Projeto
Rshare/
├── server/
│ ├── gui.py
│ ├── web_server.py
│ └── main.py
├── templates/
│ └── index.html
├── .gitignore
└── README.md

