import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.abonoteatro.com/"
USERNAME = "stv.madrid@gmail.com"
PASSWORD = "Webmaster1"

def aceptar_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)  # Espera 10 segundos
        boton = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Aceptar')]")
                # (By.XPATH, "//button[contains(.,'Aceptar') or contains(.,'Accept')]")
            )
        )
        boton.click()
        print("🍪 Cookies aceptadas")
    except:
        print("ℹ️ No apareció popup de cookies")

def iniciar():
    # 1- CARGA PARAMETROS
    print("🚀 Iniciando navegador")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    # 2 - ABRIR LA WEB PRINCIPAL
    print("🌐 Abriendo web")
    driver.get(URL)
    print("URL actual:", driver.current_url)
    print("Título:", driver.title)
    #driver.switch_to.window(driver.window_handles[-1])                 # Situarse en la Web inicial
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))   # # Esperamos a que cargue el body
    print(f"✅ Página cargada, vantanas cargas: {len(driver.window_handles)}")
    
    

    # 3 - INTERACTUAR CON LA WEB PRINCIPAL
    boton = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]")))
    print("✅ Botón encontrado")
    boton.click()
    print("🎯 Click realizado")

    # 4 - INTERACTUAR CON LA NUEVA WEB: LOGIN
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))   # Esperar que cargue la nueva página
    
    # Acepta las cookies si sale
    aceptar_cookies(driver)


    # X - FIN DEL PROGRAMA
    input("Pulsa ENTER para cerrar")
    driver.quit()

if __name__ == "__main__":
    iniciar()