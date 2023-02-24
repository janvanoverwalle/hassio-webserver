from flask import Flask, request, render_template, redirect, url_for
from .modules.terrain_types import TerrainTypes
from .modules.travel_methods import TravelMethods
from .modules.http_methods import HttpMethods
from .modules.bootstrap_helper import BootstrapContextualClasses
from .modules.terrain_tables import TerrainTables
from .modules.ingredients import Ingredients
from .modules.donjon.calendar import ElderanCalendar
from .modules.surprise import Surprise
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


def construct_schedule_data(data_dict, calendar, display_date=None):
    if not display_date:
        display_date = calendar.today

    yesterday = calendar.get_day(-1, display_date)
    today = calendar.get_day(0, display_date)
    tomorrow = calendar.get_day(1, display_date)

    data_dict['calendar']['days'] = [
        'Yesterday',
        'Today',
        'Tomorrow'
    ]
    data_dict['calendar']['dates'] = [
        yesterday.descr_format(),
        today.descr_format(),
        tomorrow.descr_format()
    ]
    data_dict['calendar']['events'] = [
        calendar.get_notes(yesterday),
        calendar.get_notes(today),
        calendar.get_notes(tomorrow)
    ]
    data_dict['calendar']['celestial'] = [
        calendar.celestial.get_celestial(yesterday),
        calendar.celestial.get_celestial(today),
        calendar.celestial.get_celestial(tomorrow)
    ]
    data_dict['calendar']['weather'] = {
        'tags': [
            calendar.weather.get_weather(yesterday),
            calendar.weather.get_weather(today),
            calendar.weather.get_weather(tomorrow)
        ],
        'descriptions': [
            calendar.weather.get_weather_descriptions(yesterday),
            calendar.weather.get_weather_descriptions(today),
            calendar.weather.get_weather_descriptions(tomorrow)
        ]
    }


def construct_week_data(data_dict, calendar, display_date=None):
    if not display_date:
        display_date = calendar.today

    week = calendar.get_week_by_date(display_date)
    data_dict['calendar']['ref_day'] = display_date.weekday() if display_date == calendar.today else -1
    data_dict['calendar']['days_in_week'] = calendar.days_in_week
    data_dict['calendar']['weekdays'] = calendar.get_weekdays()
    data_dict['calendar']['day_of_month'] = [d.day for d in week]
    data_dict['calendar']['events'] = [calendar.get_notes(d) for d in week]
    data_dict['calendar']['weather'] = {
        'tags': [calendar.weather.get_weather(d) for d in week]
    }


def construct_month_data(data_dict, calendar, display_date=None):
    if not display_date:
        display_date = calendar.today

    month = calendar.get_all_dates_in(display_date.year, display_date.month)
    print(len(month))
    data_dict['calendar']['ref_day'] = display_date.day if display_date == calendar.today else -1
    data_dict['calendar']['days_in_week'] = calendar.days_in_week
    data_dict['calendar']['weekdays'] = calendar.get_weekdays()
    data_dict['calendar']['days_in_month'] = calendar.get_days_in_months(display_date.month-1)
    data_dict['calendar']['events'] = [len(calendar.get_notes(d)) for d in month]
    data_dict['calendar']['first_weekday_of_month'] = month[0].weekday()


def construct_year_data(data_dict, calendar, display_date=None):
    if not display_date:
        display_date = calendar.today

    data_dict['calendar']['days_in_year'] = calendar.days_in_year


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', title='Page not found')


@app.route('/')
def index():
    return redirect(url_for('surprise'))


@app.route('/dnd')
def dnd():
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
    return render_template('dnd/index.html',
                           title='Hass.io Web | D&D',
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
                           scripts=['dnd'],
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
                           scripts=['dnd'],
                           **data_dict)


@app.route('/dnd/calendar', methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_calendar():
    args = request.form
    calendar = ElderanCalendar()

    if 'current_day' in args:
        current_day = int(args.get('current_day'))
        days_since = calendar.days_since(calendar.campaign_start)
        calendar.advance_days(current_day - days_since)

    display_date = calendar.today
    display_options = create_select_data(['Schedule', 'Week', 'Month', 'Year'])
    display_template = args.get('display_mode', 'schedule')
    if args.get('prev_month') or args.get('next_month'):
        if args.get('prev_month'):
            display_date = calendar.today - calendar.today.day - 1
        if args.get('next_month'):
            dim = calendar.get_days_in_months(calendar.today.month-1)
            display_date = calendar.today + (dim - calendar.today.day + 1)
        if display_date.day > 1:
            display_date -= display_date.day - 1
        display_template = 'month'

    update_selected(display_options, display_template)

    data_dict = {
        'display_date': str(display_date),
        'display_options': display_options,
        'display_template': display_template,
        'calendar': {
            'campaign_start': calendar.campaign_start.descr_format(),
            'current_day': calendar.days_since(calendar.campaign_start),
            'days_passed': max(0, calendar.days_since(calendar.campaign_start)-1),
            'age' : display_date.era,
            'year': display_date.year,
            'month': calendar.get_months(display_date.month-1)
        }
    }

    print(display_date)

    if display_template == 'schedule':
        construct_schedule_data(data_dict, calendar, display_date)
    elif display_template == 'week':
        construct_week_data(data_dict, calendar, display_date)
    elif display_template == 'month':
        construct_month_data(data_dict, calendar, display_date)
    elif display_template == 'year':
        construct_year_data(data_dict, calendar, display_date)

    print(data_dict)

    return render_template('dnd/calendar.html',
                           favicon='dnd/calendar_b',
                           title='Hass.io Web | D&D | Calendar',
                           scripts=['dnd'],
                           **data_dict)


@app.route('/dnd/calendar/schedule/<int:year>/<int:month>/<int:day>', methods=[HttpMethods.GET, HttpMethods.POST])
def dnd_calendar_schedule(year, month, day):
    # TODO: Implement
    pass


def _validate_code(code: str):
    if not code or not code.strip():
        return render_template('surprise/invalid.html', title='Hass.io Web | Invalid code', scripts=['surprise'])

    if not Surprise.is_valid_code(code):
        return render_template('surprise/invalid.html', title='Hass.io Web | Invalid code', scripts=['surprise'], invalid_code=code)

    if not Surprise.is_unlocked_code(code):
        date = Surprise.get_unlock_date_for_code(code)
        return render_template('surprise/locked.html', title='Hass.io Web | Locked code', scripts=['surprise'], locked_code=code, unlock_date=date.strftime(Surprise.DATE_FORMAT))


@app.route('/surprise', methods=[HttpMethods.GET, HttpMethods.POST])
def surprise():
    if HttpMethods.is_get(request.method):
        return render_template('surprise/index.html', title='Hass.io Web | Surprise!', scripts=['surprise'])

    code = request.form.get('input_code')
    result = _validate_code(code)
    if result:
        return result

    return redirect(url_for('surprise_code', code=code))


@app.route('/surprise/<string:code>', methods=[HttpMethods.GET])
def surprise_code(code: str):
    result = _validate_code(code)
    if result:
        return result

    return render_template('surprise/code.html', title=f'Hass.io Web | {Surprise.get_title_for_code(code)}', scripts=['surprise'], code=code)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8000, debug=True)  # Run locally in debug
    import sys
    print((
        'This module is not meant to be run directly. '
        'Run the ´server´ module instead using ´python server.py´'
    ))
    sys.exit(1)
