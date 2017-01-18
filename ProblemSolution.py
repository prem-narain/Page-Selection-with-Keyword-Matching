from collections import OrderedDict
import re

max_weight = 0  #calculate maximum number of words in pages and queries for weight
global_word_list = dict() #dictionary for storing words and the page names they have occured
global_list_of_pages = dict() #dictionary for storing pages per thier page names
global_list_of_queries = list() #list for storing queries.

class factory:
    """
    factory class for pages and queries.
    """
    def __init__(self):
        self.name = ""
        self.word_list = dict()
        self.count = 99999
        self.listOfWords =list()
        self.sum = None

    def getName(self):
        return self.name

    def getWordList(self):
        return self.word_list

    def setName(self, name):
        self.name = name

    def setCount(self,count):
        self.count = count

    def setList(self,words):
        self.listOfWords = words

    def addToList(self):
        """
        assigns weight from a counter variable(set by maximum number obtained earlier) to the words
        :param words:
        """
        for word in self.listOfWords:
            if word not in self.word_list:
                self.word_list[word] = self.count - 1
                self.count -= 1


def add_to_global(words, pageName):
    """
    function to fill the global_word_list with words as keys and list of page name, where they have occurred.
    :param words: list of words
    :param pageName: current page name being processed.
    """
    for word in words:
        if word in global_word_list:
            global_word_list[word].append(pageName)
        else:
            global_word_list[word] = [pageName]


def create(value,i,type):
    """
    create page or query object and adds it to their respective global lists.
    :param value: string from input
    :param i: index for creating name of the page/query
    """
    page = factory()
    words = value.split()
    findMax(len(words))
    page.setList(words)
    if type is 'p':
        page.setName("P" + str(i + 1))
        add_to_global(words, page.getName())
        global_list_of_pages[page.getName()] = page
    else:
        page.setName("Q" + str(i + 1))
        global_list_of_queries.append(page)

def findMax(number):
    """
    function to check the current maximum and update if less then given number. To be used as variable weight.
    :param number: number to compared the max with
    """
    global max_weight
    if max_weight < number:
        max_weight = number

def searchMain():

    """
    Search For Pages
    """
    for query in global_list_of_queries:
        visited =list()
        d =dict()
        for word in query.getWordList():
            if word in global_word_list:
                for page in global_word_list[word]:
                    if page not in visited:
                        visited.append(page)
                        sop = sumOfProducts(query,global_list_of_pages[page])
                        d[page] = sop
        d = OrderedDict(sorted(d.items(), key=lambda x: (-x[1], (x[0][0], int(x[0][1:])))))
        forPrint(query.getName(),d)

def sumOfProducts(query,page):
    """
    function to calculate SOP of the query for this page.
    :param query: query object
    :param page: page object
    :return: SOP of the entire query for that page
    """
    sop = 0
    for qword in query.getWordList():
        if qword in page.getWordList():
            sop = sop + query.getWordList()[qword] * page.getWordList()[qword]
    return sop

def forPrint(name,Dict):
    """
    function for outputing the result.
    :param name: Query name
    :param Dict: Result of operation to be printed
    """
    print(name,':',end=" ")
    i = 0
    for key in Dict.keys():
        if i < 5:
            print(key, end=" ")
            i += 1
        if i >= 5:
            break
    print("")

def assignWeights():
    """
    assigns weights to each word of each query and object,
    based on the maximum number being calculated earlier

    """
    for key,page in global_list_of_pages.items():
        page.setCount(max_weight)
        page.addToList()
    for query in global_list_of_queries:
        query.setCount(max_weight)
        query.addToList()

def readFromFile():
        """
        reads input from file in same directory and prints the obtained input in console.
        Name the file as input and in txt format.
        """
        print("Input read from input.txt file : ")
        f = open('input.txt','r')
        page_index =0
        query_index = 0
        for line in f:
            print(line,end="")
            if line[0] is 'P':
                create(line[1:],page_index,'p')
                page_index += 1

            if line[0] is 'Q':
                create(line[1:],query_index,'q')
                query_index += 1
        print("\n")


if __name__ == '__main__':
    readFromFile()
    assignWeights()
    searchMain()
