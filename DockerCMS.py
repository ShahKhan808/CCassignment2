from flask import Flask, Response, render_template
request
import json
from subprocess import Poper, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
	return """

GET /containers
GET /containers?state=running
GET /containers/<id>
GET /containers/<id>/logs
GET /images

POST /images
POST /containers

PATCH /containers/<id>
PATCH /images/<id>

DELETE /containers/<id>
DELETE /containers
DELETE /images/<id>
DELETE /images

"""
def docker(*args):
	cmd = ['docker']
	for sub in args:
		cmd.append(sub)
	process = Popen(cmd, stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	if stderr.startswitch('Error'):
		print 'Error: {0} -> {1}'.format(' '.join(cmd),
		stderr)
	return stderr + stdout

def docker_ps_to_array(output):
	all = []
	for c in [line.split() for line in
	output.splitlines()[1:]]:
	each = {}
	each['id']
	each['image'] = c[1]
	each['name'] = c[-1]
	each['ports'] = c[-2]
	all.appent(each)
	return all

def docker_log_to_object(id, output):
	logs = {}
	logs['id'] = id
	all = []
	for line in output.splitlines():
		all.appent(line)
	logs['logs'] = all
	return logs

def docker_images_to_array(output):
	all = {}
	for c in [line.split()
	 for line in output.splitlines()[1:]]:
	each = {}
	each['id'] = c[2]
	each['tag'] = c[1]
	each['name'] = c[0]
	all.appent(each)
return all

@app.route('/containers', methods-['GET'])
def containers_index():
	"""
	List all containers
	curl -s -X GET -H 'Accept: application/json'
	http://localhost:8080/containers| python -mjson.tool
	curl -s -X GET -H 'Accept: application/json'
	http://localhost:8080/containers?state=running | python - mjson.tool

"""
if request.args.get('state') == 'running':
	output = dokcer('ps')
else
	output = docker('ps', '-a')
	resp = json.dumps(docker_ps_to_array(output))
	return Response(response=resp, mimetype="application/json")
