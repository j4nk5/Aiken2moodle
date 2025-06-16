# 📝 Aiken2moodle (Aiken to Moodle Xml) – Moodle Quiz XML Generator from AIKEN Files

## 📌 Description

This Python script scans its own folder **and all subfolders** for `.txt` quiz files in AIKEN format and converts them into `.xml` files compatible with Moodle for importing into Moodle quizzes.

---

## 📂 Recognized Input File Names

The script automatically processes any `.txt` file located in its folder or subfolders, provided the filename is:

- `quiz.txt`
- `quiz1.txt`, `quiz2.txt`, ...
- `kouiz.txt`
- `kouiz1.txt`, `kouiz2.txt`, ...

---

## ✍️ AIKEN Format Example

What is the capital of France?  
A. Berlin  
B. Madrid  
C. Paris  
D. Rome  
ANSWER: C  
FEEDBACK: Paris is the capital of France.

- Each question must follow this format.
- Only **one correct answer** per question.
- Feedback is optional and must appear **immediately after** the `ANSWER:` line, starting with `FEEDBACK:`.  
  *(Note: This is our own custom addition, not part of the original AIKEN format.)*

### 🚨 Very Important AIKEN Authoring Guidelines

- The answer options (A. B. C. D.) **must be in uppercase English letters followed by a period and a space** — e.g., `C.`
- Each part of the question (the question itself, each answer option, the answer line, and the feedback) **must be on a separate line.**

---

## ✅ Output

For every `.txt` file, a corresponding `.xml` file is generated **in the same folder** with the same base name:

- `quiz.txt` → `quiz.xml`
- `math/quiz1.txt` → `math/quiz1.xml`

---

## ⚙️ Features & Rules

| Feature | Behavior |
| --- | --- |
| 🔍 File Discovery | Automatically scans all subfolders, **excluding** the `ready` folder |
| 🧠 Answer Numbering | Always uses `<answernumbering>ABCD</answernumbering>` |
| 📥 Grade Per Question | Prompted from the user at runtime (per `.txt` file) |
| ♻️ Shuffle Answers | Always set to `<shuffleanswers>false</shuffleanswers>` |
| 💬 Feedback | Extracted from the `FEEDBACK:` line and added as `<generalfeedback>` |
| ✨ Output Format | Clean, well-formatted Moodle-compatible XML |
| 🛡️ Default Grade | Stored as float with 7 decimal places (e.g., `1.0000000`) |

---

## 🚀 How to Use

1. If you're using the `.exe` version, simply run the `aiken2moodle.exe` in the same folder as your quiz file.
  
2. If you're using the `.py` version, follow these steps:
  
  1. Place the script in the root folder that contains your `.txt` quiz files or subfolders with them.
  2. Run the script:
    
    ```bash
    python aiken2moodle.py
    ```
    
3. When prompted, enter the **default grade per question** (e.g., `1`, `0.5`, `2.5`).
  
4. The script will:
  

- Discover all valid quiz files
- Parse the questions
- Generate `.xml` files in place

```
/my_quizzes/
├── script.py
├── quiz.txt
├── history/
│   └── kouiz1.txt
└── science/
    └── quiz3.txt
```

---

## ✅ Summary Checklist

- [ ] Create your quiz using the AIKEN format as described above.
- [ ] Save the file as `quiz.txt` or `kouiz.txt` — ideally with a number at the end, e.g., `quiz1.txt` or `kouiz1.txt`.
- [ ] Ensure the `.txt` file is in the same folder as the script or inside a subfolder.
- [ ] Run the script.
- [ ] Enter the desired grade per question when prompted.
- [ ] After the conversion is complete, move the processed folders to the `ready` folder.
