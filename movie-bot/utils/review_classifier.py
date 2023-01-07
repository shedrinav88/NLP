import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
import random

answers = {'positive': ['Спасибо за отзыв! Я так и думал, что тебе понравится!',
                        'Да, согласен, хороший фильм, спасибо тебе за отзыв',
                        'Знаешь, согласен с тобой, хорошее кино. Спасибо за отзыв'
                        'Спасибо за такой подробный отзыв! Действительно, очень хороший фильм :)'],
           'negative': ['Да согласен, фильм неудачный. Спасибо за отзыв!',
                        'Спасибо, что поделился своим мнением, мне тоже не очень понравился фильм',
                        'Спасибо за твое мнение. Солидарен с тобой',
                        'Спасибо за такой подробный отзыв! Я тоже считаю, что фильм мог бы быть и получше']}

tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment')
model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment',
                                                           return_dict=True)


def classify_review(review_text):
    # подготовка входа
    # input = tokenizer.encode(review_text, return_tensors='pt')
    inputs = tokenizer(review_text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()

    if predicted == 1:
        if len(review_text) < 40:
            return ''.join(random.sample(answers['positive'][:-1], k=1))
        else:
            return ''.join(answers['positive'][-1])

    elif predicted == 2:
        if len(review_text) < 40:
            return ''.join(random.sample(answers['negative'][:-1], k=1))
        else:
            return ''.join(answers['negative'][-1])
    else:
        return 'Спасибо за твой отзыв!)'
