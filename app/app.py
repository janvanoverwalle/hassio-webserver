from flask import Flask, render_template, request, redirect, url_for
from models.ingredient_properties import IngredientTerrain

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/dnd/herbalism', methods=['GET', 'POST'])
def dnd_herbalism():
    terrain_options = []
    for t in IngredientTerrain.as_list():
        terrain_options.append({'name': t, 'value': t.lower().replace(' ', '-')})

    if request.method == 'POST':
        data = {
            'msg': 'test'
        }
    else:
        data = None

    return render_template('dnd/herbalism.html',
                           title='D&D | Herbalism',
                           terrain_options=terrain_options,
                           data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
