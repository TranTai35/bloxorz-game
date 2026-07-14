from ursina import Ursina, window

from app_controller import AppController


app = Ursina()

window.title = "Bloxorz Solver"
window.borderless = False
window.fullscreen = False

controller = AppController()

app.run()