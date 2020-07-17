stuff = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

total = 0 

for key in stuff:
    if type(stuff[key]) == int:
        total += stuff[key]
    
