from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from parse import search
from selenium import webdriver

class Scrapper:
    def __init__(self,user_name,password, driver_path):
        """
        Initiatilisaton of the class 
        ---------
        Inputs 
            user_name : instagram account user name
            password : instagram account password
            driver_path : local path to Chrome WebDriver
        """
        self.driver_path = driver_path
        self.user_name = user_name
        self.password = password

    def get_influencers_world(self):
        """
        Retrieving top 49 World Influencers from Wikipedia
        ---------
        Outputs :
            df : DataFrame with influencers' related infos
            df['Links to profile'].tolist() : list of the accounts' links
        """
        browser = webdriver.Chrome(executable_path=self.driver_path)

        url = "https://fr.m.wikipedia.org/wiki/Liste_des_comptes_Instagram_les_plus_suivis"
        browser.get(url)
        browser.implicitly_wait(10)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.quit()

        insta_acc_links_int=[]
        names_int=[]
        activity = []
        country=[]
        brand = []

        base = 'https://www.instagram.com/'

        inst_in = soup.find('table',attrs={'class':"wikitable sortable"})
        table = inst_in.find_all('tr')[2:]
        del table[2]
        for infl in table:

            info = infl.find_all('td')

            pseudo = info[0].text[1:]
            insta_acc_links_int.append(base + pseudo[:-1].replace(" ", "") + '/')

            nom_util = info[1].find('a').text
            names_int.append(nom_util)

            act = info[3].text
            activity.append(act[:-1])

            pays = info[4].find_all('a')[-1].text
            country.append(pays)

            marque = info[-1].text
            brand.append(marque[:-1])
        Influencers = {'Links to profile': insta_acc_links_int,
                    'Name': names_int,
                    'Activity': activity,
                    'Country': country,
                    'Brand': brand
                    }
        df = pd.DataFrame(Influencers, columns=['Links to profile','Name','Activity','Country','Brand'])
        return df,  df['Links to profile'].tolist()

    def connection_instagram(self):
        """
        Connecting to instagram and passing connection messages
        --------
        Outputs : 
            No object as outputs but gives the webdriver connected to Instagram
        """
        user_name = self.user_name
        password = self.password

        browser = webdriver.Chrome(executable_path=self.driver_path)
        browser.implicitly_wait(10)
        browser.get("https://www.instagram.com/")
        browser.find_element_by_xpath("//button[text()='Accepter']").click() #Accept or Accepter depends on language

        browser.implicitly_wait(10)

        username_input = browser.find_element_by_css_selector("input[name='username']")
        password_input = browser.find_element_by_css_selector("input[name='password']")

        browser.implicitly_wait(10)
        username_input.send_keys(user_name)
        browser.implicitly_wait(10)
        password_input.send_keys(password)

        login_button = browser.find_element_by_xpath("//button[@type='submit']")
        browser.implicitly_wait(10)
        login_button.click()

        try:
            browser.find_element_by_xpath("//button[text()='Not Now']").click() #for save info
            browser.implicitly_wait(10)
        except:
            browser.implicitly_wait(10)

        return browser

    def get_influencer_posts(self, df_infl, index_infl, browser, account_link, pause_time):
        """
        Get links of an influencer's posts and general information about the account
        ---------
        Input :
            df_infl : dataframe a set containing names of influencers and links to their publication
            inex_infl : index of the influencer in the dataframe df_infl
            browser : webdriver connected to Instagram to instagram
            account_link : link to the influencer's account
            pause_time : time (in seconds) to wait for loading when scrolling down the account page
        ---------
        Outputs :
            df : DataFrame containing the infos (posts links and account general infos)
        """
        insta_acc_links_int = df_infl['Links to profile'].tolist()
        names_int = df_infl['Name'].tolist()
        activity = df_infl['Activity'].tolist()

        lien_pub = []
        liens=[]
        noms=[]
        activité = []
        biographys = []
        nb_posts= []
        followers = []
        followings =[]
        verif_st = []
        publis =[]
        browser.implicitly_wait(6)

        browser.get(account_link)

        for i in range(40): #integer to change in order to scroll more over the page

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(pause_time) #to wait loading of old publications, may need to be changed

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            body = soup.find('body').find('div').find('section').find('main').find('div').find('article').find('div').find('div')
            pubs = body.find_all('div')
            base = 'https://www.instagram.com'
            for pub in pubs :
                pub_1 = pub.find_all('a')
                for p in pub_1:
                    p = p['href']
                    publis.append(base + p)

        publis_2 = list(np.unique(publis))
        print(len(publis_2))
        print("Lien du compte:" + str(account_link))
        browser.implicitly_wait(10)
        browser.get(account_link)

        try:
            biography_1 = str(browser.find_element_by_xpath('html/body/div/section/main/div/header/section/div[2]/h1').text)
        except:
            biography_1 = str(" ")
        try:
            biography_2 = str(browser.find_element_by_xpath('html/body/div/section/main/div/header/section/div[2]/span').text)
        except:
            biography_2 = str(" ")
        biography = biography_1 + str(" ") + biography_2
        print("Biographie:" + str(biography))

        number_of_posts = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/ul/li/span').text
        print("Nombre de posts:"+ str(number_of_posts))

        number_of_followers = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')
        print("Nombre de followers:"+ str(number_of_followers))

        try :
            number_of_followings = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/ul/li[3]/a/span').text
        except :
            number_of_followings = 0
        print("Nombre d'abonnement:" + str(number_of_followings))

        is_verified = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/div/div/span').text
        print("Statut:" + str(is_verified))

        browser.implicitly_wait(2)
        for pub in publis_2:
            lien_pub.append(pub)
            liens.append(insta_acc_links_int[index_infl])
            noms.append(names_int[index_infl])
            activité.append(activity[index_infl])

            biographys.append(biography)
            nb_posts.append(number_of_posts)
            followers.append(number_of_followers)
            followings.append(number_of_followings)
            verif_st.append(is_verified)


        df = pd.DataFrame({'Links to profile': liens,
                    'Links to publication' : lien_pub,
                        'Name Account/Influencer': noms,
                        'Professional Activity': activité,
                        'Account description':  biographys,
                        'Number of posts':  nb_posts,
                        'Number of followers':  followers,
                        'Number of followings':  followings,
                        'Verified Status': verif_st,
                        })
        return df

    def get_pub_info(self, pub, browser):
        """
        Retrieving informations for each posts of a list of publications
        ---------
        Input :
            pub : url adress of an instagram publication 
            browser : webdriver connected to instagram
        ---------
        Outputs :
            df : DataFrame of the collected informations for each post
        """

        pub_list = []
        cap_list = []
        nb_co_list = []
        nb_likes_list = []
        date_list = []
        typ_list = []
        print(pub)

        try:
            browser.get(pub)
            browser.implicitly_wait(4)
        except:
            browser.quit()
            browser = self.connection_instagram()
            browser.get(pub)
            browser.implicitly_wait(4)

        try:
            date = browser.find_element_by_xpath('/html/body/div/section/main/div/div/article/div[3]/div[2]/a/time').get_attribute('datetime')
        except:
            browser.implicitly_wait(10)
            try :
                browser.get(pub)
                date = browser.find_element_by_xpath('/html/body/div/section/main/div/div/article/div[3]/div[2]/a/time').get_attribute('datetime')
            except :
                browser.quit()
                browser = self.connection_instagram()
                browser.get(pub)
                date = browser.find_element_by_xpath('/html/body/div/section/main/div/div/article/div[3]/div[2]/a/time').get_attribute('datetime')

        try:
            try:
                nb_likes = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/div/button/span').text
                typ = "Photo"

            except:
                nb_likes= browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/span/span').text
                typ = "Video"
        except:
            browser.implicitly_wait(10)
            try :
                browser.get(pub)
                try:
                    nb_likes = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/div/button/span').text
                    typ = "Photo"
                except:
                    nb_likes= browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/span/span').text
                    typ = "Video"
            except :
                browser.quit()
                browser = self.connection_instagram()
                browser.get(pub)
                try:
                    nb_likes = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/div/button/span').text
                    typ = "Photo"

                except:
                    nb_likes= browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/span/span').text
                    typ = "Video"
        try:
            cap = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/div/ul/div/li/div/div/div[2]/span').text
        except:
            cap = "No caption"

        try:
            c_1 = browser.find_element_by_xpath("//*[contains(text(),'edge_media_to_parent_comment')]")
            c = c_1.get_attribute('text')
            co = search(':{"count":{nb},"page_info":',c)
            nb_co = int(co['nb'])
        except:
            nb_co = "No comment"

    
        print(cap)
        print(nb_co)
        print(nb_likes)
        print(date)
        print(typ)

        pub_list.append(pub)
        cap_list.append(cap)
        nb_co_list.append(nb_co)
        nb_likes_list.append(nb_likes)
        date_list.append(date)
        typ_list.append(typ)


        df = pd.DataFrame({'Links to publication' : pub_list,
                    'Post description': cap_list,
                    'Post number of comments': nb_co_list,
                    'Post number of likes' : nb_likes_list,
                    'Posting date': date_list,
                    'Media Type': typ_list
                    })

        return df
