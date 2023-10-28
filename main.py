# TODO[nikonufrienko]: Add GUI implementation
from utils.text_capture import start_capture_daemon
from utils.spelling import SpellCorrector
import torch

corrector = None


def print_corrected(text):
    global corrector
    print("Processing...")
    print(corrector.predict(text))


if __name__ == '__main__':
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    print('Loading model...')
    corrector = SpellCorrector(
        './models/UrukHan_t5-russian-spell',
        device=device
    )
    print('Done')

    start_capture_daemon(handler=print_corrected)
