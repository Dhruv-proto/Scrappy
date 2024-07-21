import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract

def get_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def is_same_domain(url, base_domain):
    return get_domain(url) == base_domain

def get_all_links(url, base_domain, visited):
    if url in visited:
        return []
    
    visited.add(url)
    links = []
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return links
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not href.startswith('http'):
            href = urljoin(url, href)
        if is_same_domain(href, base_domain) and href not in visited:
            links.append(href)
            links.extend(get_all_links(href, base_domain, visited))
    
    return links

def main():
    print("==================================================================================")
    print("\t\t\tWelcome to SCRAPPY!")
    print("==================================================================================\n")
    i=1
    while i==1:

        website = input("Enter the website domain name (e.g., example.com): ").strip()
        base_url = f"https://{website}"
        base_domain = get_domain(base_url)
        
        print(f"Gathering links for the domain: {base_domain}")
        
        visited = set()
        all_links = get_all_links(base_url, base_domain, visited)
        
        print(f"Total links found: {len(all_links)}")
        for link in all_links:
            print(link)
        choice=input("\nDo you want to scrap more domains(Y,n): ")
        if choice=='y' or choice=='Y':
            continue
        elif choice=='n' or choice=='N':
            print("Okay Byeeeeee!:)")
            i=0
        else:
            print("Error Has been occured. Shutting Down the program.")


if __name__ == "__main__":
    main()
