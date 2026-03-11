import cfg.variables as sTv
from   cfg.librerias import *
from   cfg.cookies import aceptar_cookies

def iniciar():
    # -- CARGA PARAMETROS ---
    print("🚀 Iniciando navegador")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    #options.add_argument("--headless=new")  # MODO INVISIBLE (HEADLESS) 
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # --- INTEREACTUAR CON LAS PAGINAS WEB ---

        # 1 - ABRIR LA WEB PRINCIPAL
        print("🌐 Abriendo web")
        driver.get(sTv.URL)
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")

        # Esperamos a que cargue el body
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Intentamos aceptar cookies al entrar (por si salen al principio)
        aceptar_cookies(driver)
        print("✅ Página cargada")
        # Buscamos el enlace de login
        boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]")))
        print("✅ Botón Login encontrado")
        # Guardamos el número de pestañas actual
        ventanas_antes = len(driver.window_handles)
        boton_login.click()
        print("🎯 Click en Login realizado")
        # Esperamos a que cargue
        time.sleep(2) # Pequeña pausa para que procese el click

        # 2 - REDIRECCION A LA WEB: USUARIO Y CONTRASEÑA

        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")

        # COMPROBACIÓN: ¿Se abrió una nueva pestaña?  <----  sTv:[OPCIONAL]
        if len(driver.window_handles) > ventanas_antes:
            print("➡️ Nueva pestaña detectada, cambiando el foco...")
            driver.switch_to.window(driver.window_handles[-1])

        # Esperamos a que la nueva página (sea pestaña o misma ventana) cargue
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Intentamos aceptar cookies de nuevo por si la nueva página las pide
        aceptar_cookies(driver)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # FORMULARIO DATOS DEL USUARIO
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")

        # Rellenamos el usuario
        print("✏️ Rellenando usuario...")
        campo_usuario = wait.until(EC.element_to_be_clickable((By.ID, "nabonadologin")))    # Esperamos a que el campo sea clicleable/escribible
        campo_usuario.clear()
        campo_usuario.send_keys(sTv.USERNAME)
        print("✔️ Usuario introducido")

        # Rellenamos la contraseña
        print("🔑 Rellenando contraseña...")
        campo_pass = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
        campo_pass.send_keys(sTv.PASSWORD)
        print("✔️ Contraseña introducida")
        
        # Intentamos cerrar el banner que aveces aparece específico 'cmplz' que está molestando
        try:
            # Buscamos el botón de aceptar cookies por si sigue visible
            # Usamos un selector genérico para este tipo de banners
            cookie_close = driver.find_element(By.CSS_SELECTOR, ".cmplz-btn")
            if cookie_close.is_displayed():
                cookie_close.click()
                print("🍪 Cerrada ventana de cookies persistente")
                time.sleep(1) # Esperamos a que se anime y desaparezca
        except:
            pass # Si no está, perfecto, seguimos

        # Botón ENTRAR (Usando JavaScript para evitar bloqueos)
        print("🖱️ Haciendo click en Entrar...")
        boton_entrar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dformrlogin input[value='Entrar']")))
        # TRUCO: Usamos JavaScript para hacer clic. Esto rompe cualquier capa invisible 
        # o evita errores si el botón está parcialmente tapado.
        driver.execute_script("arguments[0].click();", boton_entrar)
        print("✅ Click realizado. Esperando respuesta...")




      

        # --- PASO 1: ENTRAR EN EL IFRAME ---
        print("🔍 Buscando el iframe de programación...")
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        print("✅ Estamos DENTRO del iframe.")

        # --- PASO 2: FILTRAR POR NUEVAS OBRAS (USANDO XPATH) ---
        try:
            print("☑️ Marcando filtro 'Nuevas Obras'...")
            
            # 1. Localizamos el contenedor del switch usando TU XPATH
            xpath_switch = '//*[@id="filtros-collapse"]/div/div[1]/div[4]/div[2]'
            switch_container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_switch)))
            
            # Hacemos clic usando JavaScript. Esto evita errores si el botón está tapado o es un input oculto.
            driver.execute_script("arguments[0].click();", switch_container)
            print("   Click realizado en el switch.")

            # 2. Localizamos el botón Lupa usando TU XPATH
            print("🔍 Pulsando botón Lupa...")
            xpath_lupa = '//*[@id="filtros-collapse"]/div/div[1]/div[6]/div[2]/button'
            btn_lupa = wait.until(EC.presence_of_element_located((By.XPATH, xpath_lupa)))
            
            # Clic con JavaScript también por seguridad
            driver.execute_script("arguments[0].click();", btn_lupa)
            print("   Click realizado en lupa.")

            # 3. Esperamos a que carguen los resultados
            print("⏳ Esperando a que cargue el listado filtrado...")
            time.sleep(4) # Damos 4 segundos para que el JS de la web actualice la lista

        except Exception as e:
            print(f"⚠️ Error aplicando filtros: {e}")

        # --- PASO 3: CAPTURAR DATOS ---
        print("📋 Buscando listado de obras...")
        
        # (El resto del código sigue igual para capturar los títulos)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")))
        titulos = driver.find_elements(By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")
        
        print(f"🎭 Se encontraron {len(titulos)} obras:")
        for i, titulo in enumerate(titulos):
            print(f"  {i+1}. {titulo.text.strip()}")
            
        driver.switch_to.default_content()





        # --- FIN DEL PROGRAMA ---

        input("\n✅ Proceso finalizado. Pulsa ENTER para cerrar el navegador...")

    except Exception as e:
        print(f"❌ Ha ocurrido un error: {e}")
        input("Pulsa ENTER para cerrar a pesar del error...")
    
    finally:
        # Este bloque se ejecuta SIEMPRE, haya error o no.
        print("👋 Cerrando navegador...")
        try:
            driver.quit()
        except Exception:
            # Si da el error de WinError 6 al cerrar, lo ignoramos silenciosamente
            pass

if __name__ == "__main__":
    iniciar()