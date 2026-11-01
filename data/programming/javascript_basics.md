# JavaScript Basics

## Declaring Variables: var, let and const
JavaScript has three ways to declare a variable:

- `var` – the old way. Function-scoped and hoisted. Avoid it in modern code.
- `let` – block-scoped. The value can be reassigned.
- `const` – block-scoped. The variable cannot be reassigned.

```javascript
let count = 0;
count = 1;          // OK

const PI = 3.14;
PI = 3;             // TypeError: Assignment to constant variable
```

Note: `const` prevents reassignment, not mutation. A `const` array can still get new items with `push()`.

## Data Types
Primitive types: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`.
Everything else (arrays, functions, objects) is an `object`.

`null` means "intentionally empty". `undefined` means "a value was never assigned".

## Equality: == vs ===
`==` compares values after type conversion. `===` compares value and type, with no conversion.

```javascript
5 == "5"    // true
5 === "5"   // false
```
Best practice: always use `===`.

## Functions
Regular function declaration:

```javascript
function add(a, b) {
  return a + b;
}
```

Arrow function – a shorter syntax:

```javascript
const add = (a, b) => a + b;
const square = x => x * x;
```

Arrow functions do not have their own `this`. They take `this` from the surrounding scope, which makes them useful inside callbacks.

## Arrays
```javascript
const nums = [1, 2, 3, 4];
nums.push(5);                       // add to end
const doubled = nums.map(n => n * 2);      // [2, 4, 6, 8, 10]
const evens = nums.filter(n => n % 2 === 0); // [2, 4]
const sum = nums.reduce((acc, n) => acc + n, 0); // 15
```

## Objects
```javascript
const user = { name: "Sara", age: 20 };
console.log(user.name);        // dot notation
console.log(user["age"]);      // bracket notation

const { name, age } = user;    // destructuring
const copy = { ...user, city: "Jerusalem" }; // spread operator
```

## Template Literals
Strings in backticks can contain expressions:

```javascript
const greeting = `Hello, ${name}! You are ${age} years old.`;
```

## Asynchronous Code
JavaScript runs on a single thread. Long operations (network requests, timers) run asynchronously so the page does not freeze.

### Promises
A Promise represents a value that will be available in the future. It has three states: pending, fulfilled, rejected.

```javascript
fetch("https://api.example.com/data")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### async / await
`async/await` is a cleaner way to write code that uses Promises. An `async` function always returns a Promise. `await` pauses the function until the Promise resolves.

```javascript
async function loadData() {
  try {
    const response = await fetch("https://api.example.com/data");
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("Request failed:", error);
  }
}
```

## The Event Loop
The event loop lets JavaScript handle asynchronous work. Synchronous code runs first on the call stack. Completed async callbacks wait in a queue, and the event loop moves them to the stack when it is empty.

## DOM Manipulation
```javascript
const button = document.getElementById("myButton");
button.addEventListener("click", () => {
  document.querySelector("h1").textContent = "Clicked!";
});
```
