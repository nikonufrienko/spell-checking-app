from utils.spelling import SpellCorrector
import torch


if __name__ == '__main__':
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    print('Loading model...')

    corrector = SpellCorrector(
        './models/UrukHan_t5-russian-spell',
        device=device
    )

    while True:
        seq = input('Input:')
        print('Spell correct: %s' % corrector.predict(seq))
