from Qa import app
from Qa.models import Question, Answer

def listQuestions():
    lq = app.session.query(Question).all()
    app.session.close()
    return lq

def listQuestionDICT():
    ret_list = []
    lq = listQuestions()
    for q in lq:
        quest = q.to_dictionary()
        ret_list.append(quest)
    return ret_list

def listAnswers():
    la = app.session.query(Answer).all()
    app.session.close()
    return la
    
def listAnswerDICT():
    ret_list = []
    la = listAnswers()
    for a in la:
        answ = a.to_dictionary()
        ret_list.append(answ)
    return ret_list

def getAnswer(id):
     a =  app.session.query(Answer).filter(Answer.question_id==id).all()
     app.session.close()
     return a

def getAnswerDICT(id):
    ret_list = []
    la = getAnswer(id)
    for a in la:
        answ = a.to_dictionary()
        ret_list.append(answ)
    return ret_list

def getQuestion(id):
     q =  app.session.query(Question).filter(Question.video_id==id).first()
     app.session.close()
     return q

def getQuestionDICT(id):
    return getQuestion(id).to_dictionary()

def newQuestion(video_id, curr_time, user, text):
    quest =  Question(video_id = video_id, curr_time = curr_time, user = user, text = text)
    try:
        app.session.add(quest)
        app.session.commit()
        print(quest.id)
        app.session.close()
        return quest.id
    except:
        return None

def newAnswer(question_id, a_user, a_text):
    answ = Answer(question_id = question_id, a_user = a_user, a_text = a_text)
    try:
        app.session.add(answ)
        app.session.commit()
        print(answ.id)
        app.session.close()
        return answ.id
    except:
        return None
