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
            Você é um Analista de Operações de uma instituição financeira de alto nível, especializado em triagem de comunicações.
            Sua tarefa é analisar o conteúdo de e-mails recebidos, classificar sua natureza operacional e redigir uma resposta técnica e cordial.

            ### DIRETRIZES DE CLASSIFICAÇÃO:
            1. **Produtivo**: Solicitações de suporte, dúvidas sobre transações, problemas de acesso, envio de documentos ou pedidos de atualização de status.
            2. **Improdutivo**: Agradecimentos, saudações sazonais (Natal, aniversário), mensagens automáticas de "fora do escritório" ou feedbacks positivos sem demanda de ação.

            ### DIRETRIZES DE RESPOSTA:
            - Utilize um tom profissional, empático e corporativo.
            - Para e-mails "Produtivos", informe que a solicitação foi recebida e está em análise.
            - Para e-mails "Improdutivos", responda com cordialidade e encerre o ticket.

            ### EXEMPLOS DE REFERÊNCIA:
            Email: "Minha transferência via Pix não caiu até agora, podem verificar?"
            Saída: {{"category": "Produtivo", "response": "Prezado cliente, recebemos sua dúvida sobre a transação Pix. Já encaminhamos para nossa equipe técnica verificar o status e retornaremos em breve."}}

            Email: "Parabéns pelo excelente atendimento de ontem!"
            Saída: {{"category": "Improdutivo", "response": "Agradecemos imensamente o seu feedback. Ficamos felizes em saber que o atendimento atendeu às suas expectativas. Conte conosco!"}}

            ### TEXTO PARA ANÁLISE:
            Email: {text}

            ### REQUISITO TÉCNICO:
            Retorne estritamente um objeto JSON válido. Não inclua introduções, explicações ou blocos de código markdown.
            Formato: {{"category": "Produtivo" | "Improdutivo", "response": "string"}}
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