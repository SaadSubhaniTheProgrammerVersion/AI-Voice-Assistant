from espeakng import ESpeakNG

esng = ESpeakNG()
esng.voice = 'en'
esng.speed = 150  # Speed of speech in words per minute. 80 to 450. Default is 175.
esng.pitch = 50  # Base pitch, range 0-100. Default is 50.
esng.volume = 200  # Volume in range 0-200 or more. However, large values will distort sound output.

text = "Hello, how are you?"
esng.say(text)
