from flask import Flask, jsonify

from flask_cors import CORS

from config import Config

from extensions import db, jwt


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, supports_credentials=True)

    db.init_app(app)

    jwt.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.opportunity_routes import opportunity_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    app.register_blueprint(
        opportunity_bp,
        url_prefix="/api/opportunities"
    )

    from models.user import User
    from models.opportunity import Opportunity

    with app.app_context():
        db.create_all()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):

        return jsonify({
            "message": "Token has expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):

        return jsonify({
            "message": "Invalid token"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):

        return jsonify({
            "message": "Authorization token required"
        }), 401

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)