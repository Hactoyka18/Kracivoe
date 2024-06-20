import threading
import pygame
import time
from .object import Text

class Game():
    '''
    Класс системы платформера
    '''
    def __init__(self, width, height, caption="Game", fps=60):
        self.scripts = {}  # Словарь для хранения запущенных сценариев
        self.events = {}  # Словарь для хранения запущенных event`ов сценариев
        self.states = {}  #Словарь для хранения текущего состояния?
        self.current_state = None # текущее состояние
        self.objects = [] # список объектов игры
        pygame.init()
        self.display_surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.frame_time = 1.0 / fps
        pygame.display.set_caption(caption)

    def add_object(self, obj):
        '''
        Добавить объект obj в игру
        '''
        self.objects.append(obj)

    def remove_object(self, obj):
        '''
        Удалить объект obj
        '''
        self.objects.remove(obj)
        
    def clear(self):
        '''
        Удалить все игровые объекты
        '''
        self.objects = []

    def key_pressed(self, key):
        '''
        Возвращает True если была нажата клавиша key, иначе False
        '''
        return pygame.key.get_pressed()[key]

    def new_state(self, name, first_func, func):
        '''
        Создать новое игровое состояние

        :param name: имя состояния
        :param first_func: функция, которая запускается при переключении в это игровое состояние
        :param func: функция, которая работает каждый кадр в этом игровом состянии
        '''
        self.states[name] = (first_func, func)

    def set_state(self, name):
        '''
        Переключиться в игровое состояние

        :param name: имя состояния
        '''
        if self.current_state is not None:
            self.stop_script(self.current_state)
        s = self.states[name]
        s[0]()
        self.start_script(s[1], name)
        self.current_state = name

    def run(self):
        '''
        Главный цикл игры
        '''
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.display_surface.fill((0, 0, 0))
            for o in self.objects:
                o.update()
            for o in self.objects:
                if type(o) == Text:
                    self.render_text(o)
                else:
                    self.display_surface.blit(o.surf, o.rect)
            pygame.display.flip()
            self.clock.tick(self.fps)
        self.stop_script(self.current_state)
        pygame.quit()

    def render_text(self, text):
        '''
        Отрисовка текстового объекта text
        '''
        f = pygame.font.SysFont(text.font, text.size)
        g = f.render(text.text, True, text.color)
        self.display_surface.blit(g, (text.x, text.y))

    def get_collision(self, obj, obj_type):
        '''
        Получить список объектов столкновения

        :param obj: объект, с которым проверяется столкновение
        :param obj_type: тип объектов, которые будут проверяться
        :return: список объектов, с которыми столкнулся заданный объект
        '''
        list = []
        for o in self.objects:
            if o != obj and type(o) == obj_type and pygame.sprite.collide_rect(o, obj):
                list.append(o)
        return list

    def get_objects(self, obj_types):
        '''
        Получить список объектов заданного типа

        :param obj_types: список требуемых типов
        :return: список объектов
        '''
        list = []
        for o in self.objects:
            for obj_type in obj_types:
                if type(o) == obj_type:
                    list.append(o)
        return list

    def start_script(self, script_function, script_name, *args):
        '''
        Запускает сценарий в отдельном потоке с возможностью остановки и передачи аргументов.

        :param: script_function: функция, содержащая код сценария
        :param: script_name: имя сценария
        :param: args: дополнительные аргументы, которые передаются в сценарий
        '''
        e = threading.Event()
        self.events[script_name] = e

        def func(e, args):
            while not e.is_set():
                script_function(*args)
                time.sleep(self.frame_time)

        script_thread = threading.Thread(target=func, args=(e, args))
        script_thread.daemon = True
        script_thread.start()
        self.scripts[script_name] = script_thread

    def stop_script(self, script_name):
        '''
        Останавливает сценарий по имени

        :param: script_name: имя сценария, который нужно остановить
        '''
        if script_name in self.scripts:
            self.events[script_name].set()
            del self.scripts[script_name]
            del self.events[script_name]
        else:
            # Если сценарий не существует
            print(f"Сценарий {script_name} не существует.")
