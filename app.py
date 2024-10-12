from flask import Flask, render_template, request, redirect, url_for, session, g
from github import Auth
from github import Github
from ai_summarizer import ai_pullrequest_summarizer

def get_git_inst():
    if 'token' in session:
        if not hasattr(g, 'github'):
            auth = Auth.Token(session['token'])
            g.github = Github(auth=auth)
            g.github.get_user().login
        return g.github
    return None

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        token = request.form['github_token']
        session['token'] = token
        return redirect(url_for('repos'))
    return render_template('index.html')

@app.route('/repos')
def repos():
    user = get_git_inst()
    repos = user.get_user().get_repos()

    repos_with_pulls = []
    for repo in repos:
        pulls = repo.get_pulls(state='open') 
        if pulls.totalCount > 0:  
            repos_with_pulls.append({'repo': repo, 'pulls': pulls})

    return render_template('repos.html', repos_with_pulls=repos_with_pulls)

@app.route('/summary/<title>/<body>')
def summarize(title, body):
    summary = ai_pullrequest_summarizer(title, body)
    return render_template('summary.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
