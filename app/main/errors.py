#  “error handlers in main blueprint”
"""“A difference when writing error handlers inside a 
blueprint is that if the errorhandler decorator is used, 
the handler will be invoked only for errors that originate in 
the routes defined by the blueprint.
To install application-wide error handlers,
the app_errorhandler decorator must be used instead.”

Page 119 of Flask Web Development, 2nd Edition"""

from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    #return render_template('404.html'), 404
    pass

@main.app_errorhandler(500)
def internal_server_error(e):
    #return render_template('500.html'), 500
    pass