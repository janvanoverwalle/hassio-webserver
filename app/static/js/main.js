/* Theme Switch */
const THEME_DARK = 'dark'
const THEME_LIGHT = 'light'
const toggle_switch = document.querySelector('.theme-switch input[type="checkbox"]');
const current_theme = localStorage.getItem('theme');

if (current_theme) {
  document.documentElement.setAttribute('data-theme', current_theme);
  if (current_theme === THEME_DARK) {
    toggle_switch.checked = true;
  }
}

if (toggle_switch) {
  toggle_switch.addEventListener('change', switch_theme, false);
}

function switch_theme(e) {
  if (e.target.checked) {
    document.documentElement.setAttribute('data-theme', THEME_DARK);
    localStorage.setItem('theme', THEME_DARK);
  }
  else {
    document.documentElement.setAttribute('data-theme', THEME_LIGHT);
    localStorage.setItem('theme', THEME_LIGHT);
  }
}

/* Ingredient Change event */
const TYPE_POTION = 'Potion'
const TYPE_POISON = 'Poison'
const TYPE_ENCHANTMENT = 'Enchantment'

var _ingredients = null
var _previous_concoction_type = null

function _get_selected_ingredient(select) {
  if (_ingredients == null) {
    console.error('Ingredients list is empty')
    return null
  }

  var selected_ingredient = null
  for (var i = 0; i < _ingredients.length; i++) {
    if (select.value == _ingredients[i].id) {
      selected_ingredient = _ingredients[i]
      break
    }
  }

  return selected_ingredient
}

function on_ingredient_change(sender, ingredients) {
  // Assumed that 'sender' is a 'select' element
  if (_ingredients == null) {
    _ingredients = ingredients
  }

  selected_ingredient = _get_selected_ingredient(sender)

  if (selected_ingredient.function == 'Effect') {
    _on_base_ingredient_change(selected_ingredient)
  }
  else {
    _on_modifier_ingredient_change(selected_ingredient)
  }
}

function _on_base_ingredient_change(selected_ingredient) {
  console.log('Concoction type: ' + selected_ingredient.type)

  if (selected_ingredient.type != _previous_concoction_type) {
    var display_state = selected_ingredient.type.includes(TYPE_ENCHANTMENT) ? 'none' : 'flex'

    _change_element_display('ingredient_2_root', display_state)
    _change_element_display('ingredient_3_root', display_state)

    _update_modifier_ingredient_options(selected_ingredient)
  }

  _previous_concoction_type = selected_ingredient.type
}

function _on_modifier_ingredient_change(selected_ingredient) {
  console.log(selected_ingredient)
}

function _update_modifier_ingredient_options(selected_ingredient) {
  var type = selected_ingredient.type

  for (var i = 1; i < (type.includes(TYPE_ENCHANTMENT) ? 1 : 3)+1; i++) {
    var select_name = 'ingredient_' + i
    var options_str = '';
    for (var j = 0; j < _ingredients.length; j++) {
      if (_ingredients[j].function != null && _ingredients[j].function == 'Effect') {
        if (!(selected_ingredient.id == 0 && _ingredients[j].type.includes(TYPE_POTION))) {
          continue
        }
      }
      if ((type.filter(value => _ingredients[j].type.includes(value))).length <= 0) {
        continue
      }
      options_str += '<option value="' + _ingredients[j].id + '">' + _ingredients[j].name + '</option>';
    }
    $('select[name="' + select_name + '"]').find('option').remove().end().append($(options_str));
  }
}

function _change_element_display(id, state) {
  document.getElementById(id).style.display = state;
}
