/* Base Ingredient Change Event */
const TYPE_POTION = 'Potion'
const TYPE_POISON = 'Poison'
const TYPE_ENCHANTMENT = 'Enchantment'

var _previous_concoction_was_enchantment = null

window.onload = (event) => {
  if (window.location.pathname.includes('alchemy')) {
    _change_element_display('ingredient_1_root', 'flex')
    on_base_ingredient_change(document.getElementById('base_ingredient'))
  }
}

function on_base_ingredient_change(sender) {
  var text = sender.options[sender.selectedIndex].text
  var types = text.split('-')[1].trim().replace(/[\(\)]/gi, '').split(',')
  types.forEach(function(item, index) {
    this[index] = this[index].trim()
  }, types)

  var is_enchantment = types.includes(TYPE_ENCHANTMENT)
  if (is_enchantment != _previous_concoction_was_enchantment) {
    var display_state = is_enchantment ? 'none' : 'flex'
    _change_element_display('ingredient_2_root', display_state)
    _change_element_display('ingredient_3_root', display_state)
  }

  _previous_concoction_was_enchantment = is_enchantment
}

function _change_element_display(id, state) {
  var element = document.getElementById(id)

  var classes = []
  for (var i = 0; i <= element.classList.length; i++) {
      if (/d-.*/.test(element.classList[i])) {
          classes.push(element.classList[i])
      }
  }

  classes.forEach(function(item, index) {
    element.classList.remove(item)
  })

  element.classList.add('d-' + state)
}

/* Current Day Change Event */
var _prev_current_day = -1

function on_current_day_focusout(sender) {
  if (sender.value == _prev_current_day) {
    _prev_current_day = sender.value
    return
  }
  _prev_current_day = sender.value
  var display_mode_dropdown = document.getElementById('display_mode')
  var current_display_mode = display_mode_dropdown.options[display_mode_dropdown.selectedIndex].value
  var current_day_form = document.getElementById('current_day_form')
  $("<input />").attr("type", "hidden")
          .attr("name", "display_mode")
          .attr("value", current_display_mode)
          .appendTo(current_day_form);
  current_day_form.submit()
}
