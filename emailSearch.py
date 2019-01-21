import re, requests
from googlesearch import search
from argparse import ArgumentParser

emailList = list()
emailList.clear()


def outputResults(path, resultList):
    with open(path, 'w') as output_file:
        for item in resultList:
            output_file.write("%s\n" % item)


def emailSearch(text):

    emailRegex = re.compile(r'''(
    
    (?:[a-z0-9!#$%&'*+=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])

    )''', re.VERBOSE)

    temp = re.findall(emailRegex,text)
    emails = {}

    for e,r,t,y,u in temp:
        emails.setdefault(e, []).append(e)


    if not emails:
        print("No emails found.")
    else:
        for i in emails:
            if "mailto:" in i:
                i = re.sub(r'mailto:','',i)
            print(str(i))
            if i not in emailList:
                emailList.append(i)


parser = ArgumentParser(description='Example use: python emailSearch.py -q site:example.com -m 100 -l eng -t com -o output.txt')
parser.add_argument('--query', '-q', help='Search engine query for email search.',default=None, type=str)
parser.add_argument('--max', '-m', help='Limit of the returned search results', default=20, type=int)
parser.add_argument('--output', '-o', help='Output filepath to save the results.', default=None, type=str)
parser.add_argument('--tld', '-t', help='Top-Level Domain of the search engine.', default='com', type=str)
parser.add_argument('--lang', '-l', help='Language of search.', default='eng', type=str)
parser.add_argument('--site','-s',help='Website to search.',default=None,type=str)

options = parser.parse_args()

current = 1

if options.query is not None:
    for url in search(str(options.query), stop=options.max, tld=options.tld, lang=options.lang):

        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            print("Connection error for " + url)
            continue

        print("[" + str(current) + " of " + str(options.max) + "]" + " Searching " + url + " for e-mails.")
        print("Response code: " + str(r.status_code))

        r_html = r.text

        emailSearch(r_html)
        current += 1

if options.site is not None:

    s=options.site

    try:
        r=requests.get(s)
    except requests.exceptions.ConnectionError:
        print("Connection error for " + s)
    print("Searching " + s + " for e-mails.")
    print("Response code: " + str(r.status_code))

    r_html = r.text

    emailSearch(r_html)

if options.output is not None:
    outputResults(options.output, emailList)
