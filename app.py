import requests
from bs4 import BeautifulSoup
from datetime import date
print(date.today())
import google.generativeai as genai
genai.configure(api_key="Enter your api key")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
model = genai.GenerativeModel('gemini-pro')

def get_page_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch page content. Status code: {response.status_code}")
        return None
    

def google_search(query):
    base_url = "https://www.google.com/search"
    params = {"q": query}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
 
        soup = BeautifulSoup(response.text, "html.parser")

        search_results = []
        for result in soup.find_all("div", class_="tF2Cxc"):
            title_element = result.find("h3")
            link_element = result.find("a")

  
            if title_element and link_element and "href" in link_element.attrs:
                title = title_element.get_text()
                link = link_element["href"]
                
                page_content = get_page_content(link)
                if page_content:
                    page_soup = BeautifulSoup(page_content, "html.parser")

                    paragraphs = page_soup.find_all("p")
                    page_text = "\n".join([p.get_text() for p in paragraphs])
                    
                    search_results.append({"title": title, "link": link, "page_text": page_text})
            else:
                print("Skipping result due to missing information.")

        return search_results
    else:
        print(f"Failed to fetch results. Status code: {response.status_code}")
        return None





while True :
    prompt =  input("say : ")
    response = model.generate_content(f""" is the prompt related to realtime data or current affairs or current news?
                                          if yes say yes and if no say no
                                          here to make you clear what might be realtime data  are
                                          if asked about price of something , prime miinister as its keep changing and ongoing events or something 
                                          the prompt : {prompt} """)
    print(response.text)
    
    if response.text == "yes" :
       rep2 = model.generate_content(f"just convert the given prompt to google query that can be used to get desire results from the google search, just a single search query , where the prompt is prompt : ''' {prompt} '''  ")
       print(rep2.text)
       search_query = rep2.text
       results = google_search(search_query)
       all_text = ""
       if results:
          for idx, result in enumerate(results, 1):
              all_text += f"\nResult #{idx}\n"
              all_text += f"Title: {result['title']}\n"
              all_text += f"Link: {result['link']}\n"
              all_text += f"Page Text:\n{result['page_text']}\n\n"
        
       
       with open('mod.txt' ,'w') as f :
                f.write(all_text)           
                f.close()
       rep3 = model.generate_content(f"answer {prompt} according to the text where the text is  :''' {all_text} '''")
       #rep3 = model.generate_content(f"go through the data from the scraped web properly and from the given data answer the prompt ccorrectly , where the data from scraped web is  **** {all_text} **** and the prompt is '{prompt}' ,well but go through the text properly because the answer of the prompt is there , the text there is a google search results and you need to find the answer from the text ")
       print(rep3.text)
    
    else :
       rep2 = model.generate_content(prompt, stream=True)
       for chunk in rep2:
            print(chunk.text)





























    '''
    response = model.generate_content(f"""if i ask you a question about real time data like price of something or current affairs or current news only then convert the prompt to a google search , and if the prompt is not about realtime data or current news or current affairs and you have some info a about the prompt then give your usual results as you give , here  i made  a dailog where im the  user and you are gemini and you are supposed to answer like gemini  given below in the dailouge, you are not supposed to  adapt to the way gemini answer the user query,
                                      

                                      The Dialouge 

                                      user   :  whats the price of bitcoin 
                                      gemini :  price of bitcoin ---query--- $catagory price
                                      user   :  hey whats up?
                                      gemini :  i am good.what about you? 
                                      user   :  whose prime minister of nepal right now?
                                      gemini :  prime minister of nepal ---query--- $catagory current afairs
                                      user   :  humour me 
                                      gemini :  okey boss ! How about a quick joke ? 
                                                Why don't scientists trust atoms?
                                                Because they make up everything!
                                      user   :  give me some tips for imporving my english 
                                      gemini :  Certainly! Improving your English can be a rewarding journey. Here are some tips to help you enhance your English skills:

                                                Read Regularly:

                                                Read a variety of materials, including books, newspapers, articles, and online content. This exposure to different writing styles and vocabulary will broaden your language skills.
                                                Expand Your Vocabulary:

                                                Learn new words every day and try to use them in your conversations and writing. You can use vocabulary-building apps, flashcards, or simply keep a word journal.
                                                Watch English Movies and TV Shows:

                                                Watching movies and TV shows in English is an enjoyable way to improve your listening skills and get accustomed to various accents and colloquial expressions.
                                                Practice Speaking:

                                                Engage in conversations with native speakers or language exchange partners. This will improve your pronunciation, fluency, and overall communication skills.
                                                Use Language Learning Apps:

                                                There are many apps designed to help you learn and practice English. Duolingo, Babbel, and Memrise are popular choices for language learners.
                                                Write Regularly:

                                                Keep a journal, write essays, or start a blog in English. Regular writing practice will enhance your grammar, sentence structure, and overall writing proficiency.
                                                Join Language Learning Communities:

                                                Online forums, social media groups, or local language exchange meetups can provide opportunities to interact with other learners and native speakers.
                                                Listen to Podcasts:

                                                Listening to English podcasts on topics that interest you is a great way to improve your listening skills and expose yourself to diverse accents and vocabulary.
                                                Take Formal English Classes:

                                                If possible, consider enrolling in English language classes. This can provide structured learning, feedback from instructors, and a supportive environment for improvement.
                                                Set Realistic Goals:

                                                Set achievable language learning goals for yourself. This could be mastering a certain number of new words each week or maintaining a conversation for a specific duration without struggling.
                                                Be Patient and Persistent:

                                                Learning a language takes time and effort. Celebrate your progress, no matter how small, and stay motivated.
                                                Remember, consistency is key. Incorporate these tips into your daily routine, and you'll likely see improvement over time. Good luck with your English language journey!
                                      user   :  whats quantum mechanics?
                                      gemini :  A black hole is a region in space where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—can escape from it. The boundary surrounding a black hole is called the event horizon. Once anything crosses this boundary, it is pulled inexorably towards the center of the black hole, a point of infinite density called a singularity.
                                                The concept of black holes comes from the theory of general relativity, proposed by Albert Einstein. Black holes can form when massive stars run out of fuel and collapse under their own gravity. There are also supermassive black holes that exist at the centers of most galaxies, including our Milky Way.
                                                The characteristics of black holes can be fascinating and include time dilation (time passing more slowly near a black hole), extreme gravitational forces, and the possibility of spaghettification—a stretching and elongation of objects as they get closer to the singularity due to the increasing gravitational pull.
                                                Despite their name, black holes are not "holes" in space; rather, they are incredibly dense objects with gravity so intense that nothing can escape once it crosses a certain point. While black holes themselves are invisible, their presence can be inferred by observing the effects they have on nearby matter and light.                 


                                      
                                      Now you are supposed to answer like the way gemini is answering to the user  ,where the prompt is ,
                                      user  : {prompt}  """ , stream=True)
    for chunk in response:
        print(chunk.text)
'''
