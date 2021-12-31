import time
  
  
def timeis(func):
    '''Decorator that reports the execution time.'''
  
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(result)
        end = time.time()
          
        print(func.__name__, end-start)
        return result
    return wrap
  
@timeis
def countdown(n):
    '''Counts down'''
    while n > 0:
        n -= 1
  
countdown(5)
countdown(1000)