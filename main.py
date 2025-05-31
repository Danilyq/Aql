from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

def calculate_sample_size(order_size):
    if order_size <= 1:
        return 0
    elif 2 <= order_size <= 8:
        return 2
    elif 9 <= order_size <= 15:
        return 3
    elif 16 <= order_size <= 25:
        return 5
    elif 26 <= order_size <= 50:
        return 8
    elif 51 <= order_size <= 90:
        return 13
    elif 91 <= order_size <= 150:
        return 20
    elif 151 <= order_size <= 280:
        return 32
    elif 281 <= order_size <= 500:
        return 50
    elif 501 <= order_size <= 1200:
        return 80
    elif 1201 <= order_size <= 3200:
        return 125
    elif 3201 <= order_size <= 10000:
        return 200
    elif 10001 <= order_size <= 35000:
        return 315
    elif 35001 <= order_size <= 150000:
        return 500
    elif 150001 <= order_size <= 500000:
        return 1250
    elif order_size > 500000:
        return 2000
    else:
        return 0

def calculate_defect_percentage(defect_count, order_size):
    try:
        return (defect_count / order_size) * 100
    except ZeroDivisionError:
        return 0

def calculate_adjusted_sample(order_size, sample_size, defect_percentage):
    if sample_size == 0 or defect_percentage == 0:
        return sample_size
    elif defect_percentage <= 3:
        return min(order_size, int(sample_size + order_size * 0.10))
    elif 3 < defect_percentage <= 10:
        return min(order_size, int(sample_size + order_size * 0.50))
    else:
        return order_size

class AQLCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.add_widget(Label(text="Размер заказа:"))
        self.order_input = TextInput(multiline=False, input_filter='int')
        self.add_widget(self.order_input)

        self.add_widget(Label(text="Количество брака:"))
        self.defect_input = TextInput(multiline=False, input_filter='int')
        self.add_widget(self.defect_input)

        self.calc_button = Button(text="Рассчитать")
        self.calc_button.bind(on_press=self.process_inputs)
        self.add_widget(self.calc_button)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

    def process_inputs(self, instance):
        try:
            order = int(self.order_input.text)
            defects = int(self.defect_input.text) if self.defect_input.text.strip() else 0

            sample = calculate_sample_size(order)
            defect_percent = calculate_defect_percentage(defects, order)
            adjusted = calculate_adjusted_sample(order, sample, defect_percent)

            result = f"Размер выборки: {sample}\nПроцент брака: {defect_percent:.2f}%\n"
            if adjusted > sample:
                result += f"Выборка увеличена до: {adjusted}"
            else:
                result += f"Окончательная выборка: {adjusted}"
            self.result_label.text = result
        except:
            self.result_label.text = "Ошибка ввода!"

class AQLApp(App):
    def build(self):
        return AQLCalculator()

if __name__ == "__main__":
    AQLApp().run()
