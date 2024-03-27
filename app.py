from flask import Flask,render_template
from config import ProductionConfig
from model import db 
#from api.user_login import login_bp
#from api.user_register import register_bp
#from api.dashboard import knowledge_bp
from api.user_chat import chat_bp
#from api.data_source import datasource_bp
#from api.kg_creation import kg_creation_bp
#from api.financial_data import financial_data_bp

app = Flask(__name__)
app.config.from_object(ProductionConfig)
app.secret_key = '123'
db.init_app(app)

with app.app_context():
    # Create all tables
    db.create_all()

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")


# Registering blueprints
#app.register_blueprint(login_bp)
#app.register_blueprint(register_bp)
#app.register_blueprint(knowledge_bp)
app.register_blueprint(chat_bp)

# API to run as cron job
#app.register_blueprint(datasource_bp)
#app.register_blueprint(kg_creation_bp)
#app.register_blueprint(financial_data_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

