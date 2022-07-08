from kivy.app import App
from kivy.uix.widget import Widget

from settings import *

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.colorpicker import ColorPicker

from kivy.graphics import (Color, Line, Ellipse)
from kivy.uix.button import Button
from kivy.uix.slider import Slider


class ColorChange(GridLayout):
    def __init__(self, **kwargs):
        super(ColorChange, self).__init__(**kwargs)

        self.cols = 1

        self.clr_picker = ColorPicker(color=color_value)
        self.add_widget(self.clr_picker)
        self.clr_picker.bind(color=self.on_color)

    @staticmethod
    def on_color(instance, value):
        global color_value
        color_value = instance.color


class BrushSlider(GridLayout):
    def __init__(self, **kwargs):
        super(BrushSlider, self).__init__(**kwargs)

        self.cols = 3

        self.brushControl = Slider(min=1, max=100, value=rad, step=1)

        self.add_widget(Label(text='Size'))
        self.add_widget(self.brushControl)

        self.brushValue = Label(text=str(rad))
        self.add_widget(self.brushValue)

        self.brushControl.bind(value=self.on_value_change)

    def on_value_change(self, instance, amount):
        global rad
        self.brushValue.text = "% d" % amount
        rad = amount


class PainterWidget(Widget):
    def __init__(self, **kwargs):
        super(PainterWidget, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*color_value)
            Ellipse(pos=(touch.x - rad / 2, touch.y - rad / 2), size=(rad, rad))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=rad / 2)

    def on_touch_move(self, touch):
        touch.ud['line'].points += (touch.x, touch.y)


class PaintApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.painter = PainterWidget()

    def build(self):
        parent = Widget()

        parent.add_widget(self.painter)
        parent.add_widget(Button(text='Clear', size=btn_size, pos=(0, 0), on_press=self.clear_func))
        parent.add_widget(Button(text='Brush size', size=btn_size, pos=(100, 0), on_press=self.width_func))
        parent.add_widget(Button(text='Color', size=btn_size, pos=(200, 0), on_press=self.color))
        parent.add_widget(Button(text='Save', size=btn_size, pos=(300, 0), on_press=self.save))

        return parent

    def clear_func(self, instance):
        self.painter.canvas.clear()

    @staticmethod
    def width_func(instance):
        content = BrushSlider()
        popup = Popup(title='Brush size', content=content, size_hint=(None, None), size=(400, 200))
        content.bind(on_press=popup.dismiss)
        popup.open()

    def save(self, instance):
        self.painter.size = (Window.size[0], Window.size[1])
        self.painter.export_to_png('image.png')

    @staticmethod
    def color(instance):
        content = ColorChange()
        popup = Popup(title='Color changer', content=content, size_hint=(None, None), size=(600, 400))
        content.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    PaintApp().run()
