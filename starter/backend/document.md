# Documentating Endpoints

## GET '/categories'

* Description: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category  
* Test: Enter a command at the terminal

`~ curl http://127.0.0.1:5000/categories`

* Returns: Categories, that contains an object of id

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

## GET '/questions?page=integer'

* Description: Fetches a paginated set of questions, a total number of questions, all categories and current category string.  
* Test: Enter a command at the terminal

`~ curl http://127.0.0.1:5000/questions\?page\=1`

* Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    ...
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "total_questions": 19
}
```

## GET '/categories/[id]/questions'

* Description: Fetches questions for a cateogry specified by id request argument  
* Test: Enter a command at the terminal

`~ curl http://127.0.0.1:5000/categories/5/questions`

* Returns: An object with questions for current cateogry, questions in current cateogry and total questions

```
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "total_questions": 3
}
```

## DELETE '/questions/[id]'

* Description: Deletes a specified question using the id of the question  
* Test: Enter a command at the terminal

`~ curl -X DELETE http://localhost:5000/questions/26`

* Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

```
{
  "id": 26
}
```

## POST '/questions'

* Description: Sends a post request in order to add a new question  
* Test: Enter a command at the terminal

`~ curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "new q", "answer": "new a", "difficulty": 1, "category": 1}'`

* Returns: {}
* Results: A new question added.(total questions: 19 to 20)

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "new a",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "new q"
    },
    ...
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "total_questions": 20
}
```

## POST '/questions/search'

* Description: Sends a post request in order to search for a specific question by search term  
* Test: Enter a command at the terminal

`~ curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "branch"}'`

* Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 1
}
```

## POST '/quizzes'

* Description: Sends a post request in order to get the random next question  
* Test: Enter a command at the terminal

`~ curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":1}}'`

* Returns: a single new question object at random

```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  }
}
```
