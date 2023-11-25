from simple_term_menu import TerminalMenu
import torch
import configparser

available_devices = ['cpu']
available_devices += [f'cuda:{i}' for i in range(torch.cuda.device_count())]
available_models = ['UrukHan/t5-russian-spell', 'ai-forever/RuM2M100-1.2B']


def get_device():
    print('Выберете устройство для запуска моделей:')
    terminal_menu = TerminalMenu(available_devices)
    device = available_devices[terminal_menu.show()]
    print(f"Device: {device}")
    return device


def get_ru_model_name():
    print('Выберите модель для Русского языка:')
    terminal_menu = TerminalMenu(available_models)
    model = available_models[terminal_menu.show()]
    print(f"Model: {model}")
    return model


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'device': get_device(),
        'model': get_ru_model_name(),
        'capture_hotkey': '<alt>+y',
        'max_time': 3600
    }
    with open('spellchecker.cfg', 'w') as configfile:
        config.write(configfile)
