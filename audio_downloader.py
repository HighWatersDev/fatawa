import requests
from bs4 import BeautifulSoup


def download_ruhayli():
    def link_collector(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        return links

    def dl_file(url):
        print("Starting download...")
        response = requests.get(f'{base_url}{url}')
        try:
            with open(f'full_audio_files/{url.rsplit("upload/")[1]}', 'wb') as f:
                f.write(response.content)
                print("Wrote to file")
        except Exception as err:
            print(err)
            pass
        return True

    base_url = "https://www.sualruhaily.com/"
    url = "https://www.sualruhaily.com/catplay.php?catsmktba=69"

    books = link_collector(url)

    book_links = []
    for a in books:
        if 'كتاب' in a.get_text() and 'catplay.php?catsmktba=' in a.get('href'):
            book_links.append(a.get('href'))

    chapter_links = []
    lesson_links = []
    for book in book_links:
        chapters = link_collector(f'{base_url}{book}')
        for chapter in chapters:
            try:
                if ('باب' in chapter.get_text() or 'أقسام' in chapter.get_text())\
                        and 'catplay.php?catsmktba=' in chapter.get('href'):
                    chapter_links.append(chapter.get('href'))
                elif "linktable" in chapter.get('class') and "play.php?catsmktba=" in chapter.get('href'):
                    lesson_links.append(chapter.get('href'))
            except Exception as e:
                print(e)
                pass
    for ch in chapter_links:
        ch_links = link_collector(f'{base_url}{ch}')
        for lesson in ch_links:
            try:
                if "linktable" in lesson.get('class') and "play.php?catsmktba=" in lesson.get('href'):
                    lesson_links.append(lesson.get('href'))
            except Exception as e:
                print(e)
                pass

    download_links = []
    for i in lesson_links:
        dl_links = link_collector(f'{base_url}{i}')
        for dl_link in dl_links:
            try:
                if '.mp3' in dl_link.get('href'):
                    download_links.append(dl_link.get('href'))
            except Exception as e:
                print(e)
                pass

    print(download_links)
    for link in download_links:
        dl_file(link)
