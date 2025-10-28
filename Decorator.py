def smart_div(func):
    def inner(*args, **kwargs):
        a, b = args  
        if a < b:
            a, b = b, a   
        return func(a, b)  
    return inner


@smart_div
def div(a, b):
    print(a / b)


div(2, 4)

''' When we call the div() function, Python actually goes to the smart_div decorator first, because div is decorated with @smart_div.

The @smart_div decorator replaces the original div with the inner function that it returns.

So, when we call div(2, 4), it really calls the inner function.Inside inner:

The values a = 2 and b = 4 are taken from args.

It checks if a < b. Since 2 < 4, it swaps them. Now a = 4 and b = 2.

Then it calls func(a, b), which means it runs the original div function.

The original div prints 4 / 2 = 2.0.'''
