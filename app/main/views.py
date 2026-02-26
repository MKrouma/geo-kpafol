import os
from flask import (
    render_template, Blueprint, jsonify, redirect, 
    url_for, send_from_directory, current_app, request, Response
)
from flask_login import login_required, current_user
from app.auth.forms import LoginForm
import geopandas as gpd 

main = Blueprint('main', __name__, 
                static_folder='static',  # Add static folder
                template_folder='templates'  # Add template folder
)



# FRONTEND 
@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', form=form) 

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('main/app.html')



# BACKEND
@main.route('/api/aoi', methods=['GET', 'POST'])
def get_aoi():
    data_dir = os.path.join(current_app.root_path, '../data')
    aoi = gpd.read_file(os.path.join(data_dir, "aoi_clean.gpkg"))
    geojson_str = aoi.to_json()  # GeoPandas -> GeoJSON string
    return Response(geojson_str, mimetype='application/geo+json')



# STATIC FAVICON
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'images/favicon.ico',
        mimetype='image/png'
    )