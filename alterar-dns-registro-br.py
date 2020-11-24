# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from time import sleep # sleep(1)
import csv

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver  = webdriver.Chrome(executable_path=r'../alterar-dns-registro-br/driver/chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):      
        driver = self.driver
        driver.get("https://registro.br/login/?session=logout")

        #Login
        id = input("Informe a ID do Registro BR: ")
        senha = input("Informe a SENHA do Registro BR: ")

        sleep(5)
        driver.find_element_by_name("login.user").click()
        driver.find_element_by_name("login.user").click()
        driver.find_element_by_name("login.user").clear()
        driver.find_element_by_name("login.user").send_keys(id)
        driver.find_element_by_id("app").click()
        driver.find_element_by_name("login.password").click()
        driver.find_element_by_name("login.password").clear()
        driver.find_element_by_name("login.password").send_keys(senha)   

        print("Faça o CAPTCHA do Google na aba do navegador que irá abrir !!")     
        
        #Pagina inicial
        input('Aperte Enter Quando Terminar de Acessar !!')
        

        #Configurações        
        dns1 = input("Informe o primeiro DNS: ")
        dns2 = input("Informe o segundo DNS: ")       

        menu = ['dominio']
        dominios = {}
        with open('dominios.csv','r',encoding='utf-8') as dados:
            leitor = csv.reader(dados)
            for line in leitor:
                if 'dominio' in line[0]: pass
                else: dominios[line[0]] = dict(zip(menu,line))

        for dominio in dominios.values():            
            try:          
                try:
                    driver.get("https://registro.br/painel/")
                    dominio = dominio['dominio']
                    sleep(3)
                    driver.find_element_by_xpath("//input[@type='search']").click()
                    driver.find_element_by_xpath("//input[@type='search']").clear()
                    driver.find_element_by_xpath("//input[@type='search']").send_keys(dominio)
                    sleep(3)
                    driver.find_element_by_link_text(dominio.upper()).click()                
                except:           
                    print("Domínio: ",dominio," não encontrado!")
                    continue
                
                #Clicar em "Alterar Servidores DNS"        
                try:
                    sleep(3) 
                    driver.find_element_by_xpath("/html/body/div/main/div[2]/div/section[4]/div/a").click()

                except:
                    print("Não possui o botão 'Alterar Servidores DNS'")
                    continue  
                
                #Informar o DNS
                sleep(2)
                driver.find_element_by_xpath("//div[@id='app']/main/div[2]/div/section[4]/div/div").click()
                driver.find_element_by_name("dns.host0").click()
                driver.find_element_by_name("dns.host0").clear()
                driver.find_element_by_name("dns.host0").send_keys(dns1)

                sleep(2)
                driver.find_element_by_xpath("//div[@id='app']/main/div[2]/div/section[4]/div/div").click()
                driver.find_element_by_name("dns.host1").click()
                driver.find_element_by_name("dns.host1").clear()
                driver.find_element_by_name("dns.host1").send_keys(dns2)
                driver.find_element_by_xpath("//button[@type='button']").click()
                sleep(5)
                print("DNS DO DOMÍNIO: ",dominio," ALTERADO COM SUCESSO")  
            except:
                print("ERRO AO ALTERAR DNS DO DOMÍNIO: ",dominio)
                continue 
            
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
