import random
import string
from .models import Anketa


class CodeGenerator:
    
    @classmethod
    def generate_codes(cls):
        new_anketa = Anketa.objects.latest('publish_date')
        num_of_codes = new_anketa.broj_kodova
        
        codes = []
        for _ in range(num_of_codes):
            code = ''.join(random.choices(string.digits, k=6))
            codes.append(code)
        return codes

