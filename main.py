from utils.text_capture import start_capture_daemon
import subprocess
from utils.spelling import SpellCorrector
import torch

corrector = None


def print_corrected(original_str):
    print("!")
    global corrector
    modified_str = corrector.predict(original_str)
    args = ['-i', original_str, '-c', modified_str]
    subprocess.run(["python", "display_results.py"] + args, check=True)


if __name__ == '__main__':
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    print('Loading model...')
    corrector = SpellCorrector(
        './models/UrukHan_t5-russian-spell',
        device=device
    )
    print('Done')

    start_capture_daemon(handler=print_corrected)
