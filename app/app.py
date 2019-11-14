from flask import Flask, render_template, request
from .modules.terrain_types import TerrainTypes
from .modules.travel_methods import TravelMethods
from .modules.http_methods import HttpMethods
from .modules.bootstrap_helper import BootstrapContextualClasses
from .modules.terrain_tables import TerrainTables
from .modules.ingredients import Ingredients
from .modules.donjon.calendar import DonjonCalendar
from .utilities.generic import create_select_data, update_selected
from .utilities.dice import Dice


app = Flask(__name__)


def crafting(data_dict, args):
    app.logger.info(f'(Crafting) { { k: v for k, v in args.items() } }')

    base_ingredient = args.get('base_ingredient')
    modifier_ingredients = [args.get(f'ingredient_{i+1}') for i in range(3)]

    update_selected(data_dict['base_ingredient_options'], int(base_ingredient))

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

    update_selected(data_dict['terrain_options'], terrain_type)
    update_selected(data_dict['travel_options'], travel_method)

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
    update_selected(data_dict['ingredient_options'], identify_ingredient)

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


def construct_schedule_data(data_dict):
    data_dict['calendar']['days'] = [
        'Yesterday',
        'Today',
        'Tomorrow'
    ]
    data_dict['calendar']['dates'] = [
        'Tirdas, 14th of Last Seed, 3E2026',
        'Middas, 15th of Last Seed, 3E2026',
        'Turdas, 16th of Last Seed, 3E2026'
    ]
    data_dict['calendar']['events'] = [
        ['None'],
        ['None'],
        ['None']
    ]
    data_dict['calendar']['celestial'] = [
        ['None'],
        ['Full moon (Lunitari)', 'Shooting star(s)'],
        ['Full moon (Lunitari)']
    ]
    data_dict['calendar']['weather'] = {
        'tags': [
            ['Warm', 'Sunny', 'Humid'],
            ['Hot', 'Thunderheads', 'Showers', 'Stormy'],
            ['Mild', 'Clear', 'Windy']
        ],
        'descriptions': [
            [
                'Uncomfortably warm days, pleasant nights.',
                'Cloudless skies, excellent visibility.',
                'Air laden with moisture, stifling.',
                'Driving, unpredictable winds.'
            ],
            [
                'Very warm days, warm nights.',
                'Dense dark clouds, often lightning.',
                'Occasional sprinkles, light rain & brief downpours.'
            ],
            [
                'Agreeable temperatures all day, chilly nights.',
                'Very few clouds in the sky, good visibility.',
                'Strong, steady winds ideal for sailing.'
            ]
        ]
    }


def construct_week_data(data_dict):
    data_dict['calendar']['days_in_week'] = 7
    data_dict['calendar']['weekdays'] = [
        'Morndas',
        'Tirdas',
        'Middas',
        'Turdas',
        'Fredas',
        'Loredas',
        'Sundas'
    ]
    data_dict['calendar']['day_of_month'] = [ 8, 9, 10, 11, 12, 13, 14]
    data_dict['calendar']['events'] = [
        ['None'],
        ['None'],
        ['None'],
        ['None'],
        ['None'],
        ['None'],
        ['None']
    ]
    data_dict['calendar']['weather'] = {
        'tags': [
            ['Warm', 'Sunny', 'Humid'],
            ['Hot', 'Thunderheads', 'Showers', 'Stormy'],
            ['Mild', 'Clear', 'Windy']
        ]
    }


def construct_month_data(data_dict):
    from random import choices

    data_dict['calendar']['days_in_week'] = 7
    data_dict['calendar']['weekdays'] = [
        'Morndas',
        'Tirdas',
        'Middas',
        'Turdas',
        'Fredas',
        'Loredas',
        'Sundas'
    ]
    data_dict['calendar']['days_in_month'] = 30
    data_dict['calendar']['events'] = choices([0, 1, 2], [0.5, 0.3, 0.2], k=30)
    data_dict['calendar']['first_weekday_of_month'] = 3


def construct_year_data(data_dict):
    pass


@app.route('/')
def index():
    pages = [{
        'header': 'D&D',
        'sections': [{
            'href': 'dnd_alchemy',
            'text': 'Alchemy'
        }, {
            'href': 'dnd_calendar',
            'text': 'Calendar'
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


@app.route('/dnd/calendar', methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_calendar():
    args = request.form

    display_options = create_select_data(['Schedule', 'Week', 'Month', 'Year'])
    display_template = args.get('display_mode', 'schedule')
    if args.get('prev_month') or args.get('next_month'):
        display_template = 'month'
        # TODO: Pagination

    update_selected(display_options, display_template)

    # calendar = DonjonCalendar('app/data/elderan-calendar.json')

    data_dict = {
        'display_options': display_options,
        'display_template': display_template,
        'calendar': {
            'campaign_start': 'Tirdas, 11th of First Seed, 3E2026',
            'current_day': 155,
            'days_passed': 154,
            'age' : 3,
            'year': 2026,
            'month': 'Last Seed'
        }
    }

    if display_template == 'schedule':
        construct_schedule_data(data_dict)
    elif display_template == 'week':
        construct_week_data(data_dict)
    elif display_template == 'month':
        construct_month_data(data_dict)
    elif display_template == 'year':
        construct_year_data(data_dict)

    return render_template('dnd/calendar.html',
                           favicon='dnd/calendar_b',
                           title='Hass.io Web | D&D | Calendar',
                           **data_dict)


@app.route('/dnd/calendar/schedule/<int:year>/<int:month>/<int:day>', \
           methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_calendar_schedule(year, month, day):
    pass


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8000, debug=True)  # Run locally in debug
    import sys
    print((
        'This module is not meant to be run directly. '
        'Run the ´server´ module instead using ´python server.py´'
    ))
    sys.exit(1)
