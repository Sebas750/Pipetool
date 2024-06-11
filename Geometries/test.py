from numpy import cos
from random import randint


n = 70

with open(f'test_random.csv', 'w') as f:
    f.write('# x  r\n')
    for i in range(n):
        f.write(f'{i/10}  {randint(1, 100)/100}\n')

