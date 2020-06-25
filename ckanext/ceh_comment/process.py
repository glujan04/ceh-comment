from flask import Blueprint, jsonify, Flask, render_template, request

@foo.route('/')
def index():
    return 'hello world!'

@foo.route('/publish2', endpoint='publish_2')
def publish_2():

    context = {'model': model, 'user': c.user}
    #print request.form

    #h.redirect_to(str('/dataset/%s' % c.pkg.name))

    #return render("package/read.html")
    #return jsonify({'data': render_template('package/read.html')}
    #return render_template("package/ceh_comment_list.html", pkg_id=c.pkg.id, pkg_name=c.pkg.name, userobj=c.userobj)
    data = ['Element 1', ' Element 2', 'Element 3']
    return jsonify({'result': True, 'data': False})
