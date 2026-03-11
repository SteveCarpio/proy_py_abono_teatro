import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- CONFIGURACIÓN ---
URL = "https://www.abonoteatro.com/"
USERNAME = "stv.madrid@gmail.com"
PASSWORD = "Webmaster1"

def iniciar():
    # 0. LIMPIEZA AGRESIVA DE PROCESOS (Evita errores de conexión)
    print("🧹 Limpiando procesos de Chrome previos...")
    os.system("taskkill /f /im chrome.exe >nul 2>&1")
    os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
    time.sleep(2)

    print("🚀 Iniciando navegador limpio")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")      # Ayuda a evitar crashes
    options.add_argument("--disable-dev-shm-usage") 
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. LOGIN
        print("🌐 Accediendo a la web...")
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Click en login
        try:
            login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]")))
            login_btn.click()
        except: pass
        
        time.sleep(2)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        # Rellenar datos
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✏️ Logueando...")
        driver.find_element(By.ID, "nabonadologin").send_keys(USERNAME)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(PASSWORD)
        
        # Click entrar
        btn_entrar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dformrlogin input[value='Entrar']")))
        driver.execute_script("arguments[0].click();", btn_entrar)
        print("✅ Login correcto.")
        time.sleep(3)

        # 2. IR A LA PÁGINA DEL IFRAME
        print("➡️ Navegando a la zona de obras...")
        driver.get("https://compras.abonoteatro.com/teatro/")
        
        # 3. LA ESTRATEGIA CLAVE: ROBAR URL DEL IFRAME
        print("🔍 Localizando URL interna del listado...")
        
        # Esperamos a que el iframe exista (pero NO entramos en él)
        iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='programacion.abonoteatro.com']")))
        
        url_real = iframe_element.get_attribute("src")
        
        if url_real:
            print(f"🎯 URL encontrada: {url_real}")
            print("🚀 Navegando directamente a la fuente (sin iframes)...")
            
            # NAVEGAMOS DIRECTAMENTE. 
            # Como ya estamos logueados, esta página cargará con datos.
            driver.get(url_real)
        else:
            print("❌ Error crítico: No se encontró la URL del iframe.")
            return

        time.sleep(3) # Esperamos a que cargue el listado real

        # 4. FILTRAR Y CAPTURAR (Ya estamos en la página final, sin iframes)
        print("☑️ Aplicando filtros...")
        try:
            # Filtro Nuevas Obras
            chk = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='select_new_event']")))
            driver.execute_script("arguments[0].click();", chk)
            
            # Botón Lupa
            btn_lupa = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@onclick, 'submit_event_filters')]")))
            driver.execute_script("arguments[0].click();", btn_lupa)
            print("⏳ Filtrando resultados...")
            time.sleep(4)
        except Exception as e:
            print(f"⚠️ Nota: No se aplicaron filtros ({e}). Capturando todo...")

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