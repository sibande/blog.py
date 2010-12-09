#blog.py

**blog.py** is a Python blog that runs on Google App Engine

##Requirements and Installation

You will need to extract the following packages under lib/

- [Jinja2](http://jinja.pocoo.org/)
- [markdown](http://daringfireball.net/projects/markdown/)
- [Pygments](pygments.org/)
- [web.py](http://webpy.org) *(suprise)*

Then set your application name in **app.yaml**

##Note

You might want to consider using my patched lib/web/form.py instead of the one that comes with web.py.
The errors now display on top of the input fields instead of below and they are enclosed by a div with an *error* class instead of the **stong** tags)

##License

(C) 2010 Josi Sibande GNU GPL 3.