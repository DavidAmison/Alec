from skybeard.utils import setup_beard

try:
    setup_beard("alec")
except Exception as e:
    print('there was a problem: ' + str(e))
