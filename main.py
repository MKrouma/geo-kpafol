import os
from app import create_app
# from app.utils import db
from waitress import serve
from dotenv import load_dotenv
from app.models.users import User
from app.cores import db

# load env
load_dotenv(override=True)
mode = os.getenv('FLASK_ENV')
print("Flask environment:", mode)

# app
app = create_app(config_name=mode)

# config app shell
@app.shell_context_processor
def make_shell_context():

    context = {
        'db': db,
        'User': User,
        # 'Village': Village,
        # 'VillageLULC': VillageLULC
    }

    return context


if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    serve(app, host='0.0.0.0', port=port)