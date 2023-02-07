
hod = []

hod2 = dict(zip(hod))

def vvod():
    a1 = int(input('введите номер строки'))
    
    b1 = int(input('введите номер столбца'))
    if 0 > a1 or a1 > 2 or 0 > b1 or b1 > 2:
        print()
        print('Введите число от 0 до 2')
        print()
        return vvod()
    
    else:
        if a1 == 0 and b1 == 0:
            hod.append(1)
        elif a1 == 1 and b1 == 0:
            hod.append(2)
        elif a1 == 2 and b1 == 0:
            hod.append(3)
        elif a1 == 0 and b1 == 1:
            hod.append(4)
        elif a1 == 1 and b1 == 1:
            hod.append(5)
        elif a1 == 2 and b1 == 1:
            hod.append(6)
        elif a1 == 0 and b1 == 2:
            hod.append(7)
        elif a1 == 1 and b1 == 2:
            hod.append(8)
        elif a1 == 2 and b1 == 2:
            hod.append(9)
        for i in hod:
            if hod.count(i) > 1:
                hod.remove(i)
                print('сделайте другой ход, клетка занята')
                return vvod()
                
    return a1, b1   
        
def print1():
    print('    | 0 | 1 | 2 |')
    print(' ----------------')
    for i, row in enumerate(S):
        row_str = f"  {i} | {' | '.join(row)} | "
            
        print(row_str)
    print()
        
def pobeda():
    list_win = (((0,0),(1,1),(2,2)),((0,0),(0,1),(0,2)),((0,0),(1,0),(2,0)),((1,0),(1,1),(1,2)),((2,0),(2,1),(2,2)),((0,1),(1,1),(2,1)),((0,2),(1,2),(2,2)),((2,0),(1,1),(0,2)))
    for cord in list_win:
        symbols = []
        for c in cord:
            symbols.append(S[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False               
    
           
S = [[" "] * 3 for i in range(3) ]
N = 0
while True:
    N += 1
    print1() 
    if N % 2 == 1:
        print(" Ходит крестик!")
    else:
        print(" Ходит нолик!")
    a1, b1 = vvod()
    if N % 2 == 1:
        S[a1][b1] = "X"
    else:
        S[a1][b1] = "0"
     
    if pobeda():
        break
     
    if N == 9:
        print(" Ничья!")
        break
        
 