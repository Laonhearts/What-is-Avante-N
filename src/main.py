import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Step 1: 아반떼 N 제원 정보 가져오기
def get_avante_n_specs():
  
    url = 'https://www.hyundai.com/kr/ko/e/vehicles/avante-n/specifications'
  
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 특정 클래스 또는 id를 사용해 필요한 정보를 가져옵니다. 
    # 여기서는 가상의 클래스를 사용했으므로 실제 웹사이트에 맞게 조정이 필요합니다.
    specs_section = soup.find('div', class_='specs-section')
    
    specs = {}
    
    if specs_section:
    
        specs_items = specs_section.find_all('li')
        
        for item in specs_items:
        
            key = item.find('span', class_='spec-key').text.strip()
            
            value = item.find('span', class_='spec-value').text.strip()
            
            specs[key] = value
    
    return specs

# Step 2: 구글에서 아반떼 N 이미지 다운로드
def download_images(query, num_images=5):
  
    options = webdriver.ChromeOptions()
  
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
  
    driver = webdriver.Chrome(options=options)

    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
  
    driver.get(search_url)
  
    time.sleep(2)

    image_urls = set()
  
    thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
    
    for img in thumbnails[:num_images]:
      
        try:
          
            img.click()
          
            time.sleep(2)
          
            images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
          
            for image in images:
              
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                  
                    image_urls.add(image.get_attribute('src'))
                  
        except Exception as e:
          
            print(f"Error: {e}")
          
            continue

    driver.quit()
    
    if not os.path.exists('images'):
      
        os.makedirs('images')

    for i, url in enumerate(image_urls):
      
        image_data = requests.get(url).content
      
        with open(f'images/avante_n_{i+1}.jpg', 'wb') as f:
          
            f.write(image_data)

    print(f"Downloaded {len(image_urls)} images.")

# Main
if __name__ == "__main__":
  
    # 아반떼 N 제원 정보 가져오기
  
    specs = get_avante_n_specs()
  
    for key, value in specs.items():
      
        print(f"{key}: {value}")

    # 구글에서 아반떼 N 이미지 다운로드
    download_images('Avante N car', num_images=5)
