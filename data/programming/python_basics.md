# יסודות Python

## משתנים וטיפוסים
ב-Python לא מצהירים על טיפוס המשתנה. הטיפוס נקבע לפי הערך שמוכנס אליו.

```python
age = 20          # int - מספר שלם
price = 9.90      # float - מספר עשרוני
name = "Sara"     # str - מחרוזת
is_student = True # bool - ערך בוליאני
```

הפונקציה `type()` מחזירה את הטיפוס של משתנה: `type(age)` מחזירה `<class 'int'>`.

## רשימה (list)
רשימה היא אוסף מסודר של איברים, וניתן לשנות אותה (mutable). כותבים אותה בסוגריים מרובעים.

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")   # הוספת איבר לסוף
fruits[0] = "orange"     # שינוי איבר
print(len(fruits))       # 4
```

## טאפל (tuple)
טאפל דומה לרשימה, אבל אי אפשר לשנות אותו אחרי שנוצר (immutable). כותבים אותו בסוגריים עגולים.

```python
point = (3, 5)
point[0] = 7   # שגיאה! TypeError
```

**ההבדל בין list ל-tuple:** רשימה ניתנת לשינוי וטאפל לא. משתמשים בטאפל לנתונים קבועים, כמו קואורדינטות או ימי השבוע. טאפל מהיר מעט יותר וחוסך זיכרון, וניתן להשתמש בו כמפתח במילון.

## מילון (dict)
מילון שומר זוגות של מפתח וערך. הגישה לערך היא לפי המפתח, ולא לפי מיקום.

```python
student = {"name": "Sara", "age": 20}
print(student["name"])        # Sara
student["city"] = "Jerusalem" # הוספת זוג חדש
print(student.get("grade", 0)) # 0 - ערך ברירת מחדל אם המפתח לא קיים
```

## קבוצה (set)
קבוצה היא אוסף ללא סדר וללא כפילויות.

```python
nums = {1, 2, 2, 3}
print(nums)   # {1, 2, 3}
```

## תנאים
```python
if age >= 18:
    print("בוגר")
elif age >= 13:
    print("נער")
else:
    print("ילד")
```
ב-Python ההזחה (indentation) היא חלק מהתחביר. בלוק קוד מוגדר לפי ההזחה ולא לפי סוגריים מסולסלים.

## לולאות
לולאת `for` עוברת על כל איבר באוסף:

```python
for fruit in fruits:
    print(fruit)

for i in range(5):   # 0, 1, 2, 3, 4
    print(i)
```

לולאת `while` רצה כל עוד התנאי מתקיים:

```python
count = 0
while count < 3:
    count += 1
```

`break` יוצא מהלולאה, ו-`continue` מדלג לאיטרציה הבאה.

## List Comprehension
דרך מקוצרת ליצור רשימה חדשה מרשימה קיימת:

```python
squares = [x * x for x in range(5)]          # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0] # [0, 2, 4, 6, 8]
```

## פונקציות
מגדירים פונקציה עם המילה `def`. אפשר לתת לפרמטר ערך ברירת מחדל.

```python
def greet(name, greeting="שלום"):
    return f"{greeting}, {name}!"

print(greet("Sara"))           # שלום, Sara!
print(greet("Sara", "בוקר טוב"))
```

`*args` מקבל מספר לא ידוע של ארגומנטים כטאפל, ו-`**kwargs` מקבל ארגומנטים בעלי שם כמילון.

## טיפול בשגיאות
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("אי אפשר לחלק באפס")
finally:
    print("הבלוק הזה רץ תמיד")
```

## מחלקות בקצרה
```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says woof"
```
המתודה `__init__` היא הבנאי (constructor), והיא רצה כשיוצרים אובייקט חדש. `self` מצביע על האובייקט הנוכחי.
