def logger(func):
    def inner(*args, **kwargs):
        # takes any arbitrary number and type of parameters 
        print "Arguments were: %s, %s" % (args, kwargs)
        return func(*args, **kwargs)
    return inner 

@logger
def foo1(x, y=1):
    return x * y

@logger
def foo2():
    return 2
    

