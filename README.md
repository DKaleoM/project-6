# Brevets Time Calculator (premium edition)
## Author Info
Author: Kaleo

Contact: kaleom@uoregon.edu

## Description
This project hosts a webpage server for a brevets time calculator
It is based on the one at https://rusa.org/octime_acp.html
The interactive frontend is made using JQuery
The backend is made using the Flask python library, and runs in docker
The actual calculation is in a separate file, and is unit tested
A Makefile is provided with the tasks "run", "logs", and "test"

The Premium edition includes:
Every feature from the MongoDB version:
The calculator comes with submit and display buttons! 
Data is saved when submitting, and can be fetched later with display.

Along with an all-new RESTful API!
Features include: 
Endpoint '/api/brevets': 




## Sources used:

For python documentation references: python docs

https://docs.python.org/

For flask documentation reference: the flask documentation
I also found documentation for the libraries flask ships with here

https://flask.palletsprojects.com/en/3.0.x/

For misc python and javascript stuff: w3schools 

https://www.w3schools.com/howto/howto_js_redirect_webpage.asp

For docker compose: docker docs

https://docs.docker.com/compose/gettingstarted/

For jquery stuff (mostly to learn how to use post with ajax):

https://api.jquery.com/

For how to use the arrow library: arrow documentation

https://arrow.readthedocs.io/en/latest/

For how to use the RESTful features of flask: example To-Do list RESTful api

https://github.com/UO-CS322/TodoListRESTful/tree/main