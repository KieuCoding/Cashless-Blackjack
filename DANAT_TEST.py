"""
1.) extract file
2.) extract every 7 string elements, store them into a list
3.) Check the characters in each sublist, if they're pipes, *, or Letters
4.) Turn the string numbers following the characters into int corrdi
5.) start comparing them to the '*' coordinate
6.) compare the pipes, see if they connect
7.) Check which letters connect to the '*' via the pipe characters  
"""
def decode(file_path):
    UniqueChar = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'
                  , 'L', 'N', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                  'V', 'W', 'X', 'Y', 'Z', '*', '═', '║', '╔', '╗',
                    '╚', '╝', '╠', '╣', '╦', '╩')
    
    batch = []
    data = []
    Map = []
    MergerOne = ''
    MergerTwo = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        Txt = file.read()
        for line in Txt:
            if line == '\n':
                continue
            elif line in UniqueChar and data:
                batch.append(data)
                data = []
            data.append(line)
        if data:
            batch.append(data)
        # if position 4 in a size 6 list is empty combine positions 5 & 6
        # if pos 4 is occupied combine positions 3 and 4
        # 7 size list, combine pos 3 & 4 then pos 6 & 7
        for i in range(0, len(batch)):
            if len(batch[i]) == 7:
                MergerOne = batch[i][2] + batch[i][3]
                MergerTwo = batch[i][5] + batch[i][6]
                batch[i] = [batch[i][0], MergerOne, MergerTwo]
                Map.append(batch[i])
            elif len(batch[i]) == 6:
                if batch[i][3] == ' ':
                    MergerOne = batch[i][2]
                    MergerTwo = batch[i][4] + batch[i][5]
                    batch[i] = [batch[i][0], MergerOne, MergerTwo]
                    Map.append(batch[i])
                elif batch[i][3] != ' ':
                    MergerOne = batch[i][2] + batch[i][3]
                    MergerTwo = batch[i][5]
                    batch[i] = [batch[i][0], MergerOne, MergerTwo]
                    Map.append(batch[i])
            
    return Map

def main():
    file_path = "data_qual.txt"
    test = []
    print(decode(file_path)[0:30])


if __name__ == "__main__":
    main() 
