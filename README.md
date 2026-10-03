# Aplicación de gramática inglesa B1

Esta aplicación permite estudiar 19 temas de gramática B1 con explicaciones en castellano, ejemplos en inglés y enlaces a ejercicios y pruebas de muestra.

El temario ya está cargado y se incluye con la aplicación. Tanto en Windows como en Linux, los pasos siguientes usan esa base de datos: no tienes que cargarla manualmente. **No necesitas una API key de OpenAI**; la instalación y el uso no te la pedirán.


## Windows

### Primera instalación

1. Descarga e instala [Python 3.11 para Windows](https://www.python.org/downloads/windows/). Durante la instalación, marca **Add python.exe to PATH** si aparece esa opción.
2. Abre la carpeta de la aplicación en el Explorador de archivos.
3. Haz clic en la barra de direcciones de esa ventana, escribe `powershell` y pulsa Enter. Se abrirá una ventana de PowerShell.
4. Copia y pega estos comandos, uno detrás de otro:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

5. Cuando aparezca el mensaje de que el servidor está funcionando, abre [http://localhost:5000](http://localhost:5000) en el navegador. Deja abierta la ventana de PowerShell mientras uses la aplicación.

Para cerrar la aplicación, vuelve a PowerShell y pulsa `Ctrl+C`.

### Abrirla otro día

Abre PowerShell en la misma carpeta y ejecuta:

```powershell
.\.venv\Scripts\python.exe app.py
```

Después vuelve a [http://localhost:5000](http://localhost:5000).

## Linux

### Primera instalación

1. En Ubuntu o Debian, abre Terminal e instala Python si todavía no está instalado:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

En Fedora, el comando equivalente es `sudo dnf install python3`.

2. Abre la carpeta de la aplicación. Haz clic derecho dentro de ella y elige **Abrir en una terminal** o una opción con un nombre parecido.
3. Copia y pega estos comandos:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

4. Cuando aparezca el mensaje de que el servidor está funcionando, abre [http://localhost:5000](http://localhost:5000) en el navegador. Deja abierta la Terminal mientras uses la aplicación.

Para cerrar la aplicación, vuelve a Terminal y pulsa `Ctrl+C`.

### Abrirla otro día

Abre una terminal en la carpeta de la aplicación y ejecuta:

```bash
.venv/bin/python app.py
```

Después vuelve a [http://localhost:5000](http://localhost:5000).

## Usar la aplicación

En el Dashboard, elige B1 y abre un tema. Cada tema incluye explicación, estructura, ejemplos, errores frecuentes y enlaces a ejercicios. Al final encontrarás los recursos oficiales de Cambridge para practicar el examen B1 Preliminary.

## Opcional: Podman

Si ya utilizas Podman en Linux, abre una terminal en la carpeta de la aplicación y ejecuta:

```bash
podman build -t grammar-app:latest .
podman run --rm -p 5000:5000 -v "$PWD:/app:Z" grammar-app:latest
```

Abre [http://localhost:5000](http://localhost:5000) y deja abierta la terminal mientras la app esté en uso.

## Detalles técnicos opcionales

La aplicación utiliza `grammar.db`, que ya contiene el temario. No ejecutes `scripts/seed_sqlite.py` para el uso normal: volver a cargar el temario eliminará el progreso guardado.

## License and price: A coffe if for you is well :) . See you at EOI!!!