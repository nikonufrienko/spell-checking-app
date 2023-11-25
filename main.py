from utils.text_capture import start_capture_daemon
import subprocess
from utils.spelling import SpellCorrector
from utils.cfg import Settings

corrector = None


def print_corrected(original_str):
    print("!")
    global corrector
    modified_str = corrector.predict(original_str)
    args = ['-i', original_str, '-c', modified_str]
    print("Processing...")
    subprocess.run(["python", "display_results.py"] + args, check=True)


if __name__ == '__main__':
    settings = Settings('spellchecker.cfg')
    print('Loading model...')
    corrector = SpellCorrector(
        './models/' + settings.model.replace('/', '_'),
        device=settings.device,
        max_time=settings.max_time
    )
    print('Done')

    start_capture_daemon(handler=print_corrected)
