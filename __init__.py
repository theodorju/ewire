# Application factory
import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    # __name__ so the app knows where it is located to set up paths
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder='static')

    app.config.from_mapping(
        SEND_FILE_MAX_AGE_DEFAULT=0
    )

    if test_config is None:
        # load the instance config if it exists when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the landing url here
    @app.route("/", methods=["GET"])
    def index():
        """
        Configure route for landing page with GET method
        """
        return render_template("index.html")

    from .src.scheduler import start_scheduler
    start_scheduler()

    # register visualization blueprint
    from .src import visualization
    app.register_blueprint(visualization.bp)

    # register contact blueprint
    from .src import contact
    app.register_blueprint(contact.bp)

    return app
