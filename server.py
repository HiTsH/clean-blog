from flask import Flask, render_template, request
import requests
import smtplib

my_email = 'hisham007_007@hotmail.com'
app_pass = 'app_password'

posts_data = requests.get('https://api.npoint.io/f56ac310cba827a3a8eb').json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template('index.html', all_posts=posts_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for post in posts_data:
        if post['id'] == index:
            requested_post = post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    msg_sent = False
    if request.method == "POST":
        data = request.form
        name = data["username"]
        email = data["email"]
        phone = data["phone"]
        user_message = data["message"]
        msg_sent = True
        send_email(name, email, phone, user_message)

    return render_template("contact.html", msg_sent=msg_sent)


def send_email(name, email, phone, message):
    with smtplib.SMTP('smtp-mail.outlook.com') as connection:
        connection.starttls()
        connection.login(user=my_email, password=app_pass)
        connection.sendmail(
            from_addr=my_email,
            to_addrs='hisham007_007@hotmail.com',
            msg=f"Subject:New Form Submitted\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
        )


if __name__ == '__main__':
    app.run(debug=True)
    