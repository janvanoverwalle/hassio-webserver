from flask import Flask, render_template, request
from .data.terrain_types import TerrainTypes
from .data.travel_methods import TravelMethods
from .data.http_methods import HttpMethods
from .data.bootstrap_helper import BootstrapContextualClasses
from .data.terrain_tables import TerrainTables
from .data.ingredients import Ingredients
from .utilities.generic import create_select_data
from .utilities.dice import Dice

app = Flask(__name__)


def crafting(data_dict, args):
    app.logger.info(f'(Crafting) { { k: v for k, v in args.items() } }')

    base_ingredient = args.get('base_ingredient')
    modifier_ingredients = [args.get(f'ingredient_{i+1}') for i in range(3)]

    for o in data_dict['base_ingredient_options']:
        if o['value'] == int(base_ingredient):
            o['selected'] = True
            break
    for o in data_dict['ingredient_options']:
        for i in range(len(modifier_ingredients)):
            if o['value'] == int(modifier_ingredients[i]):
                o['selected'] = i+1
                break

    base_ingredient = Ingredients.retrieve(base_ingredient, key=lambda i: i.id())[0]
    ingredients = []
    for ingredient in modifier_ingredients:
        if not ingredient:
            continue
        retrieved_ingredients = Ingredients.retrieve(ingredient, key=lambda i: i.id())
        if not retrieved_ingredients:
            continue
        ingredients.append(retrieved_ingredients[0])

    base_type_set = set(base_ingredient.type())
    matching_ingredients = [i for i in ingredients if base_type_set.intersection(i.type())]
    valid_types = len(matching_ingredients) == len(ingredients)

    if not valid_types:
        data_dict['crafting_result_class'] = BootstrapContextualClasses.ERROR
        data_dict['result_msg'] = (
            f'The following ingredients cannot be combined with {base_ingredient.name()}: '
            f'{", ".join([i.name() for i in ingredients if i not in matching_ingredients])}'
        )
        return

    effect_ingredients = [i for i in ingredients + [base_ingredient] if i.is_effect()]
    max_effects = 2 if Ingredients.BLOODGRASS in effect_ingredients else 1
    valid_effects = len(effect_ingredients) <= max_effects

    if not valid_effects:
        data_dict['crafting_result_class'] = BootstrapContextualClasses.ERROR
        s = '' if max_effects == 1 else 's'
        data_dict['result_msg'] = (
            f'Only {max_effects} <i>Effect</i> ingredient{s} can be used in the same concoction.'
        )
        return

    attempt_dc = 10 + base_ingredient.dc() + sum([i.dc() for i in ingredients])

    data_dict['crafting_result_class'] = BootstrapContextualClasses.SUCCESS
    data_dict['result_msg'] = f'DC to craft this concoction is {attempt_dc}.'
    data_dict['ingredients'] = [i.to_dict(highlight=True) for i in [base_ingredient] + ingredients]


def gathering(data_dict, args):
    app.logger.info(f'(Gathering) { { k: v for k, v in args.items() } }')

    gathering_roll = args.get('gathering_roll', 0)
    if not gathering_roll:
        gathering_roll = 0
    terrain_type = args.get('terrain_type')
    travel_method = args.get('travel_method')

    data_dict['prev_gather_roll'] = gathering_roll
    for o in data_dict['terrain_options']:
        if o['value'] == terrain_type:
            o['selected'] = True
            break
    for o in data_dict['travel_options']:
        if o['value'] == travel_method:
            o['selected'] = True
            break

    gathering_successful = TravelMethods.is_gathering_successful(travel_method, gathering_roll)
    data_dict['gathering_successful'] = gathering_successful

    if gathering_successful:
        gathering_result_class = BootstrapContextualClasses.SUCCESS
    else:
        gathering_result_class = BootstrapContextualClasses.ERROR
    data_dict['gathering_result_class'] = gathering_result_class

    if gathering_successful:
        data_dict['gathering_roll'] = gathering_roll
        ingredient, special = TerrainTables.retrieve_ingredient(terrain_type)
        data_dict['ingredients'] = []
        tmp_dict = {
            'ingredient': ingredient.ingredient.to_dict(highlight=True),
            'amount': ingredient.apply_multiplier(Dice('1d4').roll()),
            'remarks': ingredient.remarks,
            'msg': 'Wow!' if special else ''
        }
        data_dict['ingredients'].append(tmp_dict)

        if ingredient.additional:
            tmp_dict = {
                'ingredient': ingredient.additional.to_dict(highlight=True),
                'amount': 1,
                'msg': 'Extra!'
            }
            data_dict['ingredients'].append(tmp_dict)

    data_dict['result_msg'] = (
        f'Player rolled {gathering_roll}, '
        f'DC for {travel_method} pace is {TravelMethods.dc(travel_method)}.'
    )


def identifying(data_dict, args):
    app.logger.info(f'(Identifying) { { k: v for k, v in args.items() } }')

    identify_roll = args.get('identify_roll', 0)
    if not identify_roll:
        identify_roll = 0
    identify_ingredient = args.get('identify_ingredient')

    data_dict['prev_identify_roll'] = identify_roll
    for o in data_dict['ingredient_options']:
        if o['value'] == identify_ingredient:
            o['selected'] = True
            break

    ingredient = Ingredients.retrieve(identify_ingredient, key=lambda i: i.id())[0]

    identify_dc = 8 + ingredient.identify_dc()

    identify_successful = identify_dc <= int(identify_roll)
    data_dict['identify_successful'] = identify_successful

    if identify_dc + 5 <= int(identify_roll):
        data_dict['show_details'] = True

    if identify_successful:
        identify_result_class = BootstrapContextualClasses.SUCCESS
    else:
        identify_result_class = BootstrapContextualClasses.ERROR
    data_dict['identify_result_class'] = identify_result_class

    if identify_successful:
        data_dict['identify_roll'] = identify_roll
        data_dict['ingredient'] = ingredient.to_dict(highlight=True)

    data_dict['result_msg'] = (
        f'Player rolled {identify_roll}, '
        f'DC for {ingredient.name()} is {identify_dc}.'
    )


@app.route('/')
def index():
    pages = [{
        'header': 'D&D',
        'sections': [{
            'href': 'dnd_alchemy',
            'text': 'Alchemy'
        }, {
            'href': 'dnd_herbalism',
            'text': 'Herbalism'
        }]
    }]
    return render_template('index.html',
                           favicon='favicon',
                           title='Hass.io Web | Home',
                           pages=pages)


@app.route('/dnd/alchemy', methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_alchemy():
    ingredient_list = Ingredients.to_list()
    base_ingredient_options = create_select_data([i for i in ingredient_list if i.is_effect()])
    ingredient_options = create_select_data([i for i in ingredient_list if not i.is_effect() or i.is_special()])
    ingredient_options.insert(0, create_select_data({'name': 'None', 'value': -0x01})[0])

    data_dict = {
        'base_ingredient_options': base_ingredient_options,
        'ingredient_options': ingredient_options
    }

    if HttpMethods.is_post(request.method):
        args = request.form

        crafting(data_dict, args)

    return render_template('dnd/alchemy.html',
                           favicon='dnd/alchemy_b',
                           title='Hass.io Web | D&D | Alchemy',
                           **data_dict)


@app.route('/dnd/herbalism', methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_herbalism():
    terrain_excludes = [TerrainTypes.MOST, TerrainTypes.SPECIAL]
    terrain_options = create_select_data(TerrainTypes.to_list(exclude=terrain_excludes))
    travel_options = create_select_data(TravelMethods.to_list())
    ingredient_options = create_select_data(Ingredients.to_list(), exclude_types=True)

    data_dict = {
        'terrain_options': terrain_options,
        'travel_options': travel_options,
        'ingredient_options': ingredient_options
    }

    if HttpMethods.is_post(request.method):
        args = request.form

        if 'gathering_roll' in args:
            gathering(data_dict, args)

        if 'identify_roll' in args:
            identifying(data_dict, args)

    # app.logger.info(data_dict)

    return render_template('dnd/herbalism.html',
                           favicon='dnd/herbalism_b',
                           title='Hass.io Web | D&D | Herbalism',
                           **data_dict)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8000, debug=True)  # Run locally in debug
    import sys
    print((
        'This module is not meant to be run directly. '
        'Run the ´server´ module instead using ´python server.py´'
    ))
    sys.exit(1)
