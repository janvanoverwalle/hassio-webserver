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
