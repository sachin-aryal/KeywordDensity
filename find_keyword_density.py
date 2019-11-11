import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
from googlesearch import search

stop =  stopwords.words("english")
interested = ["li", "h1", "p", "span", "h2", "h3", "h4", "h5", "h6", "a", "title", "dl"]

def get_word_list(url):
    wordlist = []
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')

    already_extracted_elements = []
    for level1_tags in soup.findAll(True):
        if level1_tags.name in interested and level1_tags not in already_extracted_elements:
            content = level1_tags.text
            words = content.lower().split()
            for each_word in words:
                wordlist.append(each_word)
            for child in level1_tags.children:
                already_extracted_elements.append(child)
    return wordlist

def clean_wordlist(wordlist):
    clean_list = []
    for word in wordlist:
        if word not in stop and len(word) > 2:
            symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/., '

            for i in range(0, len(symbols)):
                word = word.replace(symbols[i], '')

            if len(word) > 0:
                clean_list.append(word)
    return clean_list


def create_dictionary(clean_list):
    word_count = {}
    for word in clean_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


def save_output(word_count, count, link, number_of_keywords):
    c = Counter(word_count)
    # returns the most occuring elements
    top = c.most_common(number_of_keywords)
    total_count = sum(c.values())
    file_name = "{}_{}.txt".format(str(link).replace("/", "_"), str(count))
    with open(file_name, "w") as output_file:
        output_file.write("Link: {}\n".format(link))
        output_file.write("Keyword\tCount\tDensity\n")
        for each_tuple in top:
            output_file.write(each_tuple[0] + "\t" + str(each_tuple[1]) + "\t" + str((int(each_tuple[1]) / total_count) * 100)+"\n")
    print("Output written to: {}".format(file_name))


# Driver code
if __name__ == '__main__':

    # TODO
    """Please comment this after first download"""
    # nltk.download()
    query = "Influencer Marketing Agency"
    index = 0
    number_of_keywords = 20
    for link in search(query, num=10, stop=10, pause=2):
        print("Scrapping URL: {}".format(link))
        wordlist = get_word_list(link)
        clean_list = clean_wordlist(wordlist)
        word_count = create_dictionary(clean_list)
        save_output(word_count, index, link, number_of_keywords)
        index += 1