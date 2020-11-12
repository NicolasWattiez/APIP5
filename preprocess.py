
def remove_html(text):
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text