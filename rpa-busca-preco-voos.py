import re
import sys
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##################### Variáveis de entrada ############################
partida = "Rio de Janeiro, Brasil"  # Região de destino
destino = "Fortaleza, Brasil"  # Região de destino
preco_limiar = 441.00  # Preço máximo desejado
datas_pesquisa = ["2025-06-22"] # Data de partida no formato AAAA-MM-DD
#######################################################################

# Tipo da viagem
IDA_E_VOLTA = 1
SOMENTE_IDA = 2
logs = []

chrome_options = Options()
chrome_options.add_argument("--headless")

# Função para enviar e-mail de notificação
def enviar_email(precos, link):
    remetente = "email-rementente"
    destinatario = "email-destinatario"
    senha = "senha-servico-de-email"

    assunto = "Alerta de Preço de Passagem Aérea"
    corpo = f"Encontramos uma ou mais passagem abaixo do preço definido de R$ {preco_limiar:.2f}.\nPreços encontrados: {', '.join(str(preco) for preco in precos)}.\nConfira: {link}"

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remetente, senha) # Credenciais serviço email (gmail)
            server.sendmail(remetente, destinatario, msg.as_string())
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Função para buscar passagens aéreas
def buscar_passagens(data_viagem):
    print_log(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - 🔄 Iniciando pesquisa para data {data_viagem}")
    # driver = webdriver.Chrome(options=chrome_options) # Caso queira omitir o navegador
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.google.com/travel/flights")

        # Aguarda a página carregar
        time.sleep(2)
        
        # Define somente ida
        print_log('Definir somente ida...')
        botao_tipo_viagem = driver.find_element(By.XPATH, "//div[@class='VfPpkd-aPP78e']")
        botao_tipo_viagem.click()
        opcao_so_ida = driver.find_element(By.XPATH, f"//li[@data-value='{SOMENTE_IDA}']")
        opcao_so_ida.click()
        print_log('Somente ida definida')

        # Aguarda a atualização da página
        time.sleep(2)

        # Insere a partida
        print_log('Insere partida...')
        campo_partida = driver.find_element(By.XPATH, "//input[@aria-label='De onde?']")
        campo_partida.click()
        time.sleep(2)
        campo_partida_input = driver.find_element(By.XPATH, "//input[@aria-label='Outros pontos de partida?']")
        campo_partida_input.send_keys(partida)
        campo_partida_input.send_keys(Keys.ENTER)
        print_log('Partida inserida')

        # Aguarda a atualização da página
        time.sleep(2)

        print_log('Selecionando destino...')
        campo_destino = driver.find_element(By.XPATH, "//input[@placeholder='Para onde?']")
        campo_destino.send_keys(destino)
        time.sleep(3)
        print_log('Clica na primeira opção...')
        primeira_opcao = driver.find_element(By.XPATH, "(//ul[@role='listbox' and contains(@class, 'DFGgtd')])[2]//li[1]")
        primeira_opcao.click()
        print_log('Destino selecionado')

        # Aguarda os resultados carregarem
        time.sleep(2)

        # Insere a data de partida
        print_log('Selecionando data')
        campo_data_partida = driver.find_element(By.XPATH, "//input[@placeholder='Partida']")
        campo_data_partida.click()
        campo_data_partida.send_keys(Keys.CONTROL, "a")  # Seleciona o texto atual
        campo_data_partida.send_keys(data_viagem)
        campo_data_partida.send_keys(Keys.ENTER)

        botao_concluido = driver.find_element(By.XPATH, "(//span[@jsname='V67aGc' and @class='VfPpkd-vQzf8d' and text()='Concluído'])[2]")
        botao_concluido.click()
        print_log('Data Selecionada')

        # Aguarda os resultados atualizarem
        time.sleep(2)

        print_log('Clica em Pesquisar')
        botao_pesquisar = driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and @class='VfPpkd-vQzf8d' and text()='Pesquisar']")
        botao_pesquisar.click()

        time.sleep(2)

        # Extrai os preços dos resultados
        precos_elementos = driver.find_elements(By.XPATH, "//div[h3[text()='Principais voos']]//ul[@class='Rk10dc']")
        print_log(f'Precos elementos: \n{precos_elementos}')
        
        precos_latam = []
        for elemento in precos_elementos:
            precos_latam += trata_resultado(elemento.text)

        if any(preco <= preco_limiar for preco in precos_latam):
            print_log(f"Passagens encontradas abaixo do preço limiar.\nPreços: {precos_latam}")
            link = driver.current_url
            enviar_email(precos_latam, link)
        else:
            print_log("Nenhuma passagem encontrada abaixo do preço limiar.")
    except Exception as e:
        print_log(f"Erro durante a busca: {e}")
    finally:
        driver.quit()
        print_log(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - 🔚 Pesquisa finalizada para viagem em {data_viagem}\n")
        time.sleep(5)

def trata_resultado(text):
    precos_latam = []

    linhas = text.split("\n")
    voo_latam = False
    for linha in linhas:
        if "LATAM" in linha:
            voo_latam = True
        if voo_latam and "R$" in linha:
            voo_latam = False
            preco = linha.split("R$")[1].replace(".", "").replace(",", ".")
            preco = float(preco)
            precos_latam.append(preco)
            print_log(f'Valor do voo: R$ {preco}')
    
    return precos_latam
    
def salvar_logs():
    with open("logs_busca_voos.txt", "a", encoding="utf-8") as f:
        f.write("\n".join(logs))

def print_log(msg):
    print(msg)
    logs.append(msg)


if __name__ == "__main__":
    try:
        # Pesquisa pelas datas definidas
        for data_viagem in datas_pesquisa:
            buscar_passagens(data_viagem)
        salvar_logs()
    except Exception as e:
        print_log(f"Erro ao buscar passagens: {e}")
        salvar_logs()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        sys.exit(0)