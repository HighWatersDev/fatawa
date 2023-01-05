from itertools import islice


def fatawa_template_ar(title, q, a, audio_link):
    fatwa_template = f'''

<details>
< summary style={{{{fontWeight: "bold"}}}}>
{title} 📃
</summary>

**سؤال:** {q}

**جواب:** {a}

<audio controls>
<source src="{audio_link}"/>
</audio>

</details>

'''
    print(fatwa_template)


def fatawa_template_en(title, q, a):
    fatwa_template = f'''
<details>
<summary style={{{{fontWeight: "bold"}}}}>
{title} 📃
</summary>

**Q:** {q}

**A:** {a}

</details>    
'''
    print(fatwa_template)


def build_fatawa_ar(folder, file, audio_link):
    questions = []
    answers = []
    with open(f'transcriptions/{folder}/{file}', 'r') as file1, \
         open(f'transcriptions/{folder}/{file}', 'r') as file2:
        for line1 in islice(file1, 0, None, 2):
            questions.append(line1.rstrip("\n"))
        for line2 in islice(file2, 1, None, 2):
            answers.append(line2.rstrip("\n"))
    for i in range(len(questions)):
        fatawa_template_ar("عنوان", questions[i], answers[i], audio_link)


def build_fatawa_en(folder, file):
    questions = []
    answers = []
    with open(f'translations/{folder}/{file}', 'r') as file1, \
         open(f'translations/{folder}/{file}', 'r') as file2:
        for line1 in islice(file1, 0, None, 2):
            questions.append(line1.rstrip("\n"))
        for line2 in islice(file2, 1, None, 2):
            answers.append(line2.rstrip("\n"))
    for i in range(len(questions)):
        fatawa_template_en("Title", questions[i], answers[i])
