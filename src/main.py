import cfg.variables as sTv
from   cfg.librerias import *
from   cfg.cookies import aceptar_cookies

def iniciar():
    # 1- CARGA PARAMETROS
    print("🚀 Iniciando navegador")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    #options.add_argument("--headless=new")  # MODO INVISIBLE (HEADLESS) 
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 2 - ABRIR LA WEB PRINCIPAL
        print("🌐 Abriendo web")
        driver.get(sTv.URL)
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")

        # Esperamos a que cargue el body
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Intentamos aceptar cookies al entrar (por si salen al principio)
        aceptar_cookies(driver)
        
        print("✅ Página cargada")

        # 3 - INTERACTUAR CON LA WEB PRINCIPAL (LOGIN)
        # Buscamos el enlace de login
        boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]")))
        print("✅ Botón Login encontrado")
        
        # Guardamos el número de pestañas actual
        ventanas_antes = len(driver.window_handles)
        boton_login.click()
        print("🎯 Click en Login realizado")

        # Esperamos a que cargue
        time.sleep(2) # Pequeña pausa para que procese el click

        # COMPROBACIÓN: ¿Se abrió una nueva pestaña?  <----  sTv:[OPCIONAL]
        if len(driver.window_handles) > ventanas_antes:
            print("➡️ Nueva pestaña detectada, cambiando el foco...")
            driver.switch_to.window(driver.window_handles[-1])
        
        # Esperamos a que la nueva página (sea pestaña o misma ventana) cargue
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 4 - PASOS SIGUIENTES
        # Intentamos aceptar cookies de nuevo por si la nueva página las pide
        aceptar_cookies(driver)

        # --- AQUÍ IRÍA TU LÓGICA DE RELLENO DE USUARIO/CONTRASEÑA ---
        # Ejemplo (habría que buscar los inputs reales en la web):
        # input_user = driver.find_element(By.ID, "email")
        # input_user.send_keys(USERNAME)
        # ...

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