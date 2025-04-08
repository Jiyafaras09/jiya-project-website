from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

# Define Questions
questions = [
    {"question": "How often do you exercise in a week?", "options": ["Never", "1-2 times", "3-4 times", "5+ times"]},
    {"question": "How connected do you feel with family/friends?", "options": ["Not at all", "Somewhat", "Moderately", "Very Connected"]},
    {"question": "How many hours of sleep do you get on average per night?", "options": ["Less than 5", "5-6", "7-8", "More than 8"]},
    {"question": "How much water do you drink daily?", "options": ["Less than 1L", "1-2L", "2-3L", "More than 3L"]},
    {"question": "How often do you take breaks while working/studying?", "options": ["Less than 1", "1-3", "4-6", "More than 6"]},
    {"question": "How satisfied are you with your work-life balance?", "options": ["Very Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"]},
    {"question": "How often do you experience stress?", "options": ["Rarely", "Sometimes", "Frequently", "Constantly"]},
    {"question": "How much time do you spend on social media daily?", "options": ["Less than 30 min", "30 min-1 hr", "1-2 hrs", "More than 2 hrs"]},
    {"question": "How often do you visit a doctor for a mental health check-up?", "options": ["Never", "Once a year", "More than once a year"]},
    {"question": "Do you follow a proper sleep schedule?", "options": ["No", "Sometimes", "Yes", "Strictly"]}
]

# Enhanced Scoring System
scoring = {
    "Never": 1, "1-2 times": 2, "3-4 times": 3, "5+ times": 4,
    "Not at all": 1, "Somewhat": 2, "Moderately": 3, "Very Connected": 4,
    "Less than 5": 1, "5-6": 2, "7-8": 4, "More than 8": 3,
    "Less than 1L": 1, "1-2L": 2, "2-3L": 3, "More than 3L": 4,
    "Less than 1": 1, "1-3": 3, "4-6": 4, "More than 6": 2,
    "Very Dissatisfied": 1, "Neutral": 2, "Satisfied": 3, "Very Satisfied": 4,
    "Rarely": 4, "Sometimes": 3, "Frequently": 2, "Constantly": 1,
    "Less than 30 min": 4, "30 min-1 hr": 3, "1-2 hrs": 2, "More than 2 hrs": 1,
    "Never": 1, "Once a year": 3, "More than once a year": 4,
    "No": 1, "Sometimes": 2, "Yes": 3, "Strictly": 4
}

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "current_question" not in session:
        session["current_question"] = 0
        session["answers"] = []

    if request.method == "POST":
        selected_answer = request.form.get("answer")
        if selected_answer:
            session["answers"].append(selected_answer)
            session["current_question"] += 1
            session.modified = True

        if session["current_question"] >= len(questions):
            return redirect(url_for("result"))

    question_index = min(session["current_question"], len(questions) - 1)
    try:
        return render_template('quiz.html', 
                               question=questions[question_index],
                               questions=questions)
    except Exception as e:
        return f"Error rendering quiz: {str(e)}", 500

@app.route("/result")
def result():
    try:
        user_answers = session.get("answers", [])
        if not user_answers:
            return redirect(url_for("home"))

        # Calculate total score and log each answer's contribution
        total_score = 0
        for answer in user_answers:
            score = scoring.get(answer, 0)
            total_score += score
            print(f"Answer: {answer}, Score: {score}")  # Debugging output to console

        max_possible_score = len(questions) * 4  # 10 questions * 4 = 40
        percentage = min((total_score / max_possible_score) * 100, 100)
        print(f"Total Score: {total_score}, Percentage: {percentage}%")  # Debugging output

        # Adjusted thresholds to better reflect poor well-being
        if percentage < 40:  # Adjusted from 33 to 40
            wellbeing_status = "Poor"
            notes = "It's important to focus on improving your well-being. Consider lifestyle changes and seek support."
            youtube_links = [
                {"title": "Kati Morton - Mental Health Tips", "link": "https://www.youtube.com/user/KatiMorton", "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_lxV4fQ9zDHN3Y4k53mc4tH-AeN-6Y7fBHb2eL6=s88-c-k-c0x00ffffff-no-rj"},
                {"title": "Therapy in a Nutshell - Coping Strategies", "link": "https://www.youtube.com/c/TherapyinaNutshell", "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_nV2fjsEYa5RuX5z3cHrdim8wA8aOWuHHaWgeAj=s88-c-k-c0x00ffffff-no-rj"}
            ]
        elif percentage < 70:  # Adjusted from 66 to 70
            wellbeing_status = "Average"
            notes = "You're doing okay, but there's room for improvement. Try incorporating healthier habits."
            youtube_links = [
                {"title": "Psych2Go - Understanding Emotions", "link": "https://www.youtube.com/channel/UCkJEpR7JmS36tajD34Gp4VA", "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_kP8bH0goVv8voxKzQUq0NX8y0e-bA2F0VRW97v=s88-c-k-c0x00ffffff-no-rj"},
                {"title": "Psych Hub - Mental Health Education", "link": "https://www.youtube.com/c/PsychHub", "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_nh8rM0Y0F2WkgTd7JMMzN64i4WOK8v0QVoD_6T=s88-c-k-c0x00ffffff-no-rj"}
            ]
        else:
            wellbeing_status = "Excellent"
            notes = "Excellent! You have a strong foundation for well-being. Keep up the good work."
            youtube_links = [
                {"title": "How to ADHD - Self-Improvement", "link": "https://www.youtube.com/c/HowtoADHD", "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_mgK8Q0R0yrnO7VDLGCg7eY8K8uQCUkV0yV3zQ=s88-c-k-c0x00ffffff-no-rj"},
                {"title": "TEDx - Nutrition & Mental Health", "link": "https://www.youtube.com/watch?v=3dqXHHCc5lA", "thumbnail": "https://i.ytimg.com/vi/3dqXHHCc5lA/mqdefault.jpg"}
            ]

        return render_template('result.html', 
                               answers=user_answers, 
                               wellbeing_status=wellbeing_status, 
                               notes=notes, 
                               youtube_links=youtube_links,
                               score=percentage)
    except Exception as e:
        return f"Error calculating result: {str(e)}", 500