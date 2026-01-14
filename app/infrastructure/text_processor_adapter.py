from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

from app.core.infrastructure.text_processor_port import TextProcessorPort
import nltk

from app.domain.exception.business_exception import BusinessException


class TextProcessorAdapter(TextProcessorPort):

    def __init__(self):
        try:
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)

            self.stop_words = set(stopwords.words('portuguese'))
            self.lemmatizer = WordNetLemmatizer()

        except Exception as e:
            raise Exception(f"Erro ao iniciar processador de texto: {str(e)}")

    async def process(self, text: str) -> str:
        try:

            text = text.lower()

            text = re.sub(r'\s+', ' ', text).strip()

            tokens = word_tokenize(text, language='portuguese')

            tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]

            tokens = [self.lemmatizer.lemmatize(word) for word in tokens]

            processed_text = ' '.join(tokens)

            return processed_text

        except Exception as e:
            raise Exception(f"Erro ao processar texto: str{e}")