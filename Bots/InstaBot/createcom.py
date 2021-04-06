size = 3


raw = open('instas.txt', encoding='latin-1')
arq = open('comment.txt', 'w')
x = raw.readlines()
a = 0
comment = ' '
comments = []
while a < len(x):
    if a%size == 0:
        print(comment)
        comment += '\n'
        comments.append(comment)
        comment = ""
        print(a//3)
    temp = x[a]
    temp = temp[:len(temp)-2]
    comment += temp + ' '
    
    a += 1
arq.writelines(comments)
#texto = raw.read()
#print(texto)
arq.close()
raw.close() 