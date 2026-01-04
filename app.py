import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import json

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect("quote50.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
# cur.execute()
# conn.commit()
# cur.close()

def transform_timestamp(quotes):

    updatedQuotes = []

    for quote in quotes:
        quoteDict = dict(quote)
        converted = datetime.strptime(quoteDict["timestamp"], "%Y-%m-%d %H:%M:%S")
        quoteDict["timestamp"] = converted.strftime("%d %b, %Y")

        updatedQuotes.append(quoteDict)

    return updatedQuotes

@app.route("/", methods=["GET"])
def index():

    if not "loggedIn" in session:
        return redirect("/login")

    currentUser = cur.execute("SELECT * FROM users WHERE id = ?", [session["loggedIn"]]).fetchone()    
    quotes = cur.execute("SELECT * FROM quotes JOIN users ON quotes.user = users.id ORDER BY quotes.id DESC")

    transformedQuotes = transform_timestamp(quotes)

    return render_template("index.html", user=currentUser, quotes=transformedQuotes)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", error="Invalid username")
        if not request.form.get("password"):
            return render_template("error.html", error="Invalid password")
        
        searchUser = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        if len(searchUser) != 1:
            return render_template("error.html", error="Incorrect username")
        if not check_password_hash(searchUser[0]["hash"], request.form.get("password")):
            return render_template("error.html", error="Incorrect password")
        
        session["loggedIn"] = searchUser[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", error="Invalid username")
        if ' ' in request.form.get("username"):
            return render_template("error.html", error="Username cannot have spaces")
        if not request.form.get("password"):
            return render_template("error.html", error="Invalid password")
        if not request.form.get("passwordConfirmation"):
            return render_template("error.html", error="Invalid password confirmation")
        if not request.form.get("password") == request.form.get("passwordConfirmation"):
            return render_template("error.html", error="Passwords don't match")
        
        searchUser = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        if len(searchUser) != 0:
            return render_template("error.html", error="Username already exists")
        
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"))))
        conn.commit()

        session["loggedIn"] = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()[0]["id"]
        
        return redirect("/")
    
    else:
        return render_template("register.html")


@app.route("/profile/<userId>", methods=["GET", "POST"])
def profile(userId):

    if not "loggedIn" in session:
        return redirect("/login")

    userProfile = cur.execute("SELECT * FROM users WHERE id = ?", [userId]).fetchone()
    userQuotes = cur.execute("WITH  requoted_quotes AS (SELECT q.*, u2.username AS username, u2.id AS user_id, u.username AS requoter_username, json_extract(json_each.value, '$.timestamp') AS action_timestamp FROM users u JOIN json_each(u.requotes) JOIN quotes q ON q.id = json_extract(json_each.value, '$.quoteId') JOIN users u2 ON q.user = u2.id WHERE u.id = :user_id), user_quotes AS (SELECT q.*, u.username AS username, NULL AS user_id, NULL AS requoter_username, q.timestamp AS action_timestamp FROM quotes q JOIN users u ON q.user = u.id WHERE q.user = :user_id AND q.id NOT IN (SELECT json_extract(json_each.value, '$.quoteId') FROM users u JOIN json_each(u.requotes) WHERE u.id = :user_id)) SELECT * FROM user_quotes UNION ALL SELECT * FROM requoted_quotes ORDER BY action_timestamp DESC", [userId]).fetchall()

    transformedQuotes = transform_timestamp(userQuotes)

    if userProfile == None:
        return render_template("error.html", error="User not found")

    return render_template("profile.html", user=userProfile, quotes=transformedQuotes)


@app.route("/profile", methods=["GET"])
def profileDir():

    if "loggedIn" in session:
        return redirect(f"/profile/{session["loggedIn"]}")
    
    return redirect("/login")


@app.route("/quote", methods=["POST"])
def quote():

    SOURCES = ['the book', 'the movie', 'the tv series', 'myself', 'the person', 'the song']

    if request.method == "POST":
        if not request.form.get("quote") or len(request.form.get("quote")) > 100:
            return render_template("error.html", error="Invalid quote")
        if not request.form.get("source") in SOURCES:
            return render_template("error.html", error="Invalid source")
        if request.form.get("source") != "myself" and not request.form.get("sourceName"):
            return render_template("error.html", error="Invalid source name")
        
        if request.form.get("source") == "the person":
            quoteSource = ""
            quoteName = request.form.get("sourceName")
        elif request.form.get("source") == "myself":
            quoteSource = request.form.get("source")
            quoteName = ""
        else:
            quoteSource = request.form.get("source")
            quoteName = request.form.get("sourceName")
        
        cur.execute("INSERT INTO quotes (text, source, user, name) VALUES (?, ?, ?, ?)", (request.form.get("quote"), quoteSource, session["loggedIn"], quoteName))
        conn.commit()

    return redirect("/")


@app.route("/like", methods=["POST"])
def like():

    likedQuoteId = request.get_json()["quoteId"]
    likesJson = cur.execute("SELECT likes FROM users WHERE id = ?", (session["loggedIn"],)).fetchone()[0]

    likes = json.loads(likesJson)
    hasLiked = any(like["quoteId"] == likedQuoteId for like in likes)

    if not hasLiked:
        cur.execute("UPDATE users SET likes = json_set(likes, '$[#]', json_object('quoteId', ?, 'timestamp', CURRENT_TIMESTAMP)) WHERE id = ?", (likedQuoteId, session["loggedIn"]))
        cur.execute("UPDATE quotes SET likes = likes + 1 WHERE id = ?", (likedQuoteId,))
    else:
        likes = [like for like in likes if like['quoteId'] != likedQuoteId]
        cur.execute("UPDATE users SET likes = ? WHERE id = ?", (json.dumps(likes), session["loggedIn"]))
        cur.execute("UPDATE quotes SET likes = likes - 1 WHERE id = ?", (likedQuoteId,))
        
    conn.commit()
    updatedLikes = cur.execute("SELECT likes FROM quotes WHERE id = ?", (likedQuoteId,)).fetchone()[0]
    return jsonify({"likes":updatedLikes})


@app.route("/requote", methods=["POST"])
def requote():

    requotedQuoteId = request.get_json()["quoteId"]
    requotesJson = cur.execute("SELECT requotes FROM users WHERE id = ?", (session["loggedIn"],)).fetchone()[0]

    requotes = json.loads(requotesJson)
    hasRequoted = any(requote["quoteId"] == requotedQuoteId for requote in requotes)
    
    if not hasRequoted:
        cur.execute("UPDATE users SET requotes = json_set(requotes, '$[#]', json_object('quoteId', ?, 'timestamp', CURRENT_TIMESTAMP)) WHERE id = ?", (requotedQuoteId, session["loggedIn"]))
        cur.execute("UPDATE quotes SET requotes = requotes + 1 WHERE id = ?", (requotedQuoteId,))
    else:
        requotes = [requote for requote in requotes if requote['quoteId'] != requotedQuoteId]
        cur.execute("UPDATE users SET requotes = ? WHERE id = ?", (json.dumps(requotes), session["loggedIn"]))
        cur.execute("UPDATE quotes SET requotes = requotes - 1 WHERE id = ?", (requotedQuoteId,))
        
    conn.commit()
    updatedRequotes = cur.execute("SELECT requotes FROM quotes WHERE id = ?", (requotedQuoteId)).fetchone()[0]
    return jsonify({"requotes":updatedRequotes})


@app.route("/search", methods=["GET"])
def search():

    if not "loggedIn" in session:
        return redirect("/login")

    searchInput = request.args.get("search") 
    if not searchInput:
        return render_template("error.html", error="Invalid search input")
    
    users = cur.execute("SELECT * FROM users WHERE username LIKE ?", ('%' + searchInput + '%',)).fetchall()
    quotes = cur.execute("SELECT * FROM quotes JOIN users ON quotes.user = users.id WHERE text LIKE ? ORDER BY quotes.id", ('%' + searchInput + '%',)).fetchall()
    names = cur.execute("SELECT * FROM quotes JOIN users ON quotes.user = users.id WHERE name LIKE ? ORDER BY quotes.id", ('%' + searchInput + '%',)).fetchall()

    transformedQuotes = transform_timestamp(quotes)
    transformedNames = transform_timestamp(names)

    return render_template("search.html", users=users, quotes=transformedQuotes, names=transformedNames)


@app.route("/user-likes-requotes", methods=["GET"])
def userLikesRequotes():

    if not "loggedIn" in session:
        return redirect("/login")
    
    userJson = cur.execute("SELECT likes, requotes FROM users WHERE id = ?", (session["loggedIn"],)).fetchone()
    if userJson:
        userLikes = json.loads(userJson[0])
        userRequotes = json.loads(userJson[1])

        likedQuoteIds = [like["quoteId"] for like in userLikes]
        requotedQuoteIds = [requote["quoteId"] for requote in userRequotes]

        return jsonify({"likedQuoteIds": likedQuoteIds, "requotedQuoteIds": requotedQuoteIds})
    
    return redirect("/index")


@app.route("/profile/<userId>/likes", methods=["POST"])
def userLoadLikes(userId):

    user = cur.execute("SELECT * FROM users WHERE id = ?", [userId]).fetchone()
    quotes = cur.execute("WITH liked_quotes AS (SELECT q.*, u.username AS liked_by_username, json_extract(json_each.value, '$.timestamp') AS action_timestamp, u2.username AS username FROM users u JOIN json_each(u.likes) JOIN quotes q ON q.id = json_extract(json_each.value, '$.quoteId') JOIN users u2 ON q.user = u2.id WHERE u.id = :user_id), requoted_quotes AS (SELECT q.*, u.username AS requoter_username, json_extract(json_each.value, '$.timestamp') AS action_timestamp, u2.username AS username FROM users u JOIN json_each(u.requotes) JOIN quotes q ON q.id = json_extract(json_each.value, '$.quoteId') JOIN users u2 ON q.user = u2.id WHERE u.id = :user_id) SELECT l.*, r.requoter_username FROM liked_quotes l LEFT JOIN requoted_quotes r ON l.id = r.id ORDER BY action_timestamp DESC", [userId]).fetchall()

    transformedQuotes = transform_timestamp(quotes)

    return render_template("profile.html", quotes=transformedQuotes, user=user)