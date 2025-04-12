from collections.abc import Mapping
from typing import Any, Optional, List
import requests
import json
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
import os


class YandexLLM(LLM):
    api_key: str = None
    iam_token: str = None
    folder_id: str
    max_tokens: int = 200
    temperature: float
    system_prompt: str = None
    
    @property
    def _llm_type(self) -> str:
        return "yagpt"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        # Проверка наличия учетных данных
        if not self.iam_token and not self.api_key:
            raise ValueError("Either iam_token or api_key must be provided")
        
        # Создание заголовков
        headers = {"Content-Type": "application/json"}
        
        # Приоритет отдается IAM токену, если он есть
        if self.iam_token:
            headers["Authorization"] = f"Bearer {self.iam_token}"
        elif self.api_key:
            headers["Authorization"] = f"Api-key {self.api_key}"
        
        # Отладочный вывод для проверки заголовков
        print(f"Headers: {headers}")
        print(f"folder_id: {self.folder_id}")
        
        # Создание сообщений
        messages = []
        if self.system_prompt:
            messages.append({
                "role": "system",
                "text": self.system_prompt
            })
        
        messages.append({
            "role": "user",
            "text": prompt
        })
        
        # Формирование запроса
        req = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": self.temperature,
                "maxTokens": str(self.max_tokens),
                "reasoningOptions": {
                    "mode": "DISABLED"
                }
            },
            "messages": messages
        }
        
        # Отладочный вывод тела запроса
        print(f"Request body: {json.dumps(req, ensure_ascii=False)}")
        
        try:
            response = requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers=headers,
                json=req
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            
            if response.status_code != 200:
                print(f"Error response body: {response.text}")
            
            response.raise_for_status()
            
            res = response.json()
            return res['result']['alternatives'][0]['message']['text']
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Status code: {response.status_code}")
            print(f"Response text: {response.text[:200]}...")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            raise
        except KeyError as e:
            print(f"Missing expected field in response: {e}")
            print(f"Response: {res}")
            raise