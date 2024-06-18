import threading
import pygame
import time

class Game():
    def __init__(self, width, height, caption="Game", fps=60):
        '''
        Класс системы управления игрой
        '''
        self.scripts = {}  # Словарь для хранения запущенных сценариев
        self.events = {}  # Словарь для хранения запущенных event`ов сценариев
        self.states = {}  #Словарь для хранения текущего состояния?
        self.current_state = None
        pygame.init()
        self.display_surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.frame_time = 1.0 / fps
        pygame.display.set_caption(caption)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects = []

    def key_pressed(self, key):
        return pygame.key.get_pressed()[key]

    def new_state(self, name, first_func, func):
        self.states[name] = (first_func, func)

    def set_state(self, name):
        if self.current_state is not None:
            self.stop_script(self.current_state)
        s = self.states[name]
        s[0]()
        self.start_script(s[1], name)
        self.current_state = name

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.display_surface.fill((0, 0, 0))
            for o in self.objects:
                o.update()
            for o in self.objects:
                self.display_surface.blit(o.surf, o.rect)
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

    def get_collision(self, obj):
        list = []
        for o in self.objects:
            if o != obj and pygame.sprite.collide_rect(o, obj):
                list.append(o)
        return list

    def start_script(self, script_function, script_name, *args):
        '''
        Запускает сценарий в отдельном потоке с возможностью остановки и передачи аргументов.

        :param: script_function: Функция, содержащая код сценария.
        :param: script_name: Имя сценария.
        :param: args: Дополнительные аргументы, которые нужно передать в сценарий.
        '''
        # Создание потока для сценария
        e = threading.Event()
        self.events[script_name] = e

        def func(e, args):
            while not e.is_set():
                script_function(*args)
                time.sleep(self.frame_time)

        # Создание потока для сценария
        script_thread = threading.Thread(target=func, args=(e, args))
        script_thread.daemon = True
        script_thread.start()

        # Добавление потока в словарь активных сценариев
        self.scripts[script_name] = script_thread

    def stop_script(self, script_name):
        '''
        Останавливает сценарий по имени

        :param: script_name: имя сценария, который нужно остановить
        '''
        # Проверка существования сценария
        if script_name in self.scripts:
            # Если сценарий существует, прерываем его выполнение
            self.events[script_name].set()
            # Убираем сценарий из словаря активных сценариев
            del self.scripts[script_name]
            del self.events[script_name]
            print(f"Сценарий {script_name} остановлен.")
        else:
            # Если сценарий не существует
            print(f"Сценарий {script_name} не существует.")