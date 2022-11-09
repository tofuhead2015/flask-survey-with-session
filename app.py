from flask import Flask, request, render_template, flash, redirect, session
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "top secret"

survey = surveys.personality_quiz

@app.route('/')
def show_start():    
    return render_template('start.html', title=survey.title, instructions=survey.instructions)

@app.route('/', methods=['POST'])
def start_survey():
    session['answers'] = []
    return redirect("/questions/0")

@app.route("/questions/<q_id>")
def show_question(q_id): 
    answers = session['answers']   
    id = int(q_id)
    if (len(answers) == len(survey.questions)):
        return render_template('thank_you.html', answers = answers)
    if id == len(answers):
        return render_template('question.html', question = survey.questions[id], question_id = str(id))
    if (id > len(answers)):
        flash("You are trying to access an invalid question!", "error")
        return render_template('question.html', question = survey.questions[len(answers)], 
        question_id = str(len(answers)))

@app.route('/answer', methods=['POST'])
def save_answer_and_show_next():
    answers = session['answers']
    if (len(answers) >= len(survey.questions)):
        return render_template('thank_you.html', answers = answers)
    answers.append(request.form['answer'])
    session['answers'] = answers
    if (len(answers) == len(survey.questions)):
        return redirect("/thankyou")
    return redirect("/questions/" + str(len(answers)))

@app.route("/thankyou")
def show_thank_you():
    answers = session['answers']
    return render_template('thank_you.html', answers = answers)
    
