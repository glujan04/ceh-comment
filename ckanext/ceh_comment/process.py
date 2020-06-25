
from flask import jsonify, Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/publish2/', methods=['POST'])
def publish2():

	context = {'model': model, 'user': c.user}
	#print request.form

	#h.redirect_to(str('/dataset/%s' % c.pkg.name))

	#return render("package/read.html")
	#return jsonify({'data': render_template('package/read.html')}
	#return render_template("package/ceh_comment_list.html", pkg_id=c.pkg.id, pkg_name=c.pkg.name, userobj=c.userobj)
	data = ['Element 1', ' Element 2', 'Element 3']
	return jsonify({'result': True, 'data': False})

if __name__== '__main__':
    app.run(debug=True, port=8080)