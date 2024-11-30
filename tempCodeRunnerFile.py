
app = Flask(__name__)
api=Api(app)

#database config
load_dotenv()
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATAB