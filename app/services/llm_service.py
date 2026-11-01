import asyncio
# from openai import AsyncOpenAI
# client = AsyncOpenAI(api_key="API_KEY")

class LLMService:
    @staticmethod
    async def generate_response_stream(prompt: str, context: str = ""):
        """
        LLM'den streaming (token bazlı) yanıt üretir.
        """
        
        # --- GERÇEK LLM ENTEGRASYONU (Örnek OpenAI) ---
        # response = await client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": f"Sen bir Game Master'sın. Hafıza: {context}"},
        #         {"role": "user", "content": prompt}
        #     ],
        #     stream=True
        # )
        # async for chunk in response:
        #     content = chunk.choices[0].delta.content
        #     if content is not None:
        #         yield content
        
        # --- TEST/MOCK SİMÜLASYONU ---
        mock_text = f"Odanın loş ışığında ilerlerken şu aksiyonu aldın: '{prompt}'. Zarını atıyorum..."
        words = mock_text.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05) # Kelime başı gecikme simülasyonu