# Exemplo simplificado da lógica que você vai encontrar
while True:
    comando = ouvir_microfone()  # Passo 1 e 2
    
    if "previsão do tempo" in comando:
        resposta = consultar_clima() # Passo 3 e 4
    else:
        resposta = ia_gemini(comando) # O "Cérebro"
        
    falar(resposta) # Passo 5
