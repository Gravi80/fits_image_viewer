from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
from io import BytesIO
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS
from astropy import units as u
import aplpy
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)


@app.route('/fits_image/')
def source_image():
	fit = fits.open('sample.fits')
	figfile = BytesIO()

	cord = SkyCoord(ra=fit[0].header['OBJCTRA'], dec=fit[0].header['OBJCTDEC'], frame=ICRS,unit=(u.hourangle, u.deg))
	fig=plt.figure(figsize=(20,15))
	plt.axis('off')
	fit[0].data = list(fit[0].data)
	F = aplpy.FITSFigure(fit[0], figure=fig)
	F.show_grayscale()
	F.show_markers(cord.ra.hourangle, cord.dec.deg)
	plt.savefig(figfile,bbox_inches='tight',pad_inches=0)
	resp = Response(response=figfile.getvalue(), status=200, mimetype="image/png")
	return resp

@app.route('/')
def index():
	return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=True)