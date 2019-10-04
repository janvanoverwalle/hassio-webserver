from flask import Flask, render_template, request, redirect, url_for
from data.terrain_types import TerrainTypes
from data.travel_methods import TravelMethods
from data.http_methods import HttpMethods
from data.bootstrap_helper import BootstrapContextualClasses
from data.terrain_ingredients import TerrainTables, TerrainTable
from utilities.generic import create_select_data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/dnd/herbalism', methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_herbalism():
    terrain_options = create_select_data(TerrainTypes.to_list())
    travel_options = create_select_data(TravelMethods.to_list())

    data_dict = {
        'terrain_options': terrain_options,
        'travel_options': travel_options
    }

    msg = None
    if HttpMethods.is_post(request.method):
        args = request.form
        gathering_roll = args.get('gathering_roll', 0)
        if not gathering_roll:
            gathering_roll = 0
        terrain_type = args.get('terrain_type')
        travel_method = args.get('travel_method')

        app.logger.info(f'Roll: "{gathering_roll}", Terrain: "{terrain_type}", Travel: "{travel_method}"')

        gathering_successful = TravelMethods.gather(travel_method, gathering_roll)
        data_dict['gathering_successful'] = gathering_successful

        gathering_result_class = BootstrapContextualClasses.SUCCESS if gathering_successful else BootstrapContextualClasses.ERROR
        data_dict['gathering_result_class'] = gathering_result_class

        app.logger.info(f'Gathering succesfull: {gathering_successful}')

        if gathering_successful:
            ingredient, amount, remarks = TerrainTables.retrieve_ingredient(terrain_type)
            data_dict['ingredient'] = ingredient.to_dict()
            data_dict['amount'] = amount
            data_dict['remarks'] = remarks
            app.logger.info(data_dict['ingredient'])
        else:
            msg = (
                f'Gathering attempt unsuccessful. '
                f'Player rolled {gathering_roll}, '
                f'DC is {TravelMethods.dc(travel_method)}.'
            )

    data_dict['msg'] = msg

    return render_template('dnd/herbalism.html',
                           title='D&D | Herbalism',
                           **data_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
