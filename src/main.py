import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


USERNAME = "stv.madrid@gmail.com"
PASSWORD = "Webmaster1"

var_CHROMEDRIVER = "C:\\MisCompilados\\cfg\\chromedriver-win32\\146\\chromedriver.exe"

URL_LOGIN = "https://www.abonoteatro.com/"


def iniciar_sesion():

    print("🚀 Iniciando navegador...")

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    #driver = uc.Chrome(
    #    options=options,
    #    service=Service(var_CHROMEDRIVER)
    #)

    driver = uc.Chrome(options=options)

    wait = WebDriverWait(driver, 20)

    try:

        print(f"🌐 Navegando a {URL_LOGIN}")
        driver.get(URL_LOGIN)

        # esperar que cargue la página
        time.sleep(3)

        # buscar botón iniciar sesión
        var_iniciar_sesion=f'/html/body/div[5]/section/div/div[5]/div/div/div/div/a/span/span'
        boton_login = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, var_iniciar_sesion)
            )
        )

        print("✅ Botón encontrado")
        boton_login.click()

        time.sleep(5)

    except Exception as e:
        print("❌ Error:", e)

    finally:
        print("✔ Proceso terminado")


if __name__ == "__main__":
    iniciar_sesion()