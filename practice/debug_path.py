import os
import sys

print("Current Working Directory:")
print(os.getcwd())

print("\nPython Path:")
for p in sys.path:
    print(p)