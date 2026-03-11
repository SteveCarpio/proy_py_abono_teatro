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

def aceptar_cookies(driver):
    """Intenta cerrar la capa de cookies si aparece."""
    try:
        # Damos un segundo por si aparece con animación
        time.sleep(1)
        # Buscamos el botón específico de Complianz (el plugin que usan)
        cookie_btn = driver.find_element(By.CSS_SELECTOR, ".cmplz-btn")
        if cookie_btn.is_displayed():
            cookie_btn.click()
            print("🍪 Cookies aceptadas/cerradas")
            time.sleep(1)
    except:
        # Si no aparece o ya está cerrada, ignoramos
        pass

def iniciar():
    # 0. LIMPIEZA DE PROCESOS (Evita el error 'Read timed out')
    print("🧹 Limpiando procesos previos...")
    os.system("taskkill /f /im chrome.exe >nul 2>&1")
    os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
    time.sleep(2)

    print("🚀 Iniciando navegador")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. LOGIN
        print("🌐 Abriendo web principal...")
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Intentamos cerrar cookies iniciales
        aceptar_cookies(driver)

        # Click en Login
        print("➡️ Accediendo al login...")
        try:
            # Buscamos el enlace de login
            login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]")))
            login_btn.click()
        except:
            print("   (No se encontró botón login, quizás ya estamos en la página)")

        time.sleep(2)
        
        # Gestionar si abrió nueva pestaña
        if len(driver.window_handles) > 1:
            print("🔀 Cambiando a nueva pestaña...")
            driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Cerramos cookies de nuevo en la página de login
        aceptar_cookies(driver)

        # Rellenar Usuario y Contraseña
        print("✏️ Rellenando credenciales...")
        try:
            user_field = wait.until(EC.element_to_be_clickable((By.ID, "nabonadologin")))
            user_field.clear()
            user_field.send_keys(USERNAME)
            
            pass_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            pass_field.send_keys(PASSWORD)
            
            # Click en botón Entrar
            btn_entrar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dformrlogin input[value='Entrar']")))
            driver.execute_script("arguments[0].click();", btn_entrar)
            print("✅ Login realizado.")
            time.sleep(8)
        except Exception as e:
            print(f"⚠️ Error en el formulario: {e}")

        # 2. IR A LA ZONA DE OBRAS
        print("➡️ Navegando a la sección de teatro...")
        driver.get("https://compras.abonoteatro.com/teatro/")
        time.sleep(10)

        # 3. ESTRATEGIA: EVITAR EL IFRAME
        print("🔍 Localizando URL interna del iframe...")
        
        # Buscamos el iframe PERO NO ENTRAMOS
        iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='programacion.abonoteatro.com']")))
        url_real = iframe_element.get_attribute("src")
        
        if url_real:
            print(f"🎯 URL encontrada: {url_real}")
            print("🚀 Navegando directamente a la fuente (sin iframes)...")
            
            # NAVEGAMOS DIRECTAMENTE. Esto evita el error de 'Read timed out'
            driver.get(url_real)
            # Esperamos a que cargue el listado
            time.sleep(8) 
        else:
            print("❌ Error crítico: No se encontró la URL del iframe.")
            return

        # 4. FILTRAR Y CAPTURAR (Ya estamos en la página final)
        print("☑️ Aplicando filtros...")
        try:
            # Filtro Nuevas Obras
            chk = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='select_new_event']")))
            # Usamos JS click por si hay capas residuales
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
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")))
            obras = driver.find_elements(By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")
            
            print(f"🎭 Total obras encontradas: {len(obras)}")
            for i, obra in enumerate(obras):
                print(f"  {i+1}. {obra.text.strip()}")
        except:
            print("❌ No se encontraron obras en la página final.")

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