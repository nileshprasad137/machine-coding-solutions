from flask import Flask
from token_system import token_system_bp
from token_system.views import auto_unblock
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.register_blueprint(token_system_bp, url_prefix="")


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=auto_unblock, trigger="interval", seconds=60)
    scheduler.start()

    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    
