# Chatbot para Real Jardín Botánico

Una asistencia virtual que ayuda al público a conocer las plantas y guiarles dentro del jardín.

## Preparación

Es necesario utilizar una máquina virtual en el Azure cloud y certificado (por ejemplo con Certbot) o cualquier otro servidor con dominio seguro.

## Instalación
Se instala las dependencias Docker y NGINX con pip.

```bash
sudo pip install docker-compose
sudo pip install nginx
```
Después se procede a copiar los archivos al directorio del servidor.

```bash
git clone https://github.com/WenqiangWang98/ChatBot.git
```

Configurar NGINX proxy reverso para evitar conflictos en conectividad. 
```bash
sudo nano /etc/nginx/sites-available/default
```
Y es necesario introducir el dominio del servidor en el archivo de configuración:
```nano
server {
    listen 443 ssl;
    listen [::]:443;
    root /var/www/html;
    index index.html;
    server_name <dominio>;
    ssl_certificate     /etc/letsencrypt/live/<dominio>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<dominio>/privkey.pem;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    location /webhooks/rest/webhook {        
        proxy_pass http://localhost:5005/webhooks/rest/webhook;
        proxy_buffering off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
    }
}
```
Ahora hay que copiar los archivos del sitio web estático al directorio “/var/www/html/”
```bash
sudo cp <directorio de chatbot>/Chatbot-Widget/* /var/www/html/ -r
```
Configurar en el archivo del sitio web para que se dirige al dominio correspondiente:
```bash
sudo nano /var/www/html/static/js/script.js
```
Encontrar en el archivo de JavaScript la función de enviar y escribir el dominio:
```javascript
function send(message) {

    $.ajax({
        url: "https://<dominio>/webhooks/rest/webhook",
        type: "POST",
```
## Configuración de la aplicación móvil
Abrir el proyecto con Android Studio, configurar el archivo “Constants” bajo la carpeta “utils”
```java
class Constants {

    companion object {
        val NGROCK_URL = "https://<domain>"
…
    }
}
```
En Build > Build Bundle(s) / APK (s) > Build APK(s) para oftener el archivo APK.
## Iniciar el chatbot
En el directorio del servidor de /ChatBot:
```bash
docker-compose up -d
```
Y esperar unos 30 s para que el servidor se inicie correctamente y ya puedes probar el chatbot en la página web.
