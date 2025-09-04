# APAGATOR: Tu Asistente de Ahorro de Energía

<pre>
 █████╗ ██████╗  █████╗  ██████╗  █████╗ ████████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████║██████╔╝███████║██║  ███╗███████║   ██║   ██║   ██║██████╔╝
██╔══██║██╔═══╝ ██╔══██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗
██║  ██║██║     ██║  ██║╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
</pre>

¿Alguna vez has dejado el ordenador encendido toda la noche por un descuido? **APAGATOR** es una pequeña y útil herramienta diseñada para una tarea muy específica: **apagar tu PC automáticamente tras 60 minutos de inactividad**.

Así de simple. Si no estás usando el teclado o el ratón, APAGATOR asume que no estás, y ayuda a tu equipo (y a tu factura de la luz) a tomarse un merecido descanso.

---

### ¿Cómo funciona?

APAGATOR es un guardián silencioso y eficiente:

-   **Función principal**: Inicia una cuenta atrás para apagar el sistema cuando detecta que ha estado inactivo durante **60 minutos**.
-   **Vigilancia inteligente**: Monitoriza constantemente el uso del teclado y el ratón para saber si estás ahí.
-   **Sin interrupciones**: Si detecta cualquier actividad, el temporizador se reinicia al instante. Puedes trabajar con la tranquilidad de que no se apagará mientras estés en medio de algo importante.
-   **Multiplataforma y Autónomo**: Funciona en **Windows, macOS y Linux**. Además, intenta instalar las dependencias que necesita para que no tengas que preocuparte por ello.
-   **Control total**: Puedes cancelar el proceso en cualquier momento con solo presionar `Ctrl+C`.

---

### Instrucciones de Uso

Ponerlo en marcha es muy sencillo:

1.  **Necesitas Python 3**.
2.  Abre una terminal y navega hasta la carpeta donde se encuentra `APAGATOR.py`.
3.  **Ejecuta el script**:
    ```bash
    python3 APAGATOR.py
    ```
4.  **Nota para Linux y macOS**: Para que el comando de apagado funcione correctamente, es recomendable ejecutar el script con privilegios de administrador:
    ```bash
    sudo python3 APAGATOR.py
    ```
    El script te recordará amablemente si lo olvidas.

Una vez iniciado, verás en la terminal una cuenta atrás con un diseño retro. Puedes minimizarla y seguir con tus cosas; APAGATOR funcionará discretamente en segundo plano.

---

### Dependencias

El script está diseñado para ser lo más autónomo posible. Al arrancar, comprobará e intentará instalar lo siguiente si es necesario:

-   **Windows**: El paquete `pywin32`.
-   **Linux**: La herramienta `xprintidle` (usará el gestor de paquetes de tu sistema, como `apt`, `dnf`, `pacman`, etc.).
-   **macOS**: Utiliza `ioreg`, que normalmente ya está incluido en el sistema operativo.

Si por alguna razón la instalación automática no funciona, el script te informará sobre qué dependencia necesitas instalar manualmente.

---

### Configuración

El tiempo de espera está fijado en 60 minutos, pero puedes ajustarlo a tu gusto. Simplemente abre el archivo `APAGATOR.py` en un editor de texto y modifica esta línea:

```python
MINUTOS_PARA_APAGAR = 60 # Cambia este valor por los minutos que desees
```

---

**APAGATOR** es una solución simple para un problema común. Úsalo para ahorrar energía, alargar la vida de tus componentes y evitarte la molestia de darte cuenta a la mañana siguiente de que el ordenador se quedó encendido. ¡Pruébalo!
