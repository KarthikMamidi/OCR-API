# OCR-API
An application to get the text from Images being uploaded.

steps to install:

1. open terminal:
2. clone repository
3. cd repository
4. virtualenv venv
5. . venv/bin/activate
6. pip install -r requirements.txt 

open mysql and create a database
7. use this command-> mysql -u root -p enter pwd:-> ****

once you are logged in
8. create database ocr;
9. exit();
once out of mysql

10. ->python models.py #this creates database schema
11. ->python app.py #will begin the server
open the browser go to localhost:8000
