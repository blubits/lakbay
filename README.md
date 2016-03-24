# Lakbay

Welcome to Lakbay, a traffic-based Metro Manila trip planner! A project by PSHS-Main Campus, group Truth-02 (Maded Batara, Philippe Bungabong, Justine Opulencia). 

Why the new repo? It's an attempt to improve on various things lacking in v1.0. In particular:

1. **Unifying the codebase.** This doesn't simply mean merging the two repos together (which is also a goal, by the way, as it should make codebase changes easier to execute) The algorithm and the website should be more interlinked. To this end, the back-end code will start to see more Flask-centric parts, primarily due to the big change below.
2. **A database-centric model.** A bulk of the new code will be due to the shift from a class-centric model to a hybrid database/class model via SQLAlchemy. This should faciliate faster loading from disk and easier updating through Heroku.
3. **Codebase streamlining.** The back-end system is too complex. With the switch to SQL, some bulky parts of the app can be heavily trimmed down or even removed entirely. (Looking at you, `gtfs_parser.py`.)
4. **Added features** like support for coordinate input through the web interface.

## Notes

* The app requires [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/), and [Requests](http://www.python-requests.org).

