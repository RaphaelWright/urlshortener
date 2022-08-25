from flask import Flask, render_template, request, redirect,url_for, flash,abort, session, jsonify 
import json
import os.path


app = Flask(__name__)
app.secret_key = 'raphaelwrightagbedanu'


@app.route('/')
def index():
    return render_template('index.html', codes = session.keys())

@app.route('/yoururl', methods= ['GET','POST'])
def your_url(): 
    if request.method == 'POST': 
        urls = {}
        #checking if the json file exist in the computer's directory
        #if it exists we just 'load' it 
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)


        #if the code is in the json file already, redirect to home page
        if request.form['code'] in urls.keys():
            flash('The short name has been already been taken. Please use another name')
            return redirect(url_for('index'))


        #this is to append the code and the url to a json file
        urls[request.form['code']] = {'url':request.form['url']}  
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file) 
            session[request.form['code']] = True
        return render_template('your_url.html', code = request.form['code'] )


    else:
        return redirect(url_for('index'))

@app.route( '/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

                #if the code is in the json file already, redirect to home page
                if code in urls.keys():
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]['url'])

#handle 404 error message
@app.errorhandler(500)
def page_not_found(error):
    return render_template('page_not_found.html'),500

@app.route('/api')
def session_api():
    return  jsonify(list(session.keys()))
