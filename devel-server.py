from main.api import create_app_blueprint
import os
#if __name__ == '__main__':
#application = create_app_blueprint('testing')
application = create_app_blueprint(os.getenv('FLASK_CONFIG') or 'default')
#application.run(use_debugger=False, use_reloader=False, port=4300, host='0.0.0.0')

application.run(debug=True, use_debugger=False, use_reloader=False, port=4300, host='0.0.0.0')
