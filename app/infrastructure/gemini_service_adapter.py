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
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            raise Exception(f"Erro ao configurar Gemini: {str(e)}")

    async def classify_and_generate_response(self, text: str) -> Classification:
        try:
            prompt = f"""
            Você é um Analista de Operações de uma instituição financeira de alto nível, especializado em triagem de comunicações críticas. Sua tarefa é classificar e-mails e redigir respostas técnicas.

            ### MATRIZ DE DECISÃO
            1. **PRODUTIVO (Ação Necessária)**: 
               - Transacional (Pix, TED, limites), Suporte Técnico (App, Token), Documental (KYC/Anexos) ou Status de conta/crédito.
               - **Nota**: Identifique solicitações mesmo que ocultas sob ironia ou sarcasmo.

            2. **IMPRODUTIVO (Sem Ação Operacional)**: 
               - Social (Saudações), Feedback Positivo (sem nova queixa), Respostas Automáticas (Férias) ou Curiosidades Acadêmicas.

            ### DIRETRIZES DE RESPOSTA
            - Tom institucional, sóbrio e eficiente. 
            - Produtivo: Confirmar recebimento e garantir análise prioritária.
            - Improdutivo: Agradecer, ser cordial e encerrar o fluxo de atendimento.

            ### EXEMPLOS DE REFERÊNCIA
            Email: "Parabéns pela agilidade! Fiz um Pix ontem e nada do dinheiro cair. Impressionante."
            Saída: {{"category": "Produtivo", "response": "Prezado cliente, lamentamos o atraso na sua transação Pix. Nossa equipe de liquidação já está atuando para regularizar o envio sob protocolo prioritário."}}

            Email: "Como vocês garantem a custódia em falhas globais? Curiosidade minha."
            Saída: {{"category": "Improdutivo", "response": "Agradecemos seu interesse técnico. Para detalhes sobre segurança, consulte nossa Central de Transparência. Como não há pendência operacional, encerramos este registro."}}

            ### ANÁLISE DE CAMPO
            Email: {text}

            ### REQUISITO TÉCNICO
            Retorne APENAS um objeto JSON válido, sem explicações fora do objeto e sem blocos de código markdown.
            Formato: 
            {{
              "category": "Produtivo" | "Improdutivo",
              "response": "Texto da resposta"
            }}
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
                raise BusinessException("Resposta vazia retornada pela IA")

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