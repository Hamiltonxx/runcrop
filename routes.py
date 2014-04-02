from flask import Flask, render_template , request
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.restless import APIManager
import json
import requests
import subprocess

app = Flask(__name__)

app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hamilton:123456@121.199.44.22/decropsys33'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hamilton:123456@192.168.192.108/decropsys33'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hamilton:123456@192.168.1.104/decropsys39'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hamilton:123456@10.10.99.27/decropsys34'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), nullable=True)
	role = db.Column(db.String(255), nullable=False)

#SiteGeography
class Site(db.Model):
	site_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	site_name = db.Column(db.String(255), unique=True, nullable=False)
	country = db.Column(db.String(255))
	province = db.Column(db.String(255))
	city = db.Column(db.String(255))
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	owner = db.relationship('User', backref=db.backref('sites',lazy='dynamic'))

#DailyEnvironmentData
class Daily(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	year = db.Column(db.String(10))
	day = db.Column(db.Integer)
	t_mean = db.Column(db.Float)
	t_max = db.Column(db.Float)
	t_min = db.Column(db.Float)
	humidity = db.Column(db.Float)
	#total_solar_radiation
	totalradiation = db.Column(db.String(50))
	#atmosphere_transmittance
	transmittance = db.Column(db.Float)
	rainfall = db.Column(db.Float)
	windspeed = db.Column(db.Float)
	co2mean = db.Column(db.Float)
	airpressure = db.Column(db.Float)

	siteid = db.Column(db.Integer,db.ForeignKey('site.site_id'))
	sitedetecting = db.relationship('Site', backref=db.backref('dailys',lazy='dynamic')) 

class Cultivars(db.Model):
	cultivar_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	cultivar_name = db.Column(db.String(255))
	species_name = db.Column(db.String(255))
	sub_species = db.Column(db.String(255))
	culmethod = db.Column(db.String(50))
	fromcountry = db.Column(db.String(50))
	fromprovince = db.Column(db.String(50))

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	owner = db.relationship('User', backref=db.backref('cultivars',lazy='dynamic'))

class Cultivation(db.Model):
	cultivation_id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer)
	sow_day = db.Column(db.Integer)
	flower_time = db.Column(db.Integer)
	mature_time = db.Column(db.Integer)
	havest_time = db.Column(db.Integer)
	row_distance = db.Column(db.Float)
	plant_distance = db.Column(db.Float)

	siteid = db.Column(db.Integer,db.ForeignKey('site.site_id'))
	cultivarname = db.Column(db.Integer, db.ForeignKey('cultivars.cultivar_name'))
	relatesite = db.relationship('Site', backref=db.backref('cultivations',lazy='dynamic'))
	relatecultivar = db.relationship('Cultivars', backref=db.backref('cultivations',lazy='dynamic'))
	owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	owner = db.relationship('User',backref=db.backref('cultivations',lazy='dynamic'))
	

class Gmeasure(db.Model):
	gmeasure_id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.Integer)
	main_stem_height = db.Column(db.Float)
	main_stem_spike_height = db.Column(db.Float)
	tiller_number = db.Column(db.Integer)
	max_tiller_angle = db.Column(db.Float)
	lai = db.Column(db.Float)
	main_stem_leaf_number = db.Column(db.Integer)
	spike_number = db.Column(db.Integer)
	effective_spike_number = db.Column(db.Integer)
	leaf_dry_weight = db.Column(db.Float)
	stem_dry_weight = db.Column(db.Float)
	root_dry_weight = db.Column(db.Float)
	spike_dry_weight = db.Column(db.Float)

	cultivationid = db.Column(db.Integer, db.ForeignKey('cultivation.cultivation_id'))
	belongcul = db.relationship('Cultivation',backref=db.backref('gmeasures',lazy='dynamic'))

class Pstructure(db.Model):
	pstructure_id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.Integer)
	plant_id = db.Column(db.Integer)
	stem_id = db.Column(db.Integer)
	leaf_id = db.Column(db.Integer)
	leaf_base_height = db.Column(db.Float)
	leaf_length = db.Column(db.Float)
	leaf_width = db.Column(db.Float)
	leaf_angle = db.Column(db.Float)
	leaf_curvature = db.Column(db.Float)

	cultivationid = db.Column(db.Integer, db.ForeignKey('cultivation.cultivation_id'))
	belongcul = db.relationship('Cultivation', backref=db.backref('pstructures',lazy='dynamic'))

class D3model(db.Model):
	d3modelid = db.Column(db.Integer,primary_key=True)
	z_k = db.Column(db.Float)
	l_k = db.Column(db.Float)
	w_k = db.Column(db.Float)
	a_k = db.Column(db.Float)
	c_k = db.Column(db.Float)
	k_shape = db.Column(db.Float)
	data_file = db.Column(db.String(255))
	pics = db.Column(db.String(255))
	pstructure_id = db.Column(db.Integer, db.ForeignKey('pstructure.pstructure_id'))
	pstruct = db.relationship('Pstructure',backref=db.backref('d3models',lazy='dynamic'))
	
	def __init__(self,d3modelid,z_k,l_k,w_k,a_k,c_k,k_shape,data_file,pics,pstructure_id):
		self.d3modelid=d3modelid;self.z_k=z_k;self.l_k=l_k;self.w_k=w_k;self.a_k=a_k;self.c_k=c_k;self.k_shape=k_shape;self.data_file=data_file;self.pics=pics;self.pstructure_id=pstructure_id
	
db.create_all()

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET','POST','PUT','DELETE'])
manager.create_api(Site, methods=['GET','POST','PUT','DELETE'], results_per_page=0)
manager.create_api(Daily, methods=['GET','POST','PUT','DELETE'], results_per_page=0)
manager.create_api(Cultivars, methods=['GET','POST','PUT','DELETE'], results_per_page=0)
manager.create_api(Cultivation, methods=['GET','POST','PUT','DELETE'], results_per_page=0)
manager.create_api(Gmeasure, methods=['GET','POST','PUT','DELETE'], results_per_page=0)
manager.create_api(Pstructure, methods=['GET','POST','PUT','DELETE'], results_per_page=0)
manager.create_api(D3model, methods=['GET','POST','PUT','DELETE'], results_per_page=0)

@app.route('/')
def index():
	return render_template("home.html")

@app.route('/experiment')
def experiment():
	return render_template('experiment.html')

@app.route('/experiment/sitegeo')
def sitegeo():
	return render_template('sitegeo.html')

@app.route('/experiment/sitedaily')
def sitedaily():
	sites = Site.query.all()
	return render_template('sitedaily.html',sites=sites)

@app.route('/experiment/cultivars')
def cultivars():
	return render_template('cultivars.html')

@app.route('/experiment/cultivation')
def cultivation():
	sites = Site.query.all()
	cultivars = Cultivars.query.all()
# 	for x in sites:
# 		print x.site_name
# 	for y in cultivars:
# 		print y.cultivar_name
	return render_template('cultivation.html',sites=sites,cultivars=cultivars)

@app.route('/experiment/growth')
def growth():
	return render_template('growth.html')

@app.route('/experiment/pstruct')
def pstruct():
	cultivations = Cultivation.query.all()
	return render_template('pstruct.html',cultivations=cultivations)

@app.route('/modeling')
def modeling():
	pstructures = Pstructure.query.all()
	return render_template('modeling.html',pstructures=pstructures)

@app.route('/modelresults')
def modelresults():
	return render_template('modelresults.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')
       
@app.route('/d3model')
def d3model():
	d3modelid = request.args.get('d3modelid')
	plantstructureid = request.args.get('plantstructureid')
	print plantstructureid
	z_k = request.args.get('z_k')
	l_k = request.args.get('l_k')
	w_k = request.args.get('w_k')
	a_k = request.args.get('a_k')
	c_k = request.args.get('c_k')
	k_shape = request.args.get('k_shape')
	
	ricechild = subprocess.Popen("rice MD.bo.WT.txt "+z_k+" "+l_k+" "+w_k+" "+a_k+" "+c_k+" "+k_shape+" "+d3modelid+" 0")
#	ricechild = subprocess.Popen("rice MD.bo.WT.txt 1 1 1 1 1 1 ZZ10 0")
	ricechild.wait()
	d3 = D3model(d3modelid,z_k,l_k,w_k,a_k,c_k,k_shape,d3modelid+".Chl4.txt",d3modelid+".jpg",plantstructureid)
	db.session.add(d3)
	db.session.commit()
	return str(ricechild.pid)

@app.route('/checklogin')
def checklogin():
	username = request.args.get('username')
	password = request.args.get('password')
	print username,password
	users = User.query.all()
	for u in users:
		if username == u.username and password == u.password:
			return str(u.id)
	else:
		return ""
#@app.route('/site/post')
#def addsite():
#	if request.method == 'POST':
#		print 'POSTPOST'
#		newrecord = {'site_id':10011,'site_name':u'test11','country':u'China','province':u'Shanghai','city':u'Shanghai','latitude':120.1,'longitude':71.9}
#		r = requests.post('http://192.168.2.112:5000/api/site',data=json.dumps(newrecord),headers={'content-type':'application/json'})
#		print r.status_code, r.content

app.debug = True
app.run("0.0.0.0")
