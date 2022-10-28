from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value, arg):
    obscene_words = ['сука', 'хуй', 'пизда', 'блядь']
    post_words = value.split(' ')
    for word in post_words:
        if word.strip('.,!?').lower() in obscene_words:
            post_words.insert(post_words.index(word), arg)
            post_words.remove(word)
    return ' '.join(post_words)
