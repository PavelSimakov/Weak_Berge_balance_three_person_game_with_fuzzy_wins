from tkinter import filedialog, simpledialog, LEFT, SOLID
import tkinter as tk
from tkinter.ttk import Combobox

import numpy as np
import pygambit as gbt
import json

import Library_of_defasification_functions



class ToolTip(object):                      # Всплывающая подсказка (Tooltip)

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):                # Показать подсказку (Show hint)
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=LEFT,
                         background="#ffffe0", relief=SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):             # Создаем всплывающую подсказку
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def callbackFunc(event):                   # Включаем уровень значимости Alfa
    if combo.get() == "Для метода 'Адамо'":
        txt = tk.Entry(root, width=23, textvariable=Alfa)
        txt.grid(column=2, row=1)
    else:
        txt = tk.Entry(root, width=23, textvariable=Alfa, state='disabled')
        txt.grid(column=2, row=1)


def defuzzify_centroid(fuzzy_numbers):

    defuzzification_methods = {
        "Адамо": Library_of_defasification_functions.Adamo,
        "Центр максимумов": Library_of_defasification_functions.CofMax,
        "Центра масс": Library_of_defasification_functions.CofMass,
        "Медианы": Library_of_defasification_functions.Medians,
        "Индекс Чанга": Library_of_defasification_functions.Chang,
        "Возможное среднее": Library_of_defasification_functions.PAv,
        "Индекс Ягера": Library_of_defasification_functions.Jager,
        "USt1": Library_of_defasification_functions.USt1,
    }

    crisp_numbers = []
    for fuzzy_num in fuzzy_numbers:
        numbers = [float(x) for x in fuzzy_num.split(':')]
        if len(numbers) != 3:
            raise ValueError("Нечеткое число должно состоять из трех компонентов (a:b:c)")
        a, b, c = numbers

        method_name = combo1.get()
        method = defuzzification_methods.get(method_name)
        if method:
            if method_name == "Адамо":
                result = method(a, b, c, float(Alfa.get()))
            else:
                result = method(a, b, c)
        else:
            result = "Ошибка: Неверное имя метода"

        crisp_numbers.append(result)
    return np.array(crisp_numbers)


def load_tensor_from_file(filepath):
    """Загружает тензор из файла .txt."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            data = []
            for line in lines:
                row = [x for x in line.strip().split()] # Предполагается, что числа разделены пробелами
                data.append(row)
            return np.array(data)
    except FileNotFoundError:
        return None
    except ValueError:
        print(f"Ошибка: Не удалось преобразовать данные в числовые значения в файле {filepath}")
        return None


def process_files():
    """Загружает файлы, выполняет дефаззификацию и вычисляет решение игры."""
    filepaths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])

    if len(filepaths) != 3:
        result_label.config(text="Выберите три файла!")
        return

    tensors = []
    for filepath in filepaths:
        tensor = load_tensor_from_file(filepath)
        if tensor is None:
            return          # Остановка, если произошла ошибка при загрузке
        tensors.append(tensor)

    crisp_tensors = [defuzzify_centroid(tensor.reshape(-1)) for tensor in tensors]
    crisp_tensors = [tensor.reshape(tensors[0].shape) for tensor in crisp_tensors]

    try:

        dimensions_str = simpledialog.askstring("Размеры матриц", "Введите размеры матриц (например, 3,2,4):",
                                                initialvalue="3,2,4")
        if dimensions_str is None:
            return  # Tсли пользователь отменил ввод данных

        dimensions = tuple(map(int, dimensions_str.split(',')))
        if len(dimensions) != 3:
            raise ValueError("Необходимо указать три измерения")

        if combo1.get() == "Адамо":  # Создаем всплывающую подсказку для каждого метода
            CreateToolTip(combo1,
                          text='Ранжирование происходит с помощью сравнения только правых концов альфа срезов, для определенного значения альфа.\nАльфа (α) при этом является мерой риска неправильного решения, т. е. чем больше альфа, тем меньше риск неправильного решения.')
        elif combo1.get() == "Центр максимумов":
            CreateToolTip(combo1,
                          text='Центр максимумов нечеткого числа вычисляется как среднее значение конечных точек модальных интервалов (максимальных значений принадлежности)')
        elif combo1.get() == "Центра масс":
            CreateToolTip(combo1, text='Выделяет значение, которое является центром масс нечеткого множества.')
        elif combo1.get() == "Медианы":
            CreateToolTip(combo1,
                          text='Находит центр области нечеткого числа, деля кривую функции принадлежности на две равные части.')
        elif combo1.get() == "Индекс Чанга":
            CreateToolTip(combo1, text='Метод основан на предложенном Чангам индексе.')
        elif combo1.get() == "Возможное среднее":
            CreateToolTip(combo1, text='Средневзвешенное значение средних точек альфа разрезов нечеткого числа.')
        elif combo1.get() == "Индекс Ягера":
            CreateToolTip(combo1,
                          text='Этот индекс можно рассмотреть, как обобщение метода ранжирования на основе центра тяжести.')
        elif combo1.get() == "USt1":
            CreateToolTip(combo1,
                          text='Ухоботов В.И., Стабулит И.С., Кудрявцев К.Н.\nСравнение нечетких чисел треугольного вида, Вестник Удмуртского университета.\nМатематика. Механика. Компьютерные науки, 2019, т. 29, вып. 2, с. 197-210')
        else:
            CreateToolTip(combo1, text='')

        t_1 = crisp_tensors[0]
        t_2 = crisp_tensors[1]
        t_3 = crisp_tensors[2]

        t_1 = t_1.reshape(dimensions)
        t_2 = t_2.reshape(dimensions)
        t_3 = t_3.reshape(dimensions)

        A_1 = t_2 + t_3
        B_1 = t_1 + t_3
        C_1 = t_1 + t_2

        g = gbt.Game.from_arrays(A_1, B_1, C_1)
        s = gbt.nash.logit_solve(g)  # or other solver as needed
        equilibria = s.equilibria
        data = json.loads(str(equilibria[0]))
        formatted_rows = []
        for row in data:
            formatted_row = "[" + ", ".join(f"{x:.6f}" for x in row) + "]\n"  # 6 знаков после запятой
            formatted_rows.append(formatted_row)
        formatted_data = "".join(formatted_rows)
        result_label.config(text=f"Равновесия Нэша : \n{formatted_data}")
    except Exception as e:
        result_label.config(text=f"Ошибка при решении игры: {e}")




root = tk.Tk()
root.title("Решение игры")

Alfa = tk.StringVar()

combo = Combobox(root)
combo['values'] = ("Ур. значимости \u03B1", "Для метода 'Адамо'")
combo.current(0)
combo.grid(column=1, row=1)
combo.bind("<<ComboboxSelected>>", callbackFunc)

txt = tk.Entry(root, width=23, textvariable=Alfa, state='disabled')
txt.grid(column=2, row=1)

combo1 = Combobox(root)
combo1['values'] = ("Метод сравнения", "Адамо", "Центр максимумов", "Центра масс", "Медианы", "Индекс Чанга", "Возможное среднее", "Индекс Ягера", "USt1")
combo1.current(0)
combo1.grid(column=2, row=2)

load_button = tk.Button(root, text="Загрузить тензоры выигрыша и решить игру", command=process_files)
load_button.grid(column=2, row=3)

result_label = tk.Label(root, text="")
result_label.grid(column=2, row=4)

root.mainloop()
