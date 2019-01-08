# Tastee
Tastee is a simple website written in Python, HTML, and SCSS. The goal of this example website is to combine my skills and deploy a simple full-stack web application.
# Installation
## Dependencies
To run Tastee from its source code Python, and a couple of dependencies need to be installed. The versions that were used for development are:
- Python 3.7.1 
- flask 1.0.2
- flask_sqlalchemy 2.3.1

Example command:
```
pip install flask && flask_sqlalchemy
```
If python 2 is also installed on the machine the pip3 command might be necessary, just replace pip with pip3.
## Database Setup
Tastee uses sqlight. To setup the database for the first time the following commands can be used in a Python interpreter:
```
>>> from tastee import db
>>> db.create_all()
```
This will create a new empty database for the app.

# Attributions
- This website was developed as part of the full-stack nanodegree from Udacity. The instructor Lorenzo provided the basic layout and code structure of the web-site.
- Thank you Pettycon, for uploading the burger icon to Pixabay [Link Here](https://pixabay.com/en/burger-eat-meal-food-hamburger-1674881/).
# License
MIT License

Copyright (c) [2019] [Chance Gurley]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.