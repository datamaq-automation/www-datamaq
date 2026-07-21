### 1.5 Instalación de la utilidad de línea de comandos HTTPie

**HTTPie** es una alternativa moderna, amigable e intuitiva a `curl` diseñada específicamente para interactuar con servicios web y APIs RESTful desde la terminal.

#### Ventajas de HTTPie frente a cURL

- **Sintaxis limpia y natural**: Formato claro sin necesidad de agregar flags complejas para enviar peticiones JSON.
- **Salida coloreada y formateada automáticamente**: Resalta la sintaxis de JSON y cabeceras HTTP en la consola.
- **Soporte nativo para JSON**: Envía payloads JSON por defecto sin necesidad de especificar `-H "Content-Type: application/json"`.

#### Métodos de Instalación

Puedes instalar HTTPie globalmente mediante tu administrador de paquetes o en tu entorno de Python usando `pip`:

**Instalación vía pip (Recomendado en el entorno virtual):**
```bash
pip install httpie
```

**Instalación en Debian / Ubuntu:**
```bash
sudo apt update
sudo apt install httpie
```

**Instalación en macOS:**
```bash
brew install httpie
```

#### Comparación de Sintaxis: HTTPie vs cURL

Veamos la diferencia al realizar una petición `POST` enviando un objeto JSON con parámetros para un modelo de Machine Learning:

**Con cURL:**
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 45.2, "vibration": 0.08}'
```

**Con HTTPie:**
```bash
http POST http://127.0.0.1:8000/predict temperature=45.2 vibration=0.08
```

#### Ejemplos Útiles de Comandos HTTPie

1. **Petición GET simple:**
   ```bash
   http GET http://127.0.0.1:8000/health
   ```

2. **Petición POST con parámetros numéricos y de texto:**
   ```bash
   http POST http://127.0.0.1:8000/api/v1/infer model_name="random_forest" threshold:=0.85 features:='[1.2, 3.4, 5.6]'
   ```

3. **Inclusión de Cabeceras Custom (Header Auth):**
   ```bash
   http GET http://127.0.0.1:8000/protected "Authorization: Bearer secret_token_123"
   ```

HTTPie será nuestra herramienta principal en la terminal para testear los endpoints que desarrollaremos a lo largo de esta Sección A.
