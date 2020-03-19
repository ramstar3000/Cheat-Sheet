import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
    def Login(self,User="Ram",Pass="Ram"):#swap xxxx for a username and password
        driver = self.driver
        driver.get("https://cheat-sheet-maker.herokuapp.com/")
        elem = driver.find_element_by_name("name")
        elem.send_keys(User)
        elem = driver.find_element_by_name("password")
        elem.send_keys(Pass)
        elem.send_keys(Keys.RETURN)
        return(driver)

    def test_login_successful(self):
        driver = self.Login()
        event = EC.presence_of_element_located((By.ID, "Name"))
        WebDriverWait(self.driver,15).until((event))
        assert "Card Maker" in driver.page_source
    
    def test_login_wrong(self):
        driver = self.Login("Ram","Pam")
        event = EC.presence_of_element_located((By.ID, "Error"))
        WebDriverWait(self.driver,15).until(((event)))
        assert "Wrong username or password" in driver.page_source
    
    ##def test_login_Blank(self):
    
        #driver = self.Login("Ram","")
        #event = EC.(("An error has occured"))
        #WebDriverWait(self.driver,15).until(((event)))
        #assert "Wrong username or password" in driver.page_source
    

    def test_create(self):
        driver = self.Login()

        event = EC.presence_of_element_located((By.ID, "Name"))
        WebDriverWait(self.driver,15).until(event)
        assert "Card Maker" in driver.page_source
        elem = driver.find_element_by_id("Name")
        elem.send_keys("Example")

        elem = driver.find_element_by_id("txt_comments")
        elem.send_keys("Example Program 1")

        elem = driver.find_element_by_id("Button")
        elem.click()
        
        event = EC.presence_of_element_located((By.ID, "Sent"))
        WebDriverWait(self.driver,15).until(((event)))
	
    def test_make_sheet(self):
        driver = self.Login()
        event = EC.presence_of_element_located((By.ID, "Name"))
        
        WebDriverWait(self.driver,15).until(event)
        elem = driver.find_element_by_id("View")
        elem.click()

        event = EC.presence_of_element_located((By.NAME, "Search"))
        WebDriverWait(self.driver,15).until(event)
        
        
        elem = driver.find_element_by_name("RamiscoolPrinting")
        elem.click()
        elem = driver.find_element_by_name("PrajwalHello test")
        elem.click()
        elem = driver.find_element_by_name("RamExample")
        elem.click()
        #Select some bullet points
        
        #then press make sheet
        elem = driver.find_element_by_id("Submit")
        elem.click()
        
        event = EC.presence_of_element_located((By.NAME, "Save"))
        WebDriverWait(self.driver,15).until(event)
        
        elem = driver.find_element_by_name("Save")
        elem.send_keys("Example")
        #Some problems
        elem = driver.find_element_by_id("Submit")
        elem.click()
        
        event = EC.presence_of_element_located((By.ID, "Name"))
        WebDriverWait(self.driver,15).until(event)
        
        assert "Card Maker" in driver.page_source
        
        
	
    def test_create_card(self):
        driver = self.Login()
        event = EC.presence_of_element_located((By.ID, "Name"))
        
        WebDriverWait(self.driver,15).until(event)
        elem = driver.find_element_by_id("View")
        elem.click()

        event = EC.presence_of_element_located((By.NAME, "Search"))
        WebDriverWait(self.driver,15).until(event)
        
        elem = driver.find_element_by_id("How")
        elem.click()
        
        event = EC.presence_of_element_located((By.ID, "Edit"))
        WebDriverWait(self.driver,15).until(event)
        
        assert "Ramiscool" in driver.page_source


	
    def test_print_card(self):
        driver = self.Login()
        event = EC.presence_of_element_located((By.ID, "Name"))
        
        WebDriverWait(self.driver,15).until(event)
        elem = driver.find_element_by_id("Pre")
        elem.click()
	    
        event = EC.presence_of_element_located((By.ID, "Search"))
        WebDriverWait(self.driver,15).until(event)
        #Unblank rejected#
        elem = driver.find_element_by_id("List_Func")
        elem.click()
        
        event = EC.presence_of_element_located((By.ID, "Print"))
        WebDriverWait(self.driver,15).until(event)
        
        assert "Creating" in driver.page_source

        elem = driver.find_element_by_id("Print")
        elem.click()

        event = EC.presence_of_element_located((By.ID, "PRint"))
        WebDriverWait(self.driver,15).until(event)

        elem = driver.find_element_by_id("PRint")
        elem.click()

    def test_zdelete_card(self):
        driver = self.Login()
        event = EC.presence_of_element_located((By.ID, "Name"))
        
        WebDriverWait(self.driver,15).until(event)
        elem = driver.find_element_by_id("View")
        elem.click()

        event = EC.presence_of_element_located((By.ID, "Example"))
        WebDriverWait(self.driver,15).until(event)

        elem = driver.find_element_by_id("Example")
        elem.click()

        event = EC.presence_of_element_located((By.ID, "Edit"))
        WebDriverWait(self.driver,15).until(event)

        elem = driver.find_element_by_id("Edit")
        elem.click()

        event = EC.presence_of_element_located((By.ID, "Del"))
        WebDriverWait(self.driver,15).until(event)

        elem = driver.find_element_by_id("Del")
        elem.click()
    


        
    def test_search_bar(self):
        driver = self.Login()
        event = EC.presence_of_element_located((By.ID, "Name"))

        WebDriverWait(self.driver,15).until(event)
        elem = driver.find_element_by_id("View")
        elem.click()

        elem = driver.find_element_by_id("Search")
        elem.clear()
        elem.send_keys("Printing")

        elem.send_keys(Keys.RETURN)

        sleep(7)

        assert ("Hello Test" not in driver.page_source)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
