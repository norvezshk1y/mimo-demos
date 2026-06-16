from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Point, GraphicException
from random import random
from math import sqrt
from glob import glob
from os.path import join, dirname
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.logger import Logger


class MainScreen(Screen):
    pass


class ShowcaseScreen(Screen):
    value = NumericProperty(0)
    active_demo = 'buttons'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._setup, 0)

    def _setup(self, dt):
        self.switch_demo('buttons')

    def switch_demo(self, name):
        self.active_demo = name
        content = self.ids.get('showcase_content')
        if not content:
            return
        content.clear_widgets()
        builder = self._get_demo_builder(name)
        if builder:
            content.add_widget(builder())

    def _get_demo_builder(self, name):
        builders = {
            'buttons': self._build_buttons,
            'sliders': self._build_sliders,
            'textinput': self._build_textinput,
            'switch_toggle': self._build_switch_toggle,
            'progress': self._build_progress,
        }
        return builders.get(name)

    def _build_buttons(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.togglebutton import ToggleButton

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text='Buttons', font_size='18sp', size_hint_y=None, height=40, bold=True)
        box.add_widget(label)

        row1 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        row1.add_widget(Button(text='Button', font_size='14sp'))
        row1.add_widget(Button(text='Pressed', font_size='14sp', state='down'))
        toggle = ToggleButton(text='Toggle\n' + 'normal', font_size='14sp', halign='center')
        toggle.bind(state=lambda inst, val: setattr(inst, 'text', f'Toggle\n{val}'))
        row1.add_widget(toggle)
        box.add_widget(row1)

        row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        for letter in 'ABC':
            row2.add_widget(ToggleButton(text=f'Group {letter}', group='demo_group', font_size='14sp'))
        box.add_widget(row2)

        return box

    def _build_sliders(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.slider import Slider
        from kivy.uix.label import Label

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text='Sliders', font_size='18sp', size_hint_y=None, height=40, bold=True)
        box.add_widget(label)

        row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        s1 = Slider(min=0, max=100, value=33, size_hint_x=0.7)
        s2 = Slider(min=0, max=100, value=66, orientation='vertical', size_hint_x=0.3)
        row.add_widget(s1)
        row.add_widget(s2)
        box.add_widget(row)

        return box

    def _build_textinput(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.label import Label

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text='Text Input', font_size='18sp', size_hint_y=None, height=40, bold=True)
        box.add_widget(label)
        box.add_widget(TextInput(text='Enter text here...', size_hint_y=None, height=45, font_size='14sp'))
        box.add_widget(TextInput(text='', hint_text='Password field', password=True, size_hint_y=None, height=45, font_size='14sp'))

        return box

    def _build_switch_toggle(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.switch import Switch
        from kivy.uix.togglebutton import ToggleButton
        from kivy.uix.label import Label

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text='Switch & Toggle', font_size='18sp', size_hint_y=None, height=40, bold=True)
        box.add_widget(label)

        row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        row.add_widget(Switch(size_hint_x=0.5))
        row.add_widget(Switch(active=True, size_hint_x=0.5))
        box.add_widget(row)

        row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        for letter in 'XYZ':
            row2.add_widget(ToggleButton(text=f'Toggle {letter}', font_size='14sp'))
        box.add_widget(row2)

        return box

    def _build_progress(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.progressbar import ProgressBar
        from kivy.uix.label import Label
        from kivy.clock import Clock

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text='Progress Bar', font_size='18sp', size_hint_y=None, height=40, bold=True)
        box.add_widget(label)

        pb = ProgressBar(value=0, max=100, size_hint_y=None, height=30)
        box.add_widget(pb)

        def update_progress(dt):
            pb.value = (pb.value + 1) % 101

        Clock.schedule_interval(update_progress, 0.05)

        return box


class TouchtracerWidget(FloatLayout):

    def on_touch_down(self, touch):
        win = self.get_parent_window()
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        with self.canvas:
            ud['color'] = Color(random(), 1, 1, mode='hsv', group=g)
            ud['lines'] = (
                Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                Point(points=(touch.x, touch.y), source='particle.png',
                      pointsize=5, group=g))

        ud['label'] = Label(size_hint=(None, None))
        self.update_touch_label(ud['label'], touch)
        self.add_widget(ud['label'])
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        ud = touch.ud
        ud['lines'][0].pos = touch.x, 0
        ud['lines'][1].pos = 0, touch.y

        points = ud['lines'][2].points
        oldx, oldy = points[-2], points[-1]
        points = self.calculate_points(oldx, oldy, touch.x, touch.y)
        if points:
            try:
                lp = ud['lines'][2].add_point
                for idx in range(0, len(points), 2):
                    lp(points[idx], points[idx + 1])
            except GraphicException:
                pass

        ud['label'].pos = touch.pos
        import time
        t = int(time.time())
        if t not in ud:
            ud[t] = 1
        else:
            ud[t] += 1
        self.update_touch_label(ud['label'], touch)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['group'])
        self.remove_widget(ud['label'])

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20

    @staticmethod
    def calculate_points(x1, y1, x2, y2, steps=5):
        dx = x2 - x1
        dy = y2 - y1
        dist = sqrt(dx * dx + dy * dy)
        if dist < steps:
            return None
        o = []
        m = dist / steps
        for i in range(1, int(m)):
            mi = i / m
            lastx = x1 + dx * mi
            lasty = y1 + dy * mi
            o.extend([lastx, lasty])
        return o


class TouchtracerScreen(Screen):
    pass


class Picture(Scatter):
    source = None


class PicturesScreen(Screen):
    def on_enter(self):
        self.load_pictures()

    def load_pictures(self):
        root = self.ids.pictures_root
        root.clear_widgets()
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'images', '*')):
            try:
                picture = Picture(source=filename, rotation=int(random() * 60 - 30))
                root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)


class KivyDemosApp(App):
    title = 'Kivy Demos'
    icon = 'icon.png'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ShowcaseScreen(name='showcase'))
        sm.add_widget(TouchtracerScreen(name='touchtracer'))
        sm.add_widget(PicturesScreen(name='pictures'))
        return sm

    def on_pause(self):
        return True


if __name__ == '__main__':
    KivyDemosApp().run()
