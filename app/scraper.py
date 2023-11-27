from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


class Scraper():
    def __init__(self):
        # Set up Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run Chrome in headless mode to avoid opening a browser window
        self.chrome_options.add_argument("--disable-dev-sha-usage")
        self.chrome_options.add_argument("--no-sandbox")
        # Create a WebDriver instance
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=self.chrome_options)
        self.url = "https://www.facebook.com/lyceena"
        self.ans={}

    def scrapedata(self):
        self.get_pubs()
        self.get_contact_basic_info()
        self.get_about_details()
        return self.ans

    def get_contact_basic_info(self):
        url = self.url+'/about'

        self.driver.get(url)

        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
       
        try:
            self.scroll_down_page()
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.find_all(class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xi81zsa x1s688f')
            page_name=soup.find(class_="x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz").text
            self.ans['Page']=page_name
            self.ans['Likes']=elements[0].text
            self.ans['Followers']=elements[1].text
        except:
            self.ans['Likes']='Nothing Found'
            self.ans['Followers']='Nothing Found'
        try:
            info_section = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, './/div[@class="x1iyjqo2"]'))
        )
            info_section = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'.//*[contains(@class,"xyamay9")]')))  #xyamay9 xqmdsaz x1gan7if x1swvt13
            info_elements = info_section.find_elements(By.XPATH,'*') #x1gan7if   All Direct Childs
        
            for info in info_elements:
                # info_values="null_default"
                info_category=info.find_element(By.XPATH,'.//*[contains(@class,"xieb3on")]') #checkk
                # print("     ",info_category.text)
                category_key = info_category.text
                siblings = info_category.find_elements(By.XPATH, 'following-sibling::*')
                info_values =[info_ele.text for info_ele in siblings]

                info_values_list=[]
                for value in info_values:
                    if '\n' in value:
                        val, key = value.split('\n', 1)
                        info_values_list.append({key.strip(): val.strip()})
                    else:
                        info_values_list.append(value.strip())

                if len(info_values_list) == 1: 
                    self.ans[category_key] = info_values_list[0]
                else:
                    self.ans[category_key] = info_values_list
        except:
            print('info sess not found')
        return(self.ans)

    def get_about_details(self):
        url = self.url+"/about_details"

        self.driver.get(url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.scroll_down_page()
        try:
            info_section=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(By.XPATH,'.//div[@class="xat24cr"]'))
            self.ans['About_details']=info_section.text
        except Exception as e:
            self.ans['About_details']='No_About_details_Found'
        return(self.ans)

    def get_pubs(self):
        pubs=[]

        self.driver.get(self.url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        try:
            
            self.scroll_down_page()
            #locate the publications each stored in a div with the same class name
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.find_all(class_='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z')

            for element in elements:
                ele={}
                try:
                    ele['Content']=element.find(class_="x1iorvi4 x1pi30zi x1l90r2v x1swvt13").text
                except:
                    ele['Content']='Nothing Found'
                try:
                    ele['Date_Shared']=(element.find(class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm").text)
                except:
                    ele['Date_Shared']='Nothing Found'
                try:
                    ele['Reactions_count']=element.find(class_="xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk").text
                except:
                    ele['reactions']="No_Reactions"
                try:
                    reactions=element.find(class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj")
                    reactions=reactions.find_all(class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn")
                    reac_list=[]
                    for reaction in reactions:
                        reac_list.append(reaction.text)
                    ele['Comments/Share']=reac_list
                    pubs.append(ele)
                except:
                    ele['Comments/Share']=[]

            self.ans['publications']=pubs
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return(self.ans)
    
    def scroll_down_page(self,speed=8):
        # Locate the email pw banner and wait for it to be clickable
        banner_element = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, './/*[contains(@class,"x92rtbv")]')))
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, './/*[contains(@class,"x92rtbv")]')))

        # Perform a click on the close element
        banner_element.click()

        current_scroll_position = 0

        current_scroll_position = 0
        duration = 10  # in seconds
        end_time = time.time() + duration
        while time.time() < end_time:
            current_scroll_position += speed
            self.driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            time.sleep(0.5)
