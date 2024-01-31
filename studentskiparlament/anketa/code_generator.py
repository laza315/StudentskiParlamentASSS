import random
import string
from .models import Anketa, BackUpKod


class CodeGenerator:
    
    @classmethod
    def generate_codes(cls):
        new_anketa = Anketa.objects.latest('publish_date')
        num_of_codes = new_anketa.broj_kodova
        
        codes = []
        for _ in range(num_of_codes):
            code = ''.join(random.choices(string.digits, k=6))
            codes.append(code)

        cls.secret_codes_saver(codes, new_anketa)

        return codes
    
    @classmethod
    def secret_codes_saver(cls, codes, anketa):
        for code in codes:
            secret_code = BackUpKod(code_value=code, anketa=anketa)
            secret_code.save()
            print(f'Kod {code} za anketu {anketa.id} je napravljen i sacuvan')

