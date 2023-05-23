from flask import render_template, redirect, session, flash
from app import app
from app.forms import SearchForm
from app.forms import SubmitFeedbackForm
import ethos_search
import ethos_search.get_results
import nlp_search
import nlp_search.query_process
from pymongo import MongoClient


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        user_query = form.search_query.data
        session["user_search"] = user_query
        session["number of results"] = form.number_of_results.data
        # print(form.number_of_results.data)
        return redirect("/result")

    return render_template("index.html", title="Smart Ethos search", form=form)


@app.route("/result", methods=["GET", "POST"])
def result():
    user_query = session.get("user_search", None)
    number_of_results = int(session.get("number of results", None))
    # query = "ultrasound dislocation"
    ethos_result, total_replies = ethos_search.get_results.main_app(user_query)
    # print(ethos_result)
    nlp_response_ids, nlp_result = nlp_search.query_process.query_response(
        user_query, number_of_replies=number_of_results
    )
    # print(nlp_response_ids, nlp_result)
    # *************insert your MongoDB credentials here*****************
    client = MongoClient(
        "*******"
    )
    # *************insert your MongoDB credentials here*****************
    db = client.user_data
    form = SubmitFeedbackForm()
    if form.validate_on_submit():
        user_comments = form.user_feedback.data
        user_score = form.user_score.data
        response_data = {
            "User search": user_query,
            "Ethos response": ethos_result,
            "Total Ethos replies": total_replies,
            "Semantic Search result": nlp_result,
            "User comments": user_comments,
            "Response score": user_score,
        }
        db.entries.insert_one(response_data)
        flash(
            "Thank you for your feedback! It will help to improve this tool!"
        )
        return redirect("/index")

    return render_template(
        "result.html",
        user_query=user_query,
        ethos_result=ethos_result,
        total_replies=total_replies,
        nlp_result=nlp_result,
        form=form,
        title="Search results",
    )
