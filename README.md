# ✈️ RPA - Busca de Preços de Voos

## 📌 Descrição do Projeto

Este projeto tem como objetivo automatizar a busca de preços de passagens aéreas, utilizando **Python** e **Selenium** para capturar os dados de voos de diferentes companhias aéreas através do google flights.
O script permite definir um preço de referência e a partir disso pesquisa o preço de viagens por diferentes datas. Caso encontre um preço de uma viagem com valor menor que o de referência, envia um email notificando a oportunidade.

**OBS**: Esse script foi validado em 02/2025. Atualizações futuras do site google flights podem exigir o ajuste do script.

## 🚀 Como Executar

Siga as etapas abaixo para configurar e rodar o projeto corretamente.

### 1️⃣ Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes itens instalados:

- Python 3.8+
- Google Chrome
- ChromeDriver compatível com a versão do Chrome (Versões atuais do Chrome como a `133.0.6943.60` não precisam de instalação do driver)
- Virtualenv (opcional, mas recomendado)

### 2️⃣ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuusuario/rpa-busca-preco-voos.git
   cd rpa-busca-preco-voos
   ```
2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Linux/Mac
   source venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure o ChromeDriver:**
   - Baixe a versão correta do [ChromeDriver](https://chromedriver.chromium.org/downloads) correspondente à sua versão do Chrome.
   - Extraia o arquivo e adicione-o ao **PATH** ou coloque na pasta do projeto.

### 3️⃣ Execução

Para rodar o script e iniciar a busca por passagens, utilize:

```bash
python rpa_busca_preco_voos.py
```

## ✨ Features Implementadas

✅ Busca automática de passagens aéreas

✅ Filtragem de voos pela companhia aérea LATAM

✅ Armazenamento de logs de execução do script

✅ Comparação de preços com um limiar definido

✅ Suporte a múltiplas datas para busca

## 📌 Pontos de Melhoria

🔹 Permitir filtragem de outras companhias aéreas

🔹 Melhorar a captura de informações adicionais dos voos

🔹 Melhorar a forma de armazenamento de logs usando bibliotecas apropriadas

🔹 Adicionar suporte a outras companhias e sites de busca

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Selenium**

