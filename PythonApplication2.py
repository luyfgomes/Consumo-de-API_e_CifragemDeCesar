# -*- coding: utf-8 -*-
import requests
import json
import hashlib 

requisicao = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=85c1bcea2d7cb80e0ecafa54c210d24378133b41')
resultRequisicao = json.loads(requisicao.content) #cria um dicionário contendo o conteúdo JSON convertido para objetos Python


arqJson = open('answer.json', 'w') #criando arquivo .json na pasta
#arqJson.write(str(resultRequisicao)) #passando pra string para escrever no json

alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
msgFinal = []


print('_________________________________##DESAFIO CODENATION:##__________________________________\n')
print('Criptografia de Júlio César')
print('__________________________________________________________________________________________\n\n')


entrada = resultRequisicao["cifrado"]
entrada = entrada.lower() #transformando entrada em caixa baixa
modif = int(resultRequisicao["numero_casas"]) #modificador de numero de casas


for i in entrada:
    if i in alfabeto:
        cont = alfabeto.index(i) #se i estiver no alfabeto, cont recebe a posição da letra no alfabeto
        posicaoEntrada = cont - modif #trocará a letra equivalente pela letra na posição + o modificador

        if posicaoEntrada >= len(alfabeto): #se a posição ultrapassar o numero de letras do alfabeto, ele começará de novo
            posicaoEntrada = posicaoEntrada - len(alfabeto)
        if posicaoEntrada < 0: #se a posição for menor que 0, ele começará da ultima letra, z.
            posicaoEntrada = posicaoEntrada + len(alfabeto)

        msgFinal.append(alfabeto[posicaoEntrada]) #adiciona à mensagem final a letra na posição

    else: #caracteres diferentes de letras não passarão pelo processo, serão adicionados diretamente.
        msgFinal.append(i)

msgFinal = ''.join(msgFinal) #parametro .join junta os itens na lista pelo defido entre os apostrofes; ex: se passássemos a lista [A,P,S] pelo '&'.join, imprimiria: A&P&S
resumoCriptografico = hashlib.sha1(msgFinal.encode("utf-8")).hexdigest() #necessario .encode() para hashlib
 #resumo = hashlib.sha1(decifrado.encode("utf-8")).hexdigest()

print('\n_____________________________________________##RESULTADO:##_____________________________________________\n',)

print('Mensagem cifrada: ', entrada)
print("Mensagem Decifrada: ", msgFinal ) 
print("Mensagem Sha1: ", resumoCriptografico)


print('__________________________________________________________________________________________________________\n')

resultRequisicao['decifrado'] = msgFinal
resultRequisicao['resumo_criptografico'] = resumoCriptografico
arqJson.write(str(resultRequisicao)) #escrever no json
#arqJson.close()

with open("answer.json", 'w') as answer:
    json.dump(resultRequisicao, answer)
    answer.close()

url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=85c1bcea2d7cb80e0ecafa54c210d24378133b41"
files = [('answer', open('answer.json' ,'rb'))]
response = requests.post(url , files = files)

print(response.text.encode('utf-8'))



