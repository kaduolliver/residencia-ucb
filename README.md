# residencia-ucb

# Transcrição de Áudio com AssemblyAI

Este projeto faz upload de um arquivo de áudio para a API da [AssemblyAI](https://www.assemblyai.com/) e gera a transcrição com identificação de locutores.

---

## 🔧 Requisitos

Antes de rodar o script, você precisa garantir:

1. **Python**
   - Versão 3.8 ou superior.
   - Verifique com:
     ```bash
     python --version
     ```

2. **Bibliotecas Python**
   - Instale as dependências com:
     ```bash
     pip install requests python-dotenv
     ```
   - Bibliotecas usadas no script:
     - `requests` → Para requisições HTTP à API.
     - `python-dotenv` → Para carregar a chave da API do arquivo `.env`.
     - `time`, `json` e `os` → Já inclusas no Python.

3. **Variável de ambiente**
   - Crie um arquivo `.env` na mesma pasta do script com sua chave da AssemblyAI:
     ```
     ASSEMBLYAI_API_KEY=sua_chave_aqui
     ```
   - Obtenha a chave registrando-se em: [AssemblyAI Dashboard](https://www.assemblyai.com/dashboard/signup)

4. **Arquivo de áudio**
   - Coloque o arquivo de áudio que deseja transcrever na mesma pasta do script.
   - O script espera o arquivo:
     ```
     FHD Ultra ou 2K no medio.mp3
     ```
   - Caso seu arquivo tenha outro nome ou esteja em outra pasta, atualize a variável `ARQ_AUDIO` no script.

5. **Internet**
   - O script precisa de conexão à internet ativa para enviar o áudio e receber a transcrição.

---

## 🚀 Como rodar

1. Clone ou baixe o projeto.
2. Instale as dependências:
   ```bash
   pip install requests python-dotenv
