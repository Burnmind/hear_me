import rospy
from geometry_msgs.msg import PoseStamped
from flask import Flask, send_from_directory, Response
import mimetypes
import threading

flask_server = None

def start_web_ear():
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    app = Flask(__name__)

    def web_content(filename):
        content = ''
        mimetype = 'text/html'
        with open(filename, 'r') as file_content:
            content = file_content.read()
            mimetype, _ = mimetypes.guess_type(filename)

        return Response(content, mimetype=mimetype)

    @app.route('/')
    def index():
        return web_content('web-ear/dist/index.html')
    
    @app.route('/assets/<path:file>')
    def assets(file):
        return web_content(f'web-ear/dist/assets/{file}')
    

    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

    def run_flask():
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

    global flask_server
    flask_server = threading.Thread(target=run_flask)
    flask_server.daemon = True
    flask_server.start()

if __name__ == '__main__':
    try:
        rospy.init_node('hear_me_node')
        start_web_ear()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass