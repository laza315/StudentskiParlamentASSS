from .models import Anketa  


def query_anketa():
    # Retrieve the first 5 Anketa objects using Django ORM
    anketa_objects = Anketa.objects.all()[:5]

    # Convert queryset to list of dictionaries
    result = [obj.__dict__ for obj in anketa_objects]

    # Print and return the result
    print(result)
    return result

if __name__ == '__main__':
    query_anketa()

