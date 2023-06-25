import System_data as s
import random as r

inp = 3
output = ''
ran = 0
lev = 0

for i in range(0, inp): #inp값만큼 반복
    ran = r.randint(0,s.enchant_sum-1) #무기 인첸트값을 랜덤으로 뽑음
    lev = r.randint(1,5) #인첸트 당 레벨값을 1 ~ 5 사이로 랜덤으로 뽑음
    output += s.enchant_name[ran] + ' ' + str(lev) + '\n' #output에 출력값을 정함

print(output) #결과 출력