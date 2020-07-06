from aiogram import Bot, Dispatcher, executor, types
import random
import nltk
from big_config import BOT_CONFIG
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
X_text = []
y = []
for intent, value in BOT_CONFIG['intents'].items():
    X_text += value['examples']
    y += [intent] * len(value['examples'])
vectorizer = CountVectorizer(analyzer='char_wb',ngram_range=(3, 3),lowercase=True)
X = vectorizer.fit_transform(X_text)
clf = LogisticRegression()
clf.fit(X,y)

def get_intent(text):
    text_vector = vectorizer.transform([text]).toarray()[0]
    probas_list = clf.predict_proba([text_vector])[0]
    probas_list = list(probas_list)
    max_proba = max(probas_list)
    if max_proba > 0.2:

        index = probas_list.index(max_proba)
        return clf.classes_[index]



def response_by_intent(intent):
    responses = BOT_CONFIG['intents'][intent]['responses']
    return random.choice(responses)

def get_failure_phrase():
    failure_phrase = BOT_CONFIG['failure_phrases']

    return random.choice(failure_phrase)
with open("dialogues.txt", encoding="utf-8") as f:
    content = f.read()
blocks = content.split('\n\n')

dataset = [] #Вопрос-Ответ пары

alpabet = ' 1234567890-qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэёячсмитьбю'

def clean_str(r):
    r = r[2:].lower()
    r = [c for c in r  if c in alpabet]
    return ''.join(r)


for block in blocks:
    replicas = block.split('\n')[:2]
    if len(replicas)==2:
        pair = (clean_str(replicas[0]),clean_str(replicas[1]))
        if pair[0] and pair[1]:
            dataset.append(pair)

dataset = list(set(dataset))

def get_generative_replica(text):
    text = text.lower()
    for question, answer in dataset:
        if abs(len(text)- len(question)) / len(question) < 0.2:
            distance = nltk.edit_distance(text, question)
            diffetence = distance / len(question)
            if diffetence < 0.2:
                print(answer)
                return answer


def bot(text):

    intent = get_intent(text)

    if intent:

        return response_by_intent(intent)

    #generative model
    replica = get_generative_replica(text)
    if replica:
        return replica

    return get_failure_phrase()





from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '1313962816:AAF7vdy1Bnoh-X8E2xUN-mB1tWVFdzIF9Ro'
#Nick my BOT in Telegram -  WonderfulFuck_Films_Bot


# Initialize bot and dispatcher
bot1 = Bot(token=API_TOKEN)
dp = Dispatcher(bot1)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Good day!\nI am a smart bot. My specialty is films and series. I am well versed in this, but I can maintain a conversation on almost any topic. While I work only in Russian.\nI was developed by Yan Florin, a young and promising programmer, a specialist in machine learning and just a sexy man.\n____________\nHis contacts -  https://vk.com/exciting_opportunities\nRelease Date - 28.06.2020\n Technologies Used - sklean, Logistic   Regression, nltk")



@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    resp = bot(message.text)
    await message.answer(resp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


