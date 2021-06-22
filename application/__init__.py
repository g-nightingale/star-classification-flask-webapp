from flask import Flask, request, render_template, jsonify, url_for # Import flask libraries
from . import model_stars
from . import plot

def init_app():
    """ Create Flask app """

    # Initialize the flask class and specify the templates directory
    app = Flask(__name__, template_folder='templates')

    # Default route set as 'home'
    @app.route('/')
    @app.route('/home', methods=['GET'])
    def home():
        return render_template('home.html')

    # About page
    @app.route('/about', methods=['GET'])
    def about():
        return render_template('about.html')

    # Regression page
    @app.route('/prediction', methods=['GET'])
    def prediction():
        return render_template('prediction.html')

    # Visualisation page
    @app.route('/callback', methods=['POST', 'GET'])
    def cb():
        print(request.args.get('x_var'))
        print(request.args.get('y_var'))
        return plot.create_plot(request.args.get('x_var'), request.args.get('y_var'))

    @app.route('/visualisation', methods=['POST','GET'])
    def visualisation(x_var='temp_log', y_var='r_log'):
        graphJSON = plot.create_plot(x_var, y_var)
        return render_template('visualisation.html', graphJSON=graphJSON)

    # Links page
    @app.route('/links', methods=['GET'])
    def links():
        return render_template('links.html')

    # Prediction
    @app.route('/predict', methods=['POST','GET'])
    def predict_type():
        IMAGE_FOLDER = "static/images/"
        try:
            temp = request.args.get('temp')
            lumen = request.args.get('lumen')
            radius = request.args.get('radius')
            a_m = request.args.get('a_m')
            color = request.args.get('color')
            spectral_class = request.args.get('spectral_class')

            # Get the output from the classification model
            star_type, prob = model_stars.predict_star_type(temp, lumen, radius, a_m, color, spectral_class)
            prob = round(prob, 4)

            # Get image for rendering
            if star_type == 'Red Dwarf':
                image_fname = 'red_dwarf.jpg'
            if star_type == 'White Dwarf':
                image_fname = 'white_dwarf.jpg'
            elif star_type == 'Brown Dwarf':
                image_fname = 'brown_dwarf.jpg'
            elif star_type == 'Main Sequence':
                image_fname = 'main_sequence.jpeg'
            elif star_type == 'Super Giants':
                image_fname = 'super_giant.jpg'
            elif star_type == 'Hyper Giants':
                image_fname = 'hyper_giant.jpg'

            # Render the output in new HTML page
            return render_template('output.html', star_type=star_type, prob=prob, image_fname=image_fname)
        except:
            return 'Error'

    return app
    
# Run the Flask server
if(__name__=='__main__'):
    app = init_app()
    app.run(debug=True)  
