from app import application
import database
import flask

@application.route('/show/<id>')
def _show(id):
    return flask.render_template('show.html', show=database.read_show(id))
