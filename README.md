#My Amateur Blog
A Multi User Blog created using python, jinja2 (for templates), and GoogleAppEngine (for deployment).

##Installation
Install [Python](https://www.python.org/downloads/)
Install [GoogleAppEngine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)


##Configuration
After installing GoogleAppEngine, click on File > Add existing Application, and choose the path to where you unzipped the project folder
You can run the copy of your project locally by using ```gcloud app deploy``` and access it through [localhost](http://localhost:8080)
You can also access the [live version](http://gap1-143315.appspot.com/blog)

##Code Layout
All models are in models.py
All handlers have their own .py files
All styling is in static/main.css
All html files are in templates folder
