import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from   cfg.cookies import aceptar_cookies

# --- CONFIGURACIÓN ---
URL = "https://www.abonoteatro.com/"
USERNAME = "stv.madrid@gmail.com"
PASSWORD = "Webmaster1"

def iniciar():
    print("🚀 Iniciando navegador")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new") 
    
    # Solución a errores de timeout y conexión
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # --- 1. LOGIN ---
        print("🌐 Abriendo web y logueando...")
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Click en Login
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]"))).click()
        except:
            pass 

        time.sleep(2)
        
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        aceptar_cookies(driver)

        print("✏️ Rellenando credenciales...")
        driver.find_element(By.ID, "nabonadologin").send_keys(USERNAME)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(PASSWORD)
        
        # Click entrar
        btn_entrar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dformrlogin input[value='Entrar']")))
        driver.execute_script("arguments[0].click();", btn_entrar)
        print("✅ Login correcto. Esperando...")
        time.sleep(3)

        # --- 2. IR A LA PÁGINA DE TEATRO ---
        print("➡️ Navegando a la sección de obras...")
        driver.get("https://compras.abonoteatro.com/teatro/")
        
        aceptar_cookies(driver)

        # --- 3. TRUCO: EVITAR EL IFRAME ---
        print("🔍 Buscando la URL real del listado...")
        
        iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='programacion.abonoteatro.com']")))
        url_directa = iframe_element.get_attribute("src")

        # CORRECCIÓN DEL ERROR DE TIPO
        if url_directa:
            print(f"🎯 URL encontrada: {url_directa}")
            driver.get(url_directa)
        else:
            print("⚠️ No se encontró URL del iframe, usando la general.")
            driver.get("https://compras.abonoteatro.com/teatro/")

        print("✅ Página de obras cargada.")
        time.sleep(3) 

        # --- 4. FILTRAR Y CAPTURAR ---
        print("☑️ Aplicando filtros...")
        try:
            # Filtro Nuevas Obras
            chk = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='select_new_event']")))
            if not chk.is_selected():
                driver.execute_script("arguments[0].click();", chk)
            
            # Botón Lupa
            btn_lupa = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@onclick, 'submit_event_filters')]")))
            driver.execute_script("arguments[0].click();", btn_lupa)
            print("⏳ Filtrando...")
            time.sleep(4)
        except:
            print("⚠️ No se aplicaron filtros.")

        # Capturar Obras
        print("📋 Capturando obras...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")))
        obras = driver.find_elements(By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")
        
        print(f"🎭 Total obras encontradas: {len(obras)}")
        for i, obra in enumerate(obras):
            print(f"  {i+1}. {obra.text.strip()}")

        input("\n✅ FIN. Pulsa ENTER para salir...")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
        input("Pulsa ENTER para cerrar...")
    
    finally:
        print("👋 Cerrando...")
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    iniciar()