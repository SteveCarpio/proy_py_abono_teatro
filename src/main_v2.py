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
        

        # Botón ENTRAR (Usando JavaScript para evitar bloqueos)
        print("🖱️ Haciendo click en Entrar...")
        boton_entrar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dformrlogin input[value='Entrar']")))
        driver.execute_script("arguments[0].click();", boton_entrar)   # JavaScript para hacer clic. Esto rompe cualquier capa invisible o evita errores
        print("✅ Click realizado. Esperando respuesta...")



        # 3 - WEB LISTADO DE OBRAS
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        time.sleep(4)



        # PROVINCIA MADRID
        select_provincia = driver.find_element(By.XPATH,'//*[@id="select_provincia_event"]')
        print(f"Provincia Inicio: {select_provincia.text}")
        select_provincia.send_keys("MADRID")

        select_provinciax = driver.find_element(By.XPATH,'//*[@id="select_provincia_event"]')
        print(f"Provincia Final: {select_provinciax.text}")









     
        # --- CAPTURAR DATOS (DENTRO DEL IFRAME) ---
        print("📋 Buscando listado de obras...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a"))) # Esperamos a que cargue al menos un título
        titulos = driver.find_elements(By.CSS_SELECTOR, "div.noo-tribe-events-header h2 a")     # Buscamos TODOS los elementos que coinciden con la estructura del título
        print(f"🎭 Se encontraron {len(titulos)} obras:")
        for i, titulo in enumerate(titulos):
            nombre = titulo.text
            nombre = nombre.strip()  
            print(f"  {i+1}. {nombre}")
            # Ejemplo: archivo.write(nombre + "\n")

  

      







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