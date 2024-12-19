A = 59397658
B = 0
C = 0

result = []

#while A != 0:
#    print(A)
#    B = (A % 8) ^ 1
#    C = A >> B
#    B = B ^ C ^ 4
#    A = A >> 3
#    result.append(B % 8)


#while A != 0:
#    B = (A % 8) ^ 1
#    B = B ^ (A >> B) ^ 4
#    A = A >> 3
#    result.append(B % 8)


def one_iter(A):
    return (((A % 8) ^ 1) ^ (A >> ((A % 8) ^ 1)) ^ 4) % 8

result = [2,4,1,1,7,5,4,6,1,4,0,3,5,5,3,0]
output = []
A_parts = []
A = 0
for num in result[::-1]:
    A = A << 3
    for i in range(9):
        if one_iter(A + i) == num:
            A += i
            break


print(A)

while A != 0:
    output.append(one_iter(A))
    A = A >> 3

print(','.join(str(num) for num in output))
print(','.join(str(num) for num in result))

