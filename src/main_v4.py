import cfg.variables as sTv
from cfg.librerias import *
from cfg.cookies import aceptar_cookies
import time

def iniciar():
    # -- CARGA PARAMETROS ---
    print("🚀 Iniciando navegador")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # MODO INVISIBLE (HEADLESS) 
    
    # Es recomendable añadir estas opciones para evitar timeouts en Windows
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # --- 1. LOGIN ---
        print("🌐 Abriendo web")
        driver.get(sTv.URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        aceptar_cookies(driver)
        
        print("✅ Página cargada")
        boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]")))
        ventanas_antes = len(driver.window_handles)
        boton_login.click()
        print("🎯 Click en Login realizado")
        time.sleep(2)

        # Gestionar nueva pestaña si se abriera
        if len(driver.window_handles) > ventanas_antes:
            print("➡️ Nueva pestaña detectada, cambiando el foco...")
            driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        aceptar_cookies(driver)

        # --- 2. RELLENAR FORMULARIO ---
        print("✏️ Rellenando usuario...")
        campo_usuario = wait.until(EC.element_to_be_clickable((By.ID, "nabonadologin")))
        campo_usuario.clear()
        campo_usuario.send_keys(sTv.USERNAME)

        print("🔑 Rellenando contraseña...")
        campo_pass = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
        campo_pass.send_keys(sTv.PASSWORD)
        
        # Cerrar cookies si estorban
        try:
            cookie_close = driver.find_element(By.CSS_SELECTOR, ".cmplz-btn")
            if cookie_close.is_displayed():
                cookie_close.click()
                time.sleep(1)
        except: pass

        print("🖱️ Haciendo click en Entrar...")
        boton_entrar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dformrlogin input[value='Entrar']")))
        driver.execute_script("arguments[0].click();", boton_entrar)
        print("✅ Login realizado.")

        time.sleep(7)  # by sTv
        print("1")
        #wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # by sTv

        # --- PASO CRUCIAL: NAVEGAR A LA PÁGINA DE TEATRO ---
        # El login no te lleva a las obras, te lleva a "Mi Cuenta".
        # Tenemos que ir explícitamente a la página donde está el iframe.
        print("➡️ Navegando a la página de programación...")
        ##### ¿¿¿¿ driver.get("https://compras.abonoteatro.com/teatro/")
        print("2")
        ##### ¿¿¿¿¿ wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("3")
        time.sleep(10) # Espera extra por si acaso
        print("4")

        # --- 3. ENTRAR EN EL IFRAME ---
        print("🔍 Buscando el iframe de programación...")
        # Buscamos el iframe específico por su URL parcial, es más seguro que por tag genérico
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='programacion.abonoteatro.com']")))
        
        # Antes de entrar, comprobamos que no dio error de timeout
        print("✅ Iframe encontrado. Entrando...")
        driver.switch_to.frame(iframe)
        
        # --- 4. APLICAR FILTROS (DENTRO DEL IFRAME) ---
        print("☑️ Marcando filtro 'Nuevas Obras'...")
        try:
            # XPATH del checkbox
            chk = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='select_new_event']")))
            driver.execute_script("arguments[0].click();", chk)
            
            # XPATH de la lupa
            print("🔍 Pulsando Lupa...")
            btn_lupa = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@onclick, 'submit_event_filters')]")))
            driver.execute_script("arguments[0].click();", btn_lupa)
            
            print("⏳ Esperando resultados...")
            time.sleep(4)
        except Exception as e:
            print(f"⚠️ Nota: No se pudieron aplicar filtros (quizás ya estaban puestos o no existen): {e}")

        # --- 5. CAPTURAR DATOS ---
        print("📋 Buscando listado de obras...")
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")))
            titulos = driver.find_elements(By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")
            print(f"🎭 Se encontraron {len(titulos)} obras:")
            for i, titulo in enumerate(titulos):
                print(f"  {i+1}. {titulo.text.strip()}")
        except:
            print("❌ No se encontraron obras dentro del iframe.")

        driver.switch_to.default_content()

        input("\n✅ Proceso finalizado. Pulsa ENTER para cerrar el navegador...")

    except Exception as e:
        print(f"❌ Ha ocurrido un error crítico: {e}")
        # Pausa para ver el error antes de cerrar
        input("Pulsa ENTER para cerrar...")
    
    finally:
        print("👋 Cerrando navegador...")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    iniciar()