
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver                                   
from selenium.webdriver.chrome.service import Service             
#from selenium.webdriver.chrome.options import Options    

# --- CONFIGURACIÓN ---
# Pon aquí tus datos reales de acceso
USERNAME = "stv.madrid@gmail.com"
PASSWORD = "Webmaster1"
var_CHROMEDRIVER="C:\\MisCompilados\\cfg\\chromedriver-win32\\146\\"

URL_LOGIN = "https://www.abonoteatro.com/"

def iniciar_sesion():
    print("🚀 Iniciando navegador...")
    
    # Usamos undetected_chromedriver para que la web no detecte que somos un bot
    options = uc.ChromeOptions()
    # options.add_argument("--headless") # Dejamos esto comentado para ver el navegador trabajar
    
    driver = uc.Chrome(service=Service(var_CHROMEDRIVER))

    driver = uc.Chrome(options=options)
    
    

    try:
        # 1. Ir a la web
        print(f"🌐 Navegando a {URL_LOGIN}")
        driver.get(URL_LOGIN)
        
        # 2. Esperar a que cargue la página
        wait = WebDriverWait(driver, 15)
        
        # --- AQUÍ NECESITAMOS LOS SELECTORES ---
        # Abre la web en tu Chrome normal, haz click derecho sobre el campo de usuario -> Inspeccionar.
        # Busca si tiene un ID, un Name o una Clase específica.
        
        print("⏳ Buscando campo usuario...")
        # EJEMPLO: Si el campo tiene id="username", usamos By.ID, "username"
        # Si no tiene ID, busca un atributo type="text" o name="email" dentro de un form.
        
        
        ####var_iniciar_sesion=f'/html/body/div[5]/section/div/div[5]/div/div/div/div/a/span/span'
        ####iniciar_sesion=driver.find_element(By.XPATH,var_iniciar_sesion)
        ####iniciar_sesion.click()


        # CAMBIA ESTO SEGÚN LA WEB:
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "username"))) 
        campo_password = driver.find_element(By.ID, "password") # CAMBIA ESTO
        boton_login = driver.find_element(By.XPATH, '//button[contains(text(), "Entrar") or contains(text(), "Login")]') # CAMBIA ESTO

        # 3. Rellenar formulario
        ####print("📝 Rellenando credenciales...")
        ####campo_usuario.clear()
        ####campo_usuario.send_keys(USERNAME)
        
        ####campo_password.clear()
        ####campo_password.send_keys(PASSWORD)
        
        # 4. Click en entrar
        ####print("🖱️ Haciendo click en entrar...")
        ####boton_login.click()
        
        # 5. Verificar si el login fue exitoso
        # Esperamos a que la URL cambie o aparezca un elemento de "usuario logueado"
        # Según dijiste, te lleva a "compras.abonoteatro.com..."
        ####wait.until(EC.url_contains("compras.abonoteatro.com"))
        
        print("✅ LOGIN EXITOSO. Estamos en:", driver.current_url)
        
        # Pausa para que veas el resultado antes de cerrar
        input("Presiona Enter en la consola para cerrar el navegador...")
        
        return driver # Devolvemos el driver para usarlo en el siguiente paso

    except Exception as e:
        print(f"❌ Error durante el login: {e}")
        # Dejamos el navegador abierto 1 minuto para que inspecciones qué pasó
        time.sleep(60)
        driver.quit()

if __name__ == "__main__":
    driver = iniciar_sesion()
    if driver:
        driver.quit()








