from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from datetime import datetime
import time
import json
from typing import Optional

class HanKyungScraper:
    def __init__(self, start_date: str, end_date: str, output_json: str) -> None:
        self.start_date = datetime.strptime(start_date, "%Y%m%d")
        self.end_date = datetime.strptime(end_date, "%Y%m%d")
        self.output_json = output_json
        self.url = 'https://www.hankyung.com/all-news'
        self.options = Options()
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def scrape(self) -> None:
        articles_data = []

        try:
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]/header/div/div[3]/nav/ul/li[3]/a'))).click()

            while True:
                load_more_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[1]/div[2]/div[3]/div/div/div[3]/div[4]/button')))
                load_more_button.click()

                economy_section = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.box-module-inner.economyDiv.slick-current.slick-active')))
                day_elements = economy_section.find_elements(By.CSS_SELECTOR, '.day-wrap')
                last_date_str = day_elements[-1].find_element(By.CSS_SELECTOR, '.txt-date').text
                last_date = datetime.strptime(last_date_str, "%Y.%m.%d")

                if last_date < self.start_date:
                    break

            economy_section = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.box-module-inner.economyDiv.slick-current.slick-active')))
            day_elements = economy_section.find_elements(By.CSS_SELECTOR, '.day-wrap')

            all_article_links: list[str] = []
            for day_element in day_elements:
                articles = day_element.find_elements(By.CSS_SELECTOR, '.news-list > li')

                for article in articles:
                    title_element = article.find_element(By.CSS_SELECTOR, 'h3.news-tit > a')
                    link = title_element.get_attribute('href')
                    all_article_links.append(str(link))

            for link in all_article_links:
                self.driver.get(link)
                article_html = self.driver.page_source
                article_soup = BeautifulSoup(article_html, 'html.parser')

                title_tag = article_soup.find('title')
                title = title_tag.get_text() if title_tag else ""

                date_tags = article_soup.find_all('span', class_='txt-date')
                date_str = date_tags[0].text.strip() if len(date_tags) > 0 else ""
                edit_date_str = date_tags[1].text.strip() if len(date_tags) > 1 else ""

                article_content_tag = article_soup.find('div', {'class': 'article-body'})
                article_content = article_content_tag.get_text(separator='\n', strip=True) if article_content_tag else ""

                article_data = {
                    'date': date_str,
                    'date_edit': edit_date_str,
                    'href': link,
                    'title': title,
                    'article': article_content
                }

                articles_data.append(article_data)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            with open(self.output_json, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, ensure_ascii=False, indent=4)
            self.driver.quit()
