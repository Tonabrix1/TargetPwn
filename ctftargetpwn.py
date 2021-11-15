"""
Don't use this for bad stuff, I'm not liable if you do.
"""
import itertools, re, requests, time, itertools
from bs4 import BeautifulSoup

final_kws = set()
impyears = None
fname = lname = None
mnames = None
trans = {
        **dict.fromkeys(['l','I','i'],'1'),
        **dict.fromkeys(['e','E'],'3'),
        **dict.fromkeys(['a','A'],'4'),
        **dict.fromkeys(['g','G'],'6'),
        **dict.fromkeys(['o','O'],'0'),
        **dict.fromkeys(['t','T'],'7'),
        **dict.fromkeys(['s','S'],'5')
        }

def init():
    datatypes = None
    while datatypes is None or len(datatypes) <= 0:
        datatypes = input("""Please enter a list of the types of data you have according to the following list:
        1: name (any number of middle names can be entered)
        2: nicknames/handles
        3: important dates (birthdays, events, etc; i.e. June 1st, 2005 would be 06012005)
        4: relevant words (favorite colors, seasons, people, etc)
        5: terms to search google for (terms related to interests and hobbies)
        Simply write each number that you have corresponding data for and data entry will begin.
        ----------------------------------------------------------------------------------\n""")
    process(datatypes)
    actiontypes = None
    while actiontypes is None or len(actiontypes) <= 0:
        actiontypes = input("""Please enter a list of the types of mutations that should be applied to the list
        1: leet
        2: case permutations
        3: common beginnings
        4: common endings
        5: aggressive mode <- allows 3 words to be combined before mutations
        6: first uppercase
        (any more than 3 and your wordlists will become hundreds of gigabytes large)
        (also it's probably smart not to mix kinds of mutation for the same reason)
        Simply write each number that you have corresponding data for and data wrangling will begin.
        ----------------------------------------------------------------------------------\n""")
    generate(actiontypes)

#generates preliminary data
def process(dat):
    global fname, mnames, lname, impyears, searchterms
    mnames = []
    searchterms = []
    if '1' in dat:
        ans = None
        fname = input("Please enter first name: ")
        while ans != "":
            ans = input("Please enter a middle name: ")
            if len(ans) > 0: mnames.append(ans)
        lname = input("Please enter last name: ")
    if '2' in dat:
        ans = None
        while ans != "":
            ans = input("Please input nicknames: ")
            # gets added directly to final_kws so no wrangle method needed
            if len(ans) >= 1: final_kws.add(ans)
    if '3' in dat:
        impyears = []
        ans = None
        while ans != "":
            ans = input("Please input any important years: ")
            if len(ans) >= 1: impyears.append(ans)
    if '4' in dat:
        ans = None
        while ans != "":
            ans = input("Please input any relevant words: ")
            # gets added directly to final_kws so no wrangle method needed
            if len(ans) >= 1: final_kws.add(ans)
    if '5' in dat:
        ans = None
        while ans !=  "":
            ans = input("Please input any relevant search terms: ")
            if len(ans) >= 1: searchterms.append(ans)


#generates the final wordlist
def generate(dat):
    global final_kws, searchterms, impyears, fname
    begin = time.time()
    if len(searchterms) > 0:
        final_kws.update(multisearch(searchterms))
    if fname is not None: wranglenames()
    if impyears: wrangleyears()
    with open("/home/tona/Desktop/randbash/wordlists/commonexcludes.txt",'r') as ex:
        ex=ex.read()
        ll = len(ex.split("\n"))
        cn = 0
        print(f"Filtering out {ll} common words")
        for w in ex.split("\n"):
            w = w.lower()
            if w in final_kws:
                final_kws.remove(w)
                cn += 1
        print(f"Found {cn} matches to filter.")
    temp = final_kws.copy()
    if '1' in dat:
        st = time.time()
        leet(temp)
        print(f"Finished leet permutations after {time.time()-st} seconds.")
    if '2' in dat:
        st = time.time()
        for w in temp:
                final_kws.update(caseperm(w))
        print(f"Finished caseperm after {time.time()-st} seconds.")
    if '3' in dat:
        n = int(input("Please enter the depth (max number of characters) to use: "))
        commonbeginnings(n)
    if '4' in dat:
        n = int(input("Please enter the depth (max number of characters) to use: "))
        commonendings(n)
    if '5' in dat:
        finish(3, begin)
        return
    if '6' in dat:
        for w in temp:
            final_kws.add(w[0].upper()+w[1:])
    finish(2, begin)



#adds common endings, just adds them directly instead of returning a list to concat
def commonendings(d=1):
    global final_kws
    common = ['1','2','3','4','5','6','7','8','9','0','`','~','!','@','#','$','%','^','&','*','(',')','?','.',',','>','<']
    for i in range(d):
        common = combinations(common,d) if d > 1 else common
        temp = final_kws.copy()
        for w in temp:
            for l in common:
                final_kws.add(w+''.join(l))

#adds common beginnings, just adds them directly instead of returning a list to concat
def commonbeginnings(d=1):
    global final_kws
    common = ['1','2','3','4','5','6','7','8','9','0','`','~','!','@','#','$','%','^','&','*','(',')','?','.',',','>','<']
    for i in range(d):
        common = combinations(common,d) if d > 1 else common
        temp = final_kws.copy()
        for w in temp:
            for l in common:
                final_kws.add(''.join(l)+w)


#generates likely formats for names to be used in passwords
def wranglenames():
    global fname, mnames, lname, final_kws
    print("Wrangling names...")
    final_kws.add(fname)
    final_kws.add(lname)
    final_kws.add(fname+lname)
    final_kws.add(lname+fname)
    final_kws.add(lname[0]+fname)
    final_kws.add(fname+lname[0])
    final_kws.add(fname[0]+lname)
    if type(list()) == type(mnames):
        for n in mnames:
            final_kws.add(n)
            final_kws.add(fname+n[0]+lname[0])
            final_kws.add(fname+n)
            final_kws.add(fname+n+lname)
    else:
        final_kws.add(mnames)
        final_kws.add(fname+mnames[0]+lname[0])
        final_kws.add(fname+mnames)
        final_kws.add(fname+mnames+lname)


#generates likely formats for years to be used in passwords
def wrangleyears():
    global impyears
    print("Wrangling years...")
    for y in impyears:
        final_kws.add(y)
        final_kws.add(y[-4:])
        final_kws.add(y[-2:])
        final_kws.add(y[-6:2]+y[-2:])
        final_kws.add((y[1] if y[0] == "0" else y[0:2])+(y[3] if y[2]=="0" else y[2:2])+y[-2:])


#generates leet passwords
def leet(lst):
    global trans
    st = time.time()
    print("Starting leet mutation")
    # cleans the list, it is looping through the whole base list once but it's generally small
    # and is wayyyy better than generating billions of leet mutations bc you have 10 vowel words
    goodstrings = set()
    for s in lst:
        check = 0
        for char in s:
            if trans.get(char) is not None: check += 1
        if check <= 7: goodstrings.add(s)
    for s in goodstrings:
        kwlen = len(final_kws)
        recfromdict(s,trans,0)
        if kwlen + 10000 <= len(final_kws): print(f"Num keywords {len(final_kws)}, last kw: {final_kws[-1]}")
    print(f"Permutations complete after {time.time()-st} seconds")


#generates all permutations of upper and lowercase for a given word
def caseperm(s):
    return map(''.join,itertools.product(*zip(s.upper(),s.lower())))


#grabs flag parameters
def grabflag(msg, flag):
    msg = msg.split(flag)
    outp = []
    if msg is None:
        print("flag: " + flag + " not found.")
        return None
    elif len(msg) <= 1:
        print("argument for flag: " + flag + " not found.")
        return None
    elif len(msg) > 2:
        for i in range(len(msg)):
            if i%2==0: outp.append(msg[i])
    else: outp = msg[1]
    return outp


#generates all possible permutations of a string from dict
def recfromdict(s,d,c):
    global final_kws
    if s not in final_kws: final_kws.add(s)
    for i in range(len(s)):
        if i <= c: continue
        l = s[i]
        if d.get(l) is not None:
            recfromdict(''.join(s),d,i)
            s = list(s)
            s[i] = d.get(l)
            recfromdict(''.join(s),d,0)


#scrapes google for links relating to a search term
def google_search(term):
    excludes = ["youtube.com","gstatic.com","w3.org","google.com","amazon.com","tv.apple.com","play.hbo"]
    term = term.replace("+","%2B")
    term = term.replace(" ","+")
    httpcmp = re.compile('"http://(.+?)"')
    httpscmp = re.compile('"https://(.+?)"')
    host = (f'http://www.google.com/search?channel=fs&client=ubuntu&q={term}')
    head = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
    print(f"searching {host}")
    resp = requests.get(host,headers=head)
    links = httpcmp.findall(resp.text)
    links.append(httpscmp.findall(resp.text))
    outp = set()
    for l in links:
        for lnk in l:
            add = True
            if len(lnk) <= 5: continue
            for e in excludes:
                if e in lnk:
                    add = False
            if add: outp.add(lnk)
    print(f'{len(outp)} links found')
    return outp


#scrapes sites for capital words to aggregate lists of keywords
def find_keywords(urls: list,max=False):
    checked = []
    s = requests.Session()
    kw = set()
    total = len(urls)
    c = 0
    parserfails = [';','.','\'','"',':','#','$','%','!',',','/','\\','(',')','[',']','{','}','\xa0','\n','\\n'\
                    '?','&','’','”','+','|','~','`','_','=','●','-']
    for url in list(urls):
        if not max and c == 10: break
        urltocheck = url if "?" not in url else url.split("?")[0]
        urltocheck = url if "#" not in url else url.split("#")[0]
        if urltocheck in checked: continue
        if not url.startswith("http"): url = "http://"+url
        c += 1
        print(f"searching site {c} out of {total if max else 10}: {url}")
        try:
            resp = s.get(url).text
            url = url if "#" not in url else url.split("#")[0]
            url = url if "?" not in url else url.split("?")[0]
            checked.append(url)
        except Exception as e:
            print(f"Couldn't get link: {e}")
            continue
        parser = BeautifulSoup(resp, 'html.parser')
        for found in parser.find_all("p"):
            t = found.get_text()
            for l in t.split(" "):
                for fail in parserfails:
                    if fail in l: l = l.split(fail)[0]
                if len(l) > 0 and l[0].isupper(): kw.add(l.strip().lower())
    print(kw)
    print(f'{"-"*50}\n{len(kw)} keywords aggregated\n{"-"*50}')
    return kw

#simply generates all combinations of words in a list
def combinations(lst,rpt):
    o = itertools.product(lst,repeat=rpt)
    return o

def finish(stp, begin):
    global final_kws
    kws = final_kws
    print(f"total wordlist is size {len(kws)}")
    max = pow(len(kws),stp)
    if max > 100000000:
        check = input(f"Are you sure you want to save this list of {max} words?")
        if "no" in check.lower():
            print("Aborting...")
            return
    print(f"Creating a base list {max+len(kws)} words long")
    o = combinations(kws,stp)
    print(f"Combinations complete.")
    print("Writing to file...")
    start = time.time()
    count = 1
    with open("/home/tona/Desktop/randbash/wordlists/targeted.txt","w+") as tg:
        for w in kws:
            w = ''.join(w)
            tg.write(f"{w}\n")
            count += 1
            if count % 100000 == 0: print(f"Written #{count} - {int((count/max)*100)}% done: {w}")
        for w in o:
            w = ''.join(w)
            tg.write(f"{w}\n")
            count += 1
            if count % 100000 == 0: print(f"Written #{count} - {int((count/max)*100)}% done: {w}")
            if count == max: print(f"Writing complete, #{count} entries written, took {time.time()-start} seconds to write")
    print(f"Final wordlist can be found at ../../wordlists/targeted.txt, took {time.time()-begin} seconds total.")

#generates a list of keywords from many sites across multiple searches
def multisearch(terms:list):
    kws = set()
    print(f"{'-'*50}\nsearching google for {terms}\n{'-'*50}")
    for term in terms: kws.update(find_keywords(google_search(term)))
    return kws

#-------------------------------------------------------------------------------#
init()
