from recomenda_filmes import indica_filmes


def main():
   resposta = input_usuario()
   result = indica_filmes(resposta)
   print(result)



def input_usuario():
   return input("Qual tema gostaria de procurar?") 



if __name__ == '__main__':
   main()