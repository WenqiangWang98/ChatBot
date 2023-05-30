# Chatbot para Real Jardín Botánico

Una asistencia virtual que ayuda al público a conocer las plantas y guiarles dentro del jardín.

## Preparación

Es necesario utilizar una máquina virtual en el Azure cloud y certificado (por ejemplo con Certbot) o cualquier otro servidor con dominio seguro.

## Instalación
Es necesario instalar docker y neginx para iniciarlo.

```bash
sudo pip install docker-compose
sudo pip install nginx
```
Ahora clonea los archivo al directorio del servidor.

```bash
git clone https://github.com/WenqiangWang98/ChatBot.git
```

Configurar nginx reverse proxy.
```bash
sudo nano /etc/nginx/sites-available/default
```
Y ecribir esto cambiando el dominio por el del usuario:
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
Ahora hay que copiar los archivos de la página web al direcorio /var/www/html/
```bash
sudo cp <directorio de cahtbot>/Chatbot-Widget/* /var/www/html/ -r
```
Configurar en el archivo del sitio web para que se dirige al dominio tuyo:
```bash
sudo nano /var/www/html/static/js/script.js
```
Ahora encontrar en el archivo de javascrpt la funtion de enviar y escribir el dominio:
```javascript
function send(message) {

    $.ajax({
        //url: "http://localhost:5008/webhooks/rest/webhook",
        url: "https://<dominio>/webhooks/rest/webhook",
        type: "POST",
```

## Iniciar el chatbot
En el directorio del servidor de /ChatBot:
```nano
nano docker-compose up -d
```
Y esperar unos 30 s para que el servidor se inicie correctamente y ya puedes probar el chatbot en la página web.
