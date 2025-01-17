import requests
from bs4 import BeautifulSoup
import logging


class BrokenAuthentification:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.discovered_endpoints = []

    def brut_force_usual(self):
        usual_passwords = ["123456", "password", "12345678", "qwerty", "abc123", "111111", "123123", "letmein", "monkey", "1234567", "1q2w3e4r",
                                     "qwertyuiop", "password1", "admin", "welcome", "1234", "iloveyou", "sunshine", "football", "princess", "admin123"]
        
        

 