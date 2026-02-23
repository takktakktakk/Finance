from flask import Flask
from controllers.recipe_controller import recipe_bp

app = Flask(__name__)

# Blueprint登録
app.register_blueprint(recipe_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
