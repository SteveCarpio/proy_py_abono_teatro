import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def iniciar_simple():
    print("🚀 Iniciando navegador directo a las obras...")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. IR DIRECTO A LA URL QUE ENCONTRASTE
        # Si esta URL carga el listado, nos ahorramos todo lo anterior
        url_obras = "https://programacion.abonoteatro.com/catalogo/teatros3.php?token=afuihA5GtKvlX6VvX5FAsW"
        driver.get(url_obras)
        
        print("✅ Página cargada. Esperando listado...")
        time.sleep(3) # Pequeña pausa por seguridad

        # 2. APLICAR FILTROS (Opcional)
        # Intentamos marcar el checkbox y dar a la lupa, si falla, seguimos
        try:
            print("☑️ Filtros...")
            chk = driver.find_element(By.XPATH, "//input[@id='select_new_event']")
            driver.execute_script("arguments[0].click();", chk)
            
            btn_lupa = driver.find_element(By.XPATH, "//button[contains(@onclick, 'submit_event_filters')]")
            driver.execute_script("arguments[0].click();", btn_lupa)
            time.sleep(4)
        except:
            print("⚠️ No se aplicaron filtros (quizás no son necesarios o no cargaron).")

        # 3. CAPTAR OBRAS
        print("📋 Buscando obras...")
        # Esperamos a que exista al menos un título
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")))
        
        obras = driver.find_elements(By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")
        
        print(f"🎭 Total obras encontradas: {len(obras)}")
        for i, obra in enumerate(obras):
            print(f"  {i+1}. {obra.text.strip()}")

        input("\n✅ FIN. Pulsa ENTER para salir...")

    except Exception as e:
        print(f"❌ Error: {e}")
        input("Pulsa ENTER para cerrar...")
    finally:
        driver.quit()

if __name__ == "__main__":
    iniciar_simple()