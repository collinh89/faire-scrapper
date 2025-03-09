from bs4 import BeautifulSoup

def getSizes(soup):
    sizes = []

    radioGroup = soup.find('div', role='radiogroup')
    if(radioGroup):
        sizebtns = radioGroup.find_all('button')
        for sizebtn in sizebtns:
            sizes.append(sizebtn.text)

    sizeDiv = soup.find('div', class_='sc-5b13d4dd-0 jvasCg f_flex_base f_flex_single_value_align f_flex_single_value_direction')
    if(sizeDiv):
        sizebtns = sizeDiv.find_all('div', class_='f_flex_base f_flex_single_value_gap f_flex_single_value_direction')
        sizes = []
        for sizebtn in sizebtns:
            size = sizebtn.find('p', class_='f_t_base f_t_color f_t_paragraphSansRegular')
            sizes.append(size.text)

    return sizes

