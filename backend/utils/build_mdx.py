# Need to re-work it to build fatawa from database not from text files

def fatawa_template_ar(topic, title, q, a, audio_link):
    fatwa_template = f'''
{topic}

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


def fatawa_template_en(topic, title, q, a):
    fatwa_template = f'''
{topic}

<details>
<summary style={{{{fontWeight: "bold"}}}}>
{title} 📃
</summary>

**Q:** {q}

**A:** {a}

</details>    
'''
    print(fatwa_template)


def build_fatawa(folder, file, audio_link):
    print("folder: ", folder, " file: ", file)
    with open(f'fatwa-transcription/{folder}/{file}', 'r') as file1:
        data = file1.readlines()
        fatawa_template_ar(topic=data[0].rstrip('\n'), title=data[1].rstrip('\n'), q=data[2].rstrip('\n'), a=data[3].rstrip('\n'), audio_link=audio_link)
    with open(f'fatwa-translation/{folder}/{file}', 'r') as file2:
        data = file2.readlines()
        fatawa_template_en(topic=data[0].rstrip('\n'), title=data[1].rstrip('\n'), q=data[2].rstrip('\n'), a=data[3].rstrip('\n'))
