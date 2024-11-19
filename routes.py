from flask_restful import Resource
from models import User

#mainpage dashboard
class Dashboard(Resource):
    def get():
        return {"message": "Geek Room Dashboard!"}

#certificate Sender
class CertificateSender(Resource):
    def get(self):
        return {"message": "Certificate Sender"}

#db connection checker
class Users(Resource):
    def get(self):
        try:
            users = User.query.all()
            # Format users as a list of dictionaries
            users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
            return {"users": users_list}, 200

        except Exception as e:
            return {"error": str(e)}, 500
