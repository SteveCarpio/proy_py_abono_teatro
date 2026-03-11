# ----------------------------------------------------------------------------------------------
#                                  LIBRERIAS NECESARIAS 
# Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------------
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ----------------------------------------------------------------------------------------------

# CUSTOMIZE LAS LIBRERÍAS ---------------------------------------------------------------------------------------------------


"""
options.add_argument("--user-data-dir=selenium_profile")        # Perfil para guardar cookies y no volver a aceptarlas
options.add_argument("--profile-directory=Default")             # Fuerza a usar el perfil Google por defecto y no preguntar cual cargar
"""

"""
prefs = {"profile.managed_default_content_settings.images": 2 ,       # 2 = Bloquear  Imágenes
         "profile.managed_default_content_settings.javascript": 1}    # 1 = Habilitar JavaScript 
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-extensions")          # Desactivar extensiones
chrome_options.add_argument("--log-level=3")                 # Suprime los mensajes de log (nivel de error: WARNING y superior)
chrome_options.add_argument("--disable-sync")                # Desactivar la sincronización con el perfil de usuario
chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Desactivar animaciones
chrome_options.add_argument("--disable-features=VizDisplayCompositor")       # Desactivar animaciones
chrome_options.add_argument("--disable-plugins")             # Desactivar plugins
chrome_options.add_argument("--incognito")                   # Usar modo incógnito
chrome_options.add_argument("--headless")                    # Ejecutar SIN interfaz gráfica :  carga más rápido
chrome_options.add_argument("--disable-gpu")                 # Desactivar uso de GPU         :  carga más rápido
chrome_options.add_argument('--ignore-certificate-errors')   # Ignorar certificados   
"""
# ----------------------------------------------------------------------------------------------------------------------------