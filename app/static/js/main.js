/* Theme Switch */
const THEME_DARK = 'dark'
const THEME_LIGHT = 'light'
const toggle_switch = document.querySelector('.theme-switch input[type="checkbox"]')
const current_theme = localStorage.getItem('theme')

if (current_theme) {
  document.documentElement.setAttribute('data-theme', current_theme)
  if (current_theme === THEME_DARK) {
    toggle_switch.checked = true
  }
}

if (toggle_switch) {
  toggle_switch.addEventListener('change', switch_theme, false)
}

function switch_theme(e) {
  if (e.target.checked) {
    document.documentElement.setAttribute('data-theme', THEME_DARK)
    localStorage.setItem('theme', THEME_DARK)
  }
  else {
    document.documentElement.setAttribute('data-theme', THEME_LIGHT)
    localStorage.setItem('theme', THEME_LIGHT)
  }
}

/* Base Ingredient Change event */
const TYPE_POTION = 'Potion'
const TYPE_POISON = 'Poison'
const TYPE_ENCHANTMENT = 'Enchantment'

var _previous_concoction_was_enchantment = null

window.onload = (event) => {
  _change_element_display('ingredient_1_root', 'flex')
  on_base_ingredient_change(document.getElementById('base_ingredient'))
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
