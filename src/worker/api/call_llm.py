import time

import httpx

openai_api_base = ""
# openai_api_path=""
openai_ai_path = ""
apikey = ""
model = ""
timeout = 30


async def call_llm_api(client_request: str) -> str:
    """
    Effectue une requête POST asynchrone à l'API Mistral pour améliorer un courrier client.

    Args:
        client_request: Le message client à améliorer

    Returns:
        Le courrier amélioré ou un message d'erreur

    Raises:
        httpx.HTTPError: En cas d'erreur réseau
    """

    # Construction du payload
    json_data = {
        'messages': [
            {
                'role': 'user',
                'content': (
                    'instruction:\n'
                    '"""\n'
                    'Update email anwser\n'
                    '"""\n\n'
                    'client message:\n'
                    f'"""\n{client_request}\n"""'
                )
            }
        ],
        'model': model
    }

    headers = {
        'Authorization': f'Bearer {apikey}',
        'Content-Type': 'application/json'
    }

    try:
        async with httpx.AsyncClient(
                base_url=openai_api_base,
                timeout=timeout
        ) as client:
            start_time = time.time()

            # Requête POST simplifiée
            response = await client.post(
                openai_ai_path,
                headers=headers,
                json=json_data
            )

            elapsed_time = time.time() - start_time
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            # Gestion des erreurs HTTP
            if response.status_code != 200:
                error_msg = response.text
                print(
                    f"[{timestamp}] Erreur après {elapsed_time:.2f}s - "
                    f"Status {response.status_code}: {error_msg}"
                )
                return f"Erreur {response.status_code}: {error_msg}"

            # Parsing de la réponse
            data = response.json()  # Plus pythonique que json.loads(response.content)
            formatted_request = data['choices'][0]['message']['content']

            print(f"[{timestamp}] Succès après {elapsed_time:.2f}s")
            return formatted_request

    except httpx.TimeoutException as e:
        print(f"Timeout après {timeout}s: {e}")
        return f"Erreur: Timeout de la requête ({timeout}s)"

    except httpx.HTTPError as e:
        print(f"Erreur HTTP: {e}")
        return f"Erreur réseau: {str(e)}"

    except (KeyError, IndexError) as e:
        print(f"Erreur de parsing de la réponse: {e}")
        return "Erreur: Format de réponse inattendu"

    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return f"Erreur inattendue: {str(e)}"
