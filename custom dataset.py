from time import sleep

import wget
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def myntra_image_scrapp(DRIVER_PATH=None,
                        LABEL=None,
                        MAX_NO_PAGES=None,
                        Start=None,
                        OUTPUT_LOCATION=None):

    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get("https://www.myntra.com/")
    search_bar = driver.find_element_by_class_name("desktop-searchBar")
    search_bar.send_keys(LABEL)
    search_bar.send_keys(Keys.ENTER)
    if not Start is None:
        for _ in range(Start):
            next_btn = driver.find_elements_by_css_selector(
                "#desktopSearchResults > div.search-searchProductsContainer.row-base > section > div.results-showMoreContainer > ul > li.pagination-next > a")
            if next_btn == None:
                break
            else:
                next_btn[0].send_keys(Keys.ENTER)


    max_no_of_pages = MAX_NO_PAGES
    for p in range(Start,max_no_of_pages):
        print()
        no_product_boxs = driver.find_elements_by_class_name("product-base")
        print(f"page : {p + 1} - products : {len(no_product_boxs)}")
        for i in range(1, len(no_product_boxs) + 1):
            selector = f"#desktopSearchResults > div.search-searchProductsContainer.row-base > section > ul > li:nth-child({i}) > a"
            image_url = driver.find_element_by_css_selector(selector).get_attribute("href")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(image_url)
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            sleep(2)
            imageboxes = driver.find_elements_by_class_name("image-grid-image")

            for imagebox in imageboxes:
                try:
                    image_url = imagebox.value_of_css_property("background-image").split('"')[1]
                    wget.download(image_url, OUTPUT_LOCATION)
                except:
                    pass
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        next_btn=driver.find_elements_by_css_selector(
            "#desktopSearchResults > div.search-searchProductsContainer.row-base > section > div.results-showMoreContainer > ul > li.pagination-next > a")
        if next_btn==None:
            break
        else:
            next_btn[0].send_keys(Keys.ENTER)
        sleep(5)
    driver.quit()


if __name__ == "__main__":
    DRIVER_PATH = "chromedriver.exe"
    LABEL = ["hoodie","Blouse"]
    MAX_NO_PAGES = 15
    for label in LABEL:

        OUTPUT_LOCATION = f"myntra_images/{label}"

        myntra_image_scrapp(DRIVER_PATH,label,MAX_NO_PAGES,5,OUTPUT_LOCATION)
