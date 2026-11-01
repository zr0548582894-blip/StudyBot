# השוואת אסטרטגיות Chunking

| אסטרטגיה | מקטעים | מילים למקטע | Hit@1 | Hit@4 | MRR | מילים שנשלחות ל-LLM | זמן בנייה (שניות) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A - מקטעים גדולים (512/50) | 140 | 85 | 12/15 (80%) | 14/15 (93%) | 0.85 | 425 | 94 |
| B - מקטעים קטנים (128/20) | 275 | 46 | 12/15 (80%) | 14/15 (93%) | 0.87 | 223 | 116 |

**A - מקטעים גדולים (512/50) - שאלות שהמקור הנכון לא נמצא בהן:** מה זה קצב הלמידה אלפא ואיך בוחרים אותו? (נשלף: Lecture1_EvolutionOfAI.pptx:45, Lecture1_EvolutionOfAI.pptx:25, Lecture1_EvolutionOfAI.pptx:21, Lecture1_EvolutionOfAI.pptx:24)

**B - מקטעים קטנים (128/20) - שאלות שהמקור הנכון לא נמצא בהן:** מה זה קצב הלמידה אלפא ואיך בוחרים אותו? (נשלף: Lecture1_EvolutionOfAI.pptx:21, Lecture1_EvolutionOfAI.pptx:24, Lecture1_EvolutionOfAI.pptx:32, Lecture1_EvolutionOfAI.pptx:25)
