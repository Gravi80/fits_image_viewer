from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
from io import BytesIO
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS
from astropy import units as u
import aplpy
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import ftplib

app = Flask(__name__)


@app.route('/fits_image/')
def source_image():
	fit = read_fits_file('sample.fits')
	figfile = BytesIO()

	cord = SkyCoord(ra=fit.header['OBJCTRA'], dec=fit.header['OBJCTDEC'], frame=ICRS,unit=(u.hourangle, u.deg))
	fig=plt.figure(figsize=(20,15))
	F = aplpy.FITSFigure(fit, figure=fig)
	F.show_grayscale()
	F.show_markers(cord.ra.hourangle, cord.dec.deg)
	plt.savefig(figfile,bbox_inches='tight',pad_inches=0)
	resp = Response(response=figfile.getvalue(), status=200, mimetype="image/png")
	return resp

def read_fits_file(file_name):
	server = ftplib.FTP()
	server.connect('127.0.0.1', 2121)
	server.login('user3','54321')
	array = bytearray()
	server.retrbinary('RETR {0}'.format(file_name),lambda x: array.extend(x))
	res1=bytes(array)
	return fits.PrimaryHDU.fromstring(res1)

@app.route('/')
def index():
	return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=True)