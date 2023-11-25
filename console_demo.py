from utils.spelling import SpellCorrector
from utils.cfg import Settings


if __name__ == '__main__':
    settings = Settings('spellchecker.cfg')
    device = settings.device
    print('Loading model...')

    corrector = SpellCorrector(
        './models/' + settings.model.replace('/', '_'),
        device=device,
        max_time=settings.max_time
    )

    while True:
        seq = input('Input:')
        print('Spell correct: %s' % corrector.predict(seq))
