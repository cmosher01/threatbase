from app import application
import database
import flask

@application.route('/show/<id>')
def _show(id):
    return flask.render_template('show.html', show=database.read_show(application.root_path, id))

@application.route('/shows/<id>')
def _shows(id):
    return flask.render_template('shows.html', shows=database.read_shows(application.root_path, id))
