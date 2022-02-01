from maths_question_generator import basic_arithmetic

def generate_questions(question_count, sub_topics):

    add = True if 'Addition' in sub_topics else False
    sub = True if 'Subtraction' in sub_topics else False
    mul = True if 'Multiplication' in sub_topics else False
    div = True if 'Division' in sub_topics else False
    
    questions = []
    while len(questions) < question_count:
        q_and_a = basic_arithmetic(
            add=add,
            sub=sub,
            mul=mul,
            div=div,
            min_res=0,
            max_res=1000
        )
        questions.append(q_and_a)

    return questions