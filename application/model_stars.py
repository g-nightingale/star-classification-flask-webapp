import numpy as np
import lightgbm
import joblib 

def predict_star_type(temp, lumen, radius, a_m, color, spectral_class):
    """ Return predicted star type from light gbm model"""

    MODEL_PATH = 'application/lgb_stars.pkl'

    # Encode the data
    data_a = [temp, lumen, radius, a_m]
    data_b = encode_colors(color)
    data_c = encode_spectral(spectral_class)
    new_data = np.array(data_a + data_b + data_c)
    new_data = np.reshape(new_data, (1, new_data.shape[0]))

    # Load model
    lgb = joblib.load(MODEL_PATH)
    
    # Make prediction and get probability
    pred = lgb.predict(new_data)
    prob = lgb.predict_proba(new_data).max()
    
    # Get the star type
    star_type = get_star_type(pred)
    
    return star_type, prob

def encode_colors(color):
    """ Encode binary variables for color """
    
    if color == "Red":
        return [1, 0, 0, 0, 0, 0, 0, 0, 0]
    elif color == "Blue":
        return [0, 1, 0, 0, 0, 0, 0, 0, 0]
    elif color == "Blue-White":
         return [0, 0, 1, 0, 0, 0, 0, 0, 0]       
    elif color == "White":
         return [0, 0, 0, 1, 0, 0, 0, 0, 0]    
    elif color == "Yellow-White":
         return [0, 0, 0, 0, 1, 0, 0, 0, 0]  
    elif color == "Yellow":
         return [0, 0, 0, 0, 0, 1, 0, 0, 0]  
    elif color == "Orange":
         return [0, 0, 0, 0, 0, 0, 1, 0, 0]  
    elif color == "Orange-Red":
         return [0, 0, 0, 0, 0, 0, 0, 1, 0]  
    elif color == "Yellow-Orange":
         return [0, 0, 0, 0, 0, 0, 0, 0, 1]  
    else:
         return [0, 0, 0, 0, 0, 0, 0, 0, 0] 

def encode_spectral(spectral_class):
    """ Encode binary variables for spectral class """
    
    if spectral_class == "M":
         return [1, 0, 0, 0, 0, 0, 0]
    elif spectral_class == "B":
         return [0, 1, 0, 0, 0, 0, 0]
    elif spectral_class == "O":
         return [0, 0, 1, 0, 0, 0, 0]       
    elif spectral_class == "A":
         return [0, 0, 0, 1, 0, 0, 0]    
    elif spectral_class == "F":
         return [0, 0, 0, 0, 1, 0, 0]  
    elif spectral_class == "K":
         return [0, 0, 0, 0, 0, 1, 0]  
    elif spectral_class == "G":
         return [0, 0, 0, 0, 0, 0, 1]  
    else:
         return [0, 0, 0, 0, 0, 0, 0]  
         
def get_star_type(pred):
    """ Return the star type given a predicted class """
    
    if pred == 0:
        return 'Red Dwarf'
    elif pred == 1:
        return 'Brown Dwarf'
    elif pred == 2:
        return 'White Dwarf'
    elif pred == 3:
        return 'Main Sequence'
    elif pred == 4:
        return 'Super Giants'
    elif pred == 5:
        return 'Hyper Giants'
    else: 
        return 'Unknown'

# Testing
if __name__ == "__main__":
    print(predict_star_type(3068, 0.0024, 0.17, 16.12, "Red", "M"))
    print(predict_star_type(3342, 0.0015, 0.3070, 11.87, "Red", "M"))
    print(predict_star_type(9383, 342940.00, 98.00, -6.98, "Blue", "O"))