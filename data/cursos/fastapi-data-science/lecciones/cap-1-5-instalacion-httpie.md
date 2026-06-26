### 1.5 Instalación de la utilidad de línea de comandos HTTPie
**HTTPie** es una alternativa amigable a `curl` para enviar peticiones HTTP a nuestra API de FastAPI desde la terminal:
```bash
# En macOS usando Homebrew
brew install httpie
# En Ubuntu/Debian
sudo apt install httpie

# Probar enviando una petición GET a un endpoint local
http GET http://127.0.0.1:8000/
```
