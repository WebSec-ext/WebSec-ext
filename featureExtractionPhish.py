import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import *
import whois
from datetime import datetime
import time
from dateutil.parser import parse as date_parse



# Calculates number of months
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# Generate data set by extracting the features from the URL
def generate_data_set(url):

    data_set = []
    li = []

    having_IP_Address = None
    URL_Length = None
    Shortining_Service = None   
    having_At_Symbol = None
    double_slash_redirecting = None
    Prefix_Suffix = None
    having_Sub_Domain = None
    SSLfinal_State = None
    Domain_registeration_length = None
    Favicon = None
    port = None
    HTTPS_token = None
    Request_URL = None
    URL_of_Anchor = None
    Links_in_tags = None
    SFH = None
    Submitting_to_email = None
    Abnormal_URL = None
    Redirect = None
    on_mouseover = None
    RightClick = None
    popUpWidnow = None
    Iframe = None
    age_of_domain = None
    DNSRecord = None
    web_traffic = None
    Page_Rank = None
    Google_Index = None
    Links_pointing_to_page = None
    Statistical_report = None

    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url


    # Stores the response of the given URL
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999


    # Extracts domain from the given URL
    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.",domain):
	       domain = domain.replace("www.","")

    # Requests all the information about the domain
    whois_response = whois.whois(domain)

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })

    # Extracts global rank of the website
    try:
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1

    # 1.having_IP_Address
    try:
        ipaddress.ip_address(url)
        having_IP_Address = -1
        data_set.append(-1)
    except:
        having_IP_Address = 1
        data_set.append(1)

    # 2.URL_Length
    if len(url) < 54:
        URL_Length = 1
        data_set.append(1)
    elif len(url) >= 54 and len(url) <= 75:
        URL_Length = 0
        data_set.append(0)
    else:
        URL_Length = -1
        data_set.append(-1)

    # 3.Shortining_Service
    match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
    if match:
        Shortining_Service = -1
        data_set.append(-1)
    else:
        Shortining_Service = 1
        data_set.append(1)

    # 4.having_At_Symbol
    if re.findall("@", url):
        having_At_Symbol = -1
        data_set.append(-1)
    else:
        having_At_Symbol = 1
        data_set.append(1)

    # 5.double_slash_redirecting
    list=[x.start(0) for x in re.finditer('//', url)]
    if list[len(list)-1]>6:
        double_slash_redirecting = -1
        data_set.append(-1)
    else:
        double_slash_redirecting = 1
        data_set.append(1)

    # 6.Prefix_Suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        Prefix_Suffix = -1
        data_set.append(-1)
    else:
        Prefix_Suffix = 1
        data_set.append(1)

    # 7.having_Sub_Domain
    if len(re.findall("\.", url)) == 1:
        having_Sub_Domain = 1
        data_set.append(1)
    elif len(re.findall("\.", url)) == 2:
        having_Sub_Domain = 0
        data_set.append(0)
    else:
        having_Sub_Domain = -1
        data_set.append(-1)

    # 8.SSLfinal_State
    try:
        if response.text:
            SSLfinal_State = 1
            data_set.append(1)
        else:
            SSLfinal_State = -1
    except:
        SSLfinal_State = -1
        data_set.append(-1)

    # 9.Domain_registeration_length
    expiration_date = whois_response.expiration_date
    registration_length = 0
    try:
        expiration_date = min(expiration_date)
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = abs((expiration_date - today).days)

        if registration_length / 365 <= 1:
            Domain_registeration_length = -1
            data_set.append(-1)
        else:
            Domain_registeration_length = 1
            data_set.append(1)
    except:
        Domain_registeration_length = -1
        data_set.append(-1)

    # 10.Favicon
    Favicon = -1
    if soup == -999:
        Favicon = -1
        data_set.append(-1)
    else:
        try:
            for head in soup.find_all('head'):
                for head.link in soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                    if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                        Favicon = 1
                        data_set.append(1)
                        raise StopIteration
                    else:
                        Favicon = -1
                        data_set.append(-1)
                        raise StopIteration
        except StopIteration:
            pass

    #11. port
    try:
        port = domain.split(":")[1]
        if port:
            port = -1
            data_set.append(-1)
        else:
            port = 1
            data_set.append(1)
    except:
        port = 1
        data_set.append(1)

    #12. HTTPS_token
    if re.findall(r"^https://", url):
        HTTPS_token = 1
        data_set.append(1)
    else:
        HTTPS_token = -1
        data_set.append(-1)

    #13. Request_URL
    i = 0
    success = 0
    if soup == -999:
        Request_URL = -1
        data_set.append(-1)
    else:
        for img in soup.find_all('img', src= True):
            dots= [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        for audio in soup.find_all('audio', src= True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        for embed in soup.find_all('embed', src= True):
            dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        for iframe in soup.find_all('iframe', src= True):
            dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        try:
            percentage = success/float(i) * 100
            if percentage < 22.0 :
                Request_URL = 1
                dataset.append(1)
            elif((percentage >= 22.0) and (percentage < 61.0)) :
                Request_URL = 0
                data_set.append(0)
            else :
                Request_URL = -1
                data_set.append(-1)
        except:
            Request_URL = 1
            data_set.append(1)



    #14. URL_of_Anchor
    percentage = 0
    i = 0
    unsafe=0
    if soup == -999:
        URL_of_Anchor = -1
        data_set.append(-1)
    else:
        for a in soup.find_all('a', href=True):
        # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
                # there in the actual a['href']
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
        except:
            URL_of_Anchor = 1
            data_set.append(1)

        if percentage < 31.0:
            URL_of_Anchor = 1
            data_set.append(1)
        elif ((percentage >= 31.0) and (percentage < 67.0)):
            URL_of_Anchor = 0
            data_set.append(0)
        else:
            URL_of_Anchor = -1
            data_set.append(-1)

    #15. Links_in_tags
    i=0
    success =0
    if soup == -999:
        Links_in_tags = -1
        data_set.append(-1)
    else:
        for link in soup.find_all('link', href= True):
            dots=[x.start(0) for x in re.finditer('\.',link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots)==1:
                success = success + 1
            i=i+1

        for script in soup.find_all('script', src= True):
            dots=[x.start(0) for x in re.finditer('\.',script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots)==1 :
                success = success + 1
            i=i+1
        try:
            percentage = success / float(i) * 100
        except:
            Links_in_tags = 1
            data_set.append(1)

        if percentage < 17.0 :
            Links_in_tags = 1
            data_set.append(1)
        elif((percentage >= 17.0) and (percentage < 81.0)) :
            Links_in_tags = 0
            data_set.append(0)
        else :
            Links_in_tags = -1
            data_set.append(-1)

        #16. SFH
        SFH = -1
        for form in soup.find_all('form', action= True):
            if form['action'] =="" or form['action'] == "about:blank" :
                SFH = -1
                data_set.append(-1)
                break
            elif url not in form['action'] and domain not in form['action']:
                SFH = 0
                data_set.append(0)
                break
            else:
                SFH = 1
                data_set.append(1)
                break

    #17. Submitting_to_email
    if response == "":
        Submitting_to_email = -1
        data_set.append(-1)
    else:
        if re.findall(r"[mail\(\)|mailto:?]", response.text):
            Submitting_to_email = 1
            data_set.append(1)
        else:
            Submitting_to_email = -1
            data_set.append(-1)

    #18. Abnormal_URL
    if response == "":
        Abnormal_URL = -1
        data_set.append(-1)
    else:
        if response.text == "":
            Abnormal_URL = 1
            data_set.append(1)
        else:
            Abnormal_URL = -1
            data_set.append(-1)

    #19. Redirect
    if response == "":
        Redirect = -1
        data_set.append(-1)
    else:
        if len(response.history) <= 1:
            Redirect = -1
            data_set.append(-1)
        elif len(response.history) <= 4:
            Redirect = 0
            data_set.append(0)
        else:
            Redirect = 1
            data_set.append(1)

    #20. on_mouseover
    if response == "" :
        on_mouseover = -1
        data_set.append(-1)
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            on_mouseover = 1
            data_set.append(1)
        else:
            on_mouseover = -1
            data_set.append(-1)

    #21. RightClick
    if response == "":
        RightClick = -1
        data_set.append(-1)
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            RightClick = 1
            data_set.append(1)
        else:
            RightClick = -1
            data_set.append(-1)

    #22. popUpWidnow
    if response == "":
        popUpWidnow = -1
        data_set.append(-1)
    else:
        if re.findall(r"alert\(", response.text):
            popUpWidnow = 1
            data_set.append(1)
        else:
            popUpWidnow = -1
            data_set.append(-1)

    #23. Iframe
    if response == "":
        Iframe = -1
        data_set.append(-1)
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            Iframe = 1
            data_set.append(1)
        else:
            Iframe = -1
            data_set.append(-1)

    #24. age_of_domain
    if response == "":
        age_of_domain = -1
        data_set.append(-1)
    else:
        try:
            registration_date = re.findall(r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
            if diff_month(date.today(), date_parse(registration_date)) >= 6:
                age_of_domain = -1
                data_set.append(-1)
            else:
                age_of_domain = 1
                data_set.append(1)
        except:
            age_of_domain = 1
            data_set.append(1)

    #25. DNSRecord
    dns = 1
    try:
        d = whois.whois(domain)
    except:
        dns=-1
    if dns == -1:
        DNSRecord = -1
        data_set.append(-1)
    else:
        if registration_length / 365 <= 1:
            DNSRecord = -1
            data_set.append(-1)
        else:
            DNSRecord = 1
            data_set.append(1)

    #26. web_traffic
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank= int(rank)
        if (rank<100000):
            web_traffic = 1
            data_set.append(1)
        else:
            web_traffic = 0
            data_set.append(0)
    except TypeError:
        web_traffic = -1
        data_set.append(-1)

    #27. Page_Rank
    try:
        if global_rank > 0 and global_rank < 100000:
            Page_Rank = -1
            data_set.append(-1)
        else:
            Page_Rank = 1
            data_set.append(1)
    except:
        Page_Rank = 1
        data_set.append(1)

    #28. Google_Index
    site=search(url, 5)
    if site:
        Google_Index = 1
        data_set.append(1)
    else:
        Google_Index = -1
        data_set.append(-1)

    #29. Links_pointing_to_page
    if response == "":
        Links_pointing_to_page = -1
        data_set.append(-1)
    else:
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            Links_pointing_to_page = 1
            data_set.append(1)
        elif number_of_links <= 2:
            Links_pointing_to_page = 0
            data_set.append(0)
        else:
            Links_pointing_to_page = -1
            data_set.append(-1)

    #30. Statistical_report
    url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address=socket.gethostbyname(domain)
        ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                           '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                           '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                           '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                           '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                           '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)
        if url_match:
            Statistical_report = -1
            data_set.append(-1)
        elif ip_match:
            Statistical_report = -1
            data_set.append(-1)
        else:
            Statistical_report = 1
            data_set.append(1)
    except:
        Statistical_report = 1
        data_set.append(1)

    #print("Final")
    #print(data_set)

    if having_IP_Address==None:
        having_IP_Address = 1
    if URL_Length==None:
        URL_Length = 1
    if Shortining_Service==None:
        Shortining_Service = 1
    if having_At_Symbol==None:
        having_At_Symbol = 1
    if double_slash_redirecting==None:
        double_slash_redirecting = 1
    if Prefix_Suffix==None:
        Prefix_Suffix = 1
    if having_Sub_Domain==None:
        having_Sub_Domain = -1
    if SSLfinal_State==None:
        SSLfinal_State = -1
    if Domain_registeration_length==None:
        Domain_registeration_length = -1
    if Favicon==None:
        Favicon = -1
    if port==None:
        port = 1
    if HTTPS_token==None:
        HTTPS_token = -1
    if Request_URL==None:
        Request_URL = -1
    if URL_of_Anchor==None:
        URL_of_Anchor = -1
    if Links_in_tags==None:
        Links_in_tags = -1
    if SFH==None:
        SFH = -1
    if Submitting_to_email==None:
        Submitting_to_email = -1
    if Abnormal_URL==None:
        Abnormal_URL = -1
    if Redirect==None:
        Redirect = -1
    if on_mouseover==None:
        on_mouseover = -1
    if RightClick==None:
        RightClick = -1
    if popUpWidnow==None:
        popUpWidnow = -1
    if Iframe==None:
        Iframe = -1
    if age_of_domain==None:
        age_of_domain = -1
    if DNSRecord==None:
        DNSRecord = -1
    if web_traffic==None:
        web_traffic = -1
    if Page_Rank==None:
        Page_Rank = 1
    if Google_Index==None:
        Google_Index = -1
    if Links_pointing_to_page==None:
        Links_pointing_to_page = -1
    if Statistical_report==None:
        Statistical_report = 1


    li.append(having_IP_Address)
    li.append(URL_Length)
    li.append(Shortining_Service)
    li.append(having_At_Symbol)
    li.append(double_slash_redirecting)
    li.append(Prefix_Suffix)
    li.append(having_Sub_Domain)
    li.append(SSLfinal_State)
    li.append(Domain_registeration_length)
    li.append(Favicon)
    li.append(port)
    li.append(HTTPS_token)
    li.append(Request_URL)
    li.append(URL_of_Anchor)
    li.append(Links_in_tags)
    li.append(SFH)
    li.append(Submitting_to_email)
    li.append(Abnormal_URL)
    li.append(Redirect)
    li.append(on_mouseover)
    li.append(RightClick)
    li.append(popUpWidnow)
    li.append(Iframe)
    li.append(age_of_domain)
    li.append(DNSRecord)
    li.append(web_traffic)
    li.append(Page_Rank)
    li.append(Google_Index)
    li.append(Links_pointing_to_page)
    li.append(Statistical_report)

    #print("new List")
    #print(li)
    #return data_set

    return li