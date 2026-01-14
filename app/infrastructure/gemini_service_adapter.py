import re
import json
import google.generativeai as genai
from google.api_core import exceptions
from app.core.infrastructure.gemini_service_port import GeminiServicePort
from app.domain.classification import Classification
from app.domain.enums.category import Category
from app.domain.exception.business_exception import BusinessException


class GeminiServiceAdapter(GeminiServicePort):
    def __init__(self, api_key: str):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        except Exception as e:
            raise Exception(f"Erro ao configurar Gemini: {str(e)}")

    async def classify_and_generate_response(self, text: str) -> Classification:
        try:
            prompt = f"""
            Você é um assistente de classificação de emails para uma empresa financeira.

            Analise o seguinte email e:
            1. Classifique como "Produtivo" ou "Improdutivo"
               - Produtivo: emails que requerem ação (suporte técnico, atualizações, dúvidas sobre sistema)
               - Improdutivo: emails que não requerem ação imediata (felicitações, agradecimentos)

            2. Gere uma resposta automática apropriada e profissional

            Email: {text}

            Retorne APENAS um JSON válido no formato:
            {{"category": "Produtivo", "response": "Sua resposta aqui"}}

            Não inclua nenhum texto adicional, apenas o JSON.
             """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            json_match = re.search(r'\{.*\}', response_text, re.DOTALL) # Se vier markdown

            if json_match:
                response_text = json_match.group()

            result = json.loads(response_text)

            category_str = result.get('category', '').strip()
            if category_str not in ['Produtivo', 'Improdutivo']:
                raise Exception(f"Categoria inválida retornada: {category_str}")

            category = Category.PRODUCTIVE if category_str == 'Produtivo' else Category.UNPRODUCTIVE

            response = result.get('response', '').strip()

            if not response:
                raise Exception("Resposta vazia retornada pela IA")

            return Classification(
                category=category,
                suggested_response=response
            )

        except exceptions.ResourceExhausted:
            raise BusinessException("Limite atingido, tente novamente mais tarde.")

        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao parsear resposta JSON: {str(e)}")

        except Exception as e:
            raise Exception(f"Erro ao chamar IA: {str(e)}")