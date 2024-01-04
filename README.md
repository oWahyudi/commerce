
# Commerce - Django
Experimental - Web development using Django framework


1. Create virtual environment
   >python3 -m venv django-env

2. Activate virtual environment
   >source django-env/bin/activate

3. Install requirement
   >pip install -r requirement.txt

4. Create Django Project
   >django-admin startproject <PROJECT_NAME>

5. Run Django application (webserver)
   > python manage.py runserver (default port 8000)  
   > python manage.py runserver 8001  (run at port 8001)  

6. Create Django apps
   > stop webserver (CTR-C)  
   > python manage.py startapp <appname>  
   > Configure <appname> into INSTALL_APP in setting.py (in Django admin Project folder)  
   > Create urls.py in <appname> folder  
   > Configure <appname> path into URLPATTERN in urls.py (in Django admin project folder)  

7. Create default Session table.
   > python manage.py migrate (in Django admin project root folder)



# Nginx -  Configure Nginx as a web server to host image files from an auction platform

1. Install Nginx
   > brew install nginx

2a. start nginx manually
    > nginx

2b. start nginx automatically ( install as service)
    > brew services start nginx

3. Verify nginx instalation, browse http://localhost

4. Configuration file path "/usr/local/etc/nginx/"
   Default webroot path "/usr/local/var/www/"

5a. Stop nginx manually
    > nginx -s stop

5b. Stop nginx (if installed as service)
    > brew services stop nginx

6. Restart nginx
   > brew services restart nginx  or restart nginx




# Configure nginx as file server

1. Create a local nginx local configuration file
   > mkdir /Users/dummyuser/myfolder/nginx.conf

  ```sample config:

server {
  listen 8181;
  server_name localhost;

  # Location for favicon
  location = /favicon.ico { 
     access_log off; 
     log_not_found off; 
  }

 
  # Serve media files directly
  location /media/ {
     alias /Users/dummyuser/files/commerce/media/;
     expires 30d;
  }

  # Proxy other request to Gunicorn server
  # URL for website that consme images files 
  location / {
     proxy_pass http://127.0.0.1:8000;   
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
  }


}
```



3. Include your local nginx.conf to /usr/local/etc/nginx/nginx.conf



```
.
.
.
http {
    
    #include to local nginx.conf path
    include /Users/dummyuser/myfolder//nginx.conf;
.
.
.

```





