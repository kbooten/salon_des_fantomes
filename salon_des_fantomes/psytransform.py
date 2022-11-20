import random,time,re

def transform_text(text,transformation,probability_of_transformation,max=3):
    c = 0
    while probability_of_transformation>0 and c<max:
        probability_of_transformation-=1.0
        if random.random()>probability_of_transformation:
            text = transformation(text)
        c+=1
        print('transforming')
        time.sleep(.5)
        print(text)
    return text

# def apply_all_transformations(text,transformation_probability_tuples):
#     for transformation,probability_of_transformation in transformation_probability_tuples:
#         text = _transform_text(text,transformation,probability_of_transformation)
#     return text

def main():
    from psychotropics.odd_parenthetical import add_odd_parenthetical
    test_text = "This is just a test text. I'm just trying to see if this function works."
    #transformation_probability_tuples = [(add_odd_parenthetical,2.3)]
    text = transform_text(test_text,add_odd_parenthetical,1.0) 
    print(text)

if __name__ == '__main__':
  main()