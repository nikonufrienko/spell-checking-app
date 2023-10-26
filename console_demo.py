from utils.spelling import SpellCorrector

corrector = SpellCorrector("./models/UrukHan_t5-russian-spell")

while True:
    seq = [input('Input:')]
    print("Spell correct: %s" % corrector.predict(seq)[0])
