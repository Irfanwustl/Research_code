from scipy.special import expit
def sigmoid_shape(x, high, low):
    return expit(x)*(high-low)+low
