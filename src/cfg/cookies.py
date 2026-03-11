from   cfg.librerias import *

def aceptar_cookies(driver):
    """
    Busca y acepta cookies si aparecen.
    Usa un try/except simple para no detener el flujo si no salen.
    """
    try:
        # Espera corta (3 segundos) porque a veces tardan en aparecer
        wait = WebDriverWait(driver, 3)
        # Busca botones que contengan la palabra 'Aceptar' o 'Accept'
        boton = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Aceptar') or contains(.,'Accept')]")
            )
        )
        boton.click()
        print("🍪 Cookies aceptadas")
    except:
        # Si no aparecen, simplemente continuamos sin imprimir error (es normal)
        pass