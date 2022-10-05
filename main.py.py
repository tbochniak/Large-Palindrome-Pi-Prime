# digitviewer-convert from https://github.com/carvalhopatrick/DigitViewer.git edited to receive parameters as argv

import urllib.request
import subprocess
import time

last_digits = '0123456789'*10
idx_g = -50 #offset
maior_p = 21

def isprime(num):
  if num == 2 or num == 3:
      return True
  if num < 2 or num%2 == 0:
      return False
  if num < 9:
      return True
  if num%3 == 0:
      return False
  a = int(num**0.5)
  b = 5
  while b <= a:
    if num%b == 0:
        return False
    if num%(b+2) == 0:
        return False
    b=b+6
  return True

def download(file_num):
    url = f'https://storage.googleapis.com/pi100t/Pi%20-%20Dec%20-%20Chudnovsky/Pi%20-%20Dec%20-%20Chudnovsky%20-%20{file_num}.ycd'
    urllib.request.urlretrieve(url,f"file{file_num}.ycd")

def unzip(file_num):
    inicio = (file_num)*100*10**9+1
    fim = inicio + 100*10**9-1
    Command = ['digitviewer-convert', f'file{file_num}.ycd', str(inicio), str(fim), f"file{file_num}.txt"]
    subprocess.run(Command)

def delete(file_num):
    command1 = ['rm', f"file{file_num}.txt"]
    command2 = ['rm', f"file{file_num}.ycd"]
    subprocess.run(command1)
    subprocess.run(command2)

def process_file(file_num):
    global last_digits
    global idx_g
    global maior_p
    with open(f'file{file_num}.txt', 'r') as f:
        for i in range(100):
            #Process the last 50 digits of the previous file
            pi = last_digits+f.read(50)
            f.seek(i*10**9)
            for j in range(50, 100):
                for k in range(1, 50):
                    if not(pi[j-k] == pi[j+k]):
                        k -= 1
                        if((2*k+1) >= maior_p) and isprime(int(pi[j-k:j+k+1])):
                            print(f"Arquivo: {file_num}//Palindromo de {2*k+1} dígitos// {pi[j-k:j+k+1]}// idx: {idx_g}\n")
                            with open(f'output.txt', 'a+') as o:
                                o.write(f"Arquivo: {file_num}//Palindromo de {2*k+1} dígitos// {pi[j-k:j+k+1]}// idx: {idx_g}\n")
                        break
                idx_g += 1

            #Process the first 50 digits of the file
            pi = last_digits[len(last_digits)-50:len(last_digits)] + f.read(100)
            f.seek(i*10**9)
            for j in range(50, 100):
                for k in range(1, 50):
                    if not(pi[j-k] == pi[j+k]):
                        k -= 1
                        if(2*k+1) >= maior_p:
                            print(f"Arquivo: {file_num}//Palindromo de {2*k+1} dígitos// {pi[j-k:j+k+1]}// idx: {idx_g}\n")
                            with open(f'output.txt', 'a+') as o:
                                o.write(f"Arquivo: {file_num}//Palindromo de {2*k+1} dígitos// {pi[j-k:j+k+1]}// idx: {idx_g}\n")
                        break
                idx_g += 1

            #Process digits from 50 to 10**9-50
            pi = f.read(10**9)
            for j in range(50, 10**9-50):
                for k in range(1, 50):
                    if not(pi[j-k] == pi[j+k]):
                        k -= 1
                        if(2*k+1) >= maior_p:
                            print((f"Arquivo: {file_num}//Palindromo de {2*k+1} dígitos// {pi[j-k:j+k+1]}// idx: {idx_g}\n"))
                            with open(f'output.txt', 'a+') as o:
                                o.write(f"Arquivo: {file_num}//Palindromo de {2*k+1} dígitos// {pi[j-k:j+k+1]}// idx: {idx_g}\n")
                        break
                idx_g += 1

            #update global variable
            last_digits = pi[10**9-100:10**9]

def main():
    t_start = time.time()
    for file_num in range(1000):
        print(f"Iniciando o download do file{file_num}.ycd")
        download(file_num)
        print(f"Fim do download do file{file_num}.ycd")
        unzip(file_num)
        print(f"Arquivo descomapctado file{file_num}.txt")
        print(f"Iniciando o processamento file{file_num}.txt")
        process_file(file_num)
        print(f"Finalizando o processamento file{file_num}.txt")
        print("Indíce:", idx_g)
        delete(file_num)
        print(f"Arquivo apagado file{file_num}.ycd/txt")
        print(f"Tempo total de excecução file{file_num}:", time.time()-t_start, "\n\n\n")
main()