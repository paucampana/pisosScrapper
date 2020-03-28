def get_string_from_class (soup, tagName, className):
    result = soup.find(tagName,attrs={'class':className})
    result = get_text(result)
    return result;

def get_string_from_class_last (soup, tagName, className):
    result = soup.findAll(tagName,attrs={'class':className})
    if len(result) != 0:
        result = result[-1]
        result = get_text(result)
    else:
        result = ""
    return result;

def get_a_link_from_class (soup, tagName, className):
    result = soup.find(tagName,attrs={'class':className})
    result = get_a_link(result)
    return result;

def get_one (soup, tagName):
    result = soup.find(tagName)
    return result;



def get_string_from_id (soup, tagName, idName):
    result = soup.find(tagName, id=idName)
    result = get_text(result)
    return result;

def get_input_value_from_id (soup, tagName, idName):
    minput = soup.find(tagName, id=idName)
    result = ""
    if minput is not None:
        if minput.has_attr('value'):
            result = minput['value']
    return result;


def get_all_elements_ul (soup, tagName, className):
    ul = soup.find(tagName,attrs={'class':className})
    result = []
    if ul is not None:
        elements = ul.findAll("li")
        for elem in elements:
            result.append(get_text(elem))
    return ', '.join(result);

def get_all_elements_ul_by_id (soup, tagName, idName):
    ul = soup.find(tagName,id=idName)

    result = []
    if ul is not None:
        elements = ul.findAll("li")
        for elem in elements:
            #print(elem)
            img = get_one(elem, "img")
            if img is not None:
                result.append(get_src(img))

    return ', '.join(result);



def get_last_string(text):
    result = text.split()[2]
    return result;

def delete_empty_lines (text):
    text.split('\n')
    list_lines = []
    for line in text.split('\n'): 
        if line.strip():
            list_lines.append(line)
    return  ''.join(list_lines);


def string_one_line(text):
    return text.replace('\n', ' ')


def get_text(mtext):
    result = mtext
    if mtext is not None:
        result = mtext.text.strip()
    else:
        result = ""
    return result


def get_a_link(mtext):
    result = mtext
    if mtext is not None:
        result = "https:" + mtext['href']
    else:
        result = ""
    return result

def get_src(mtext):
    result = mtext
    if mtext is not None:
        result = mtext['src']
    else:
        result = ""
    return result


def get_first_word(mtext):
    mtext = mtext.replace('\xa0',' ')
    return mtext.split(" ")[0]
