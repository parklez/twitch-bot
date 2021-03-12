"""
TODO
- (Maybe some information about being live or not)
- Accounts Button
- Settings Button
- Plugins Button
- Volume Slider
"""
import tkinter
from parky_bot.gui.themes.default import Theme


class ButtonBar(tkinter.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.button1 = tkinter.Button(self, text='Account', bg=Theme.BUTTON_BG, fg=Theme.HL)
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button2 = tkinter.Button(self, text='Settings', bg=Theme.BUTTON_BG, fg=Theme.HL)
        self.button2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.button3 = tkinter.Button(self, text='Plugins', bg=Theme.BUTTON_BG, fg=Theme.HL)
        self.button3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        #https://pt.stackoverflow.com/questions/343574/como-inicializar-essa-fun%C3%A7%C3%A3o-de-photoimage-do-tkinter
        self.vol_emote = "iVBORw0KGgoAAAANSUhEUgAAACQAAAAfCAYAAACPvW/2AAAABGdBTUEAALGPC/xhBQAA\
            AAlwSFlzAAAOwgAADsIBFShKgAAAABh0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMS42/U4J6AAABGhJRE\
            FUWEe1l21sU1UYx/cKHXW0dF0HzHV27qUZbIgJbgvVKQlqwouhom4VX+Jw4rIgk85BfKuorCZoYEi2obBI\
            ZDHrQqLwZTMLvmRE6zSAgQTly0wwfjIQDQQS8/g8T8853Hantx0pT/JL+/zvOff8ent7720WANwyWH3Ifw\
            g1RjbrxqeDNkwHrAGDQCIv6+YQWB5krW4boQ1TgfUJwouHQiEIh8OM3W7nDNmaZB7JXBFjVmjH6EIzsA6J\
            HUJPTw9MTk7C8PAwYxDarplHMn+K7QSJeWeMSwzMwOoXO2OZqampZEI7EuaRzEXelp0DOZZ5ctx5ZG7cWG\
            NjBtZ+sRPo7u5mGROhnYZ5pcgZkYM38iNUf/6tHEf0xa1jmGhBViL3a9iL8A46OzuVTCohLJI5JzJwrHsa\
            lp+9xpS90SfHEg/HCWEdMGxMSltbW5yMmRBCMpdFryh9dbeSWvDoEzI/rYSw6FqiJiQjEAjMkDER6jXOrT\
            5yEha271D93f1fspB3NKoyZIMUukSBz+eDrq4uCAaDfI4kMjExMRshhfvdg+qI2Fat5+yOe1eqzPlkuxwb\
            kUIctLS0aEUktyqUO98Oy6J/8+I1X5xSefnuw5xVHR43jncisSaTQtm5ebBk7DewVNZy73jsmZtHZGMbZ/\
            bVG1SWZy/iDOlAMi9EP+3Ypx+TC0HFvhHOKvaOcJ9jKYDlZ65y5lgbkOP2IJkXsq/2q08/3/cIZ0X+57m/\
            5+creARzOas5+h1nC1/ayT1yDIkJtba2akUksz2H6BdEi7me28Z9QU2dkpyzqIwzz56j3Je9uV/OO43cHq\
            Hy9z/lxdy7Brifs8ithKz193FWGgxzX9E3KufRdev2CFUOHOfFFne9x/3c8iolJE92d6if+7t6h+S8aSTz\
            Qtn5+VB3cpoXc6zfxBm9SiH5q6ocPME9Xb2Fxykk80Lutw+oxeXRWLz1He5rj/8qF4far85yVrypU2ajSO\
            aFnE+1xz759l7uc+ZZYenXF2NZ8APOCqpvnuTWZY2cIfuQzAsRrmdfUe/pVyQXL6haylnJ5m7u6775Q41D\
            HkeyblDj9/u1IpLZCklsD65RMmVvfazyJWMXOKNbiMim5b2MH54cDgc0NjbG0dTUxDfd5uZmGBwcnI3Q7+\
            JVfX3131+CvCIXZyUvvqYkrXUr5JxdUmiVCEyxWq0wNDSUrtA25IScWxzogMKGh/i9pcKrbrbGI4ZUspCw\
            qkfoIe0nwRTyC0JXTjqC1xEoLCyESCSSjlCH2O9nold4R36IHbHJvyC/5E6Zh2m8EkoF1gPIVZpss9lgfH\
            w8lZD6o4j1kcji7vry2Qi5gGSr8fJNKrBI6h+Ez7doNGom9ELC3JDIobh1i/G6Q/jjxhqbVGDRAz8/Jzud\
            zrSFxNzXxTYjH84YlxikAov+mfC/T5fLlbaQmEsP/3LMEe0YXZgKLJL6l3bs8XigoaGBoV6gFSKw6Os7pt\
            tGaMN0wPIh1xApYSSpkDmQ9T+RwWlXgHWgoAAAAABJRU5ErkJggg=="
        self.vol_img = tkinter.PhotoImage(data=self.vol_emote)
        self.vol_img_label = tkinter.Label(self, image=self.vol_img, bg=Theme.BAR_BG)
        self.vol_img_label.grid(row=0, column=3, padx=(10, 0), sticky='EW')

        self.vol_meter = tkinter.Scale(self, orient=tkinter.HORIZONTAL,
                                       bg=Theme.SLIDER_BG,
                                       fg=Theme.HL,
                                       activebackground=Theme.SLIDER_ACTIVE_BG,
                                       troughcolor=Theme.SLIDER_SLIDE_BG,
                                       highlightbackground=Theme.SLIDER_HL_BG)
        self.vol_meter.grid(row=0, column=4, padx=10, sticky='EW')

        self.columnconfigure(4, weight=1)
