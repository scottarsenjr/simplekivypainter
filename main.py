##############################################################

from kivy.app import App
from kivy.uix.widget import Widget

from settings import *

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import (Color, Rectangle, Line, Ellipse)
from kivy.uix.button import Button
from kivy.uix.slider import Slider

##############################################################


# MAIN WIDGET CLASS

class MainWidget(GridLayout):
    pass


# CUSTOM LAYOUT CLASS

class CustomLayout(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(CustomLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(*background_value)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# BACKGROUND COLOR CLASS

class BackgroundColorChange(GridLayout):
    def __init__(self, **kwargs):
        super(BackgroundColorChange, self).__init__(**kwargs)

        self.cols = 1

        self.bg_picker = ColorPicker(color=background_value)
        self.add_widget(self.bg_picker)
        self.bg_picker.bind(color=self.on_color)

    @staticmethod
    def on_color(instance, value):
        global background_value
        background_value = instance.color


# BRUSH COLOR CLASS

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


# BRUSH SIZE CLASS

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


# DRAWING CLASS

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
        self.background = CustomLayout()

    def build(self):

        parent = MainWidget()

        # WIDGETS

        parent.add_widget(self.background)
        parent.add_widget(self.painter)
        parent.add_widget(Button(text='Clear', size=btn_size, pos=(0, 0), on_press=self.clear_func))
        parent.add_widget(Button(text='Brush size', size=btn_size, pos=(100, 0), on_press=self.width_func))
        parent.add_widget(Button(text='Color', size=btn_size, pos=(200, 0), on_press=self.color))
        parent.add_widget(Button(text='Background', size=btn_size, pos=(300, 0),
                                 on_press=self.change_background_color))

        # TODO: MAKE BACKGROUND COLOR CHANGER TO WORK

        parent.add_widget(Button(text='Save', size=btn_size, pos=(400, 0), on_press=self.save))

        return parent

    # BACKGROUND COLOR UPDATE

    @staticmethod
    def change_background_color(instance):
        content = BackgroundColorChange()
        popup = Popup(title='Background Color', content=content, size_hint=(None, None), size=(600, 400))
        content.bind(on_press=popup.dismiss)
        popup.open()

    # CLEAR FUNCTION

    def clear_func(self, instance):
        self.painter.canvas.clear()

    # BRUSH SIZE FUNCTION

    @staticmethod
    def width_func(instance):
        content = BrushSlider()
        popup = Popup(title='Brush size', content=content, size_hint=(None, None), size=(400, 200))
        content.bind(on_press=popup.dismiss)
        popup.open()

    # IMAGE SAVING FUNCTION

    def save(self, instance):
        self.painter.size = (Window.size[0], Window.size[1])
        self.painter.export_to_png('image.png')
        content = Label(text='Image has been successfully saved!')
        popup = Popup(title='Saved', content=content, size_hint=(None, None), size=(400, 200))
        content.bind(on_press=popup.dismiss)
        popup.open()

    # BRUSH COLOR FUNCTION

    @staticmethod
    def color(instance):
        content = ColorChange()
        popup = Popup(title='Brush color changer', content=content, size_hint=(None, None), size=(600, 400))
        content.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    PaintApp().run()
