#1Q.Build a mini interpreter that reads a string like "5 + 2 * (3 - 1)" and evaluates it using loops, if–else, and functions.
Program:
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def precedence(op):
 
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0

def apply_operator(a, b, op):
   
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b

def evaluate(expression):
        nums = [] 
    ops = []   
    i = 0

    while i < len(expression):
        char = expression[i]

        
        if char == ' ':
            i += 1
            continue

       
        if char.isdigit():
            num = 0
            while i < len(expression) and expression[i].isdigit():
                num = num * 10 + int(expression[i])
                i += 1
            nums.append(num)
            i -= 1  
        elif char == '(':
            ops.append(char)
        elif char == ')':
            # Solve entire bracket
            while ops and ops[-1] != '(':
                b = nums.pop()
                a = nums.pop()
                op = ops.pop()
                nums.append(apply_operator(a, b, op))
            ops.pop()  
        else:
            # Operator encountered
            while ops and precedence(ops[-1]) >= precedence(char):
                b = nums.pop()
                a = nums.pop()
                op = ops.pop()
                nums.append(apply_operator(a, b, op))
            ops.append(char)

        i += 1

  
        b = nums.pop()
        a = nums.pop()
        op = ops.pop()
        nums.append(apply_operator(a, b, op))

    return nums[-1]



result = evaluate(expression)
print("Input Expression:", expression)
print("Output Result:", result)


#2Q.Define a function word_count(sentence) that returns the top N frequent words (case-insensitive, ignore punctuation).
Program:
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import string

def word_count(sentence, N):
    sentence = sentence.lower()
    translator = str.maketrans('', '', string.punctuation)
    sentence = sentence.translate(translator)
    words = sentence.split()
    
   freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    

    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    return sorted_words[:N]

sentence = "Hello hello world! This is a test. Hello, world test test."
top_n = 3
result = word_count(sentence, top_n)
print(f"Top {top_n} frequent words:", result)



