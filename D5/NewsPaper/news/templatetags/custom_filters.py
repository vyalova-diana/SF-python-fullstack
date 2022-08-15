from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    if isinstance(value, str):
        list_of_stop_words = ["profanity", "curse", "ругательство", "мат"]
        split_str = value.split()
        filtered_str = ' '.join((filter(lambda s: s not in list_of_stop_words, split_str)))
        return str(filtered_str)
    else:
        raise ValueError(f'Нельзя применить цензуру к данному типу: {type(value)}')
