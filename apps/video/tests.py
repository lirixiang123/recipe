from django.test import TestCase

# Create your tests here.
a=1
list = [1,2]
for i in range(8):
    if i == 2:
        a=5
    list.append(a)

print(list)
