import numpy as np
import random as rnd
import math
from scipy.optimize import minimize
from plotting import plot_data


# =============================================================================
# ==== Defining Kernels =======================================================
# =============================================================================
def linear_kernel(x_i, x_j):
    '''This kernel simply returns the scalar product between the two points.
    This results in a linear separation.'''
    linear = np.dot(x_i, x_j)
    return linear


def polynomial_kernel(x_i, x_j, p=2):
    '''This kernel allows for curved decision boundaries.
    The exponent p (apositive integer) controls the degree of the polynomials.
    p = 2 will make quadratic shapes (ellipses, parabolas, hyperbolas).
    Setting p = 3 or higher will result in more complex shapes.'''
    poly = np.power((np.dot(x_i, x_j) + 1), p)
    # Polynomial order:
    # P = 2 => Quadratic shapes (ellipses, parabolas, hyperbolas).
    # P > 2 => More complex shapes.
    return poly


def radial_basis_kernel(x_i, x_j, sigma=0.5):
    '''This kernel uses the explicit euclidian distance between the two
    datapoints, and often results in very good boundaries. The parameter sigma
    is used to control the smoothness of the boundary.'''
    norm_squared = np.power(np.linalg.norm(np.subtract(x_i, x_j)), 2)
    radial = math.exp(-norm_squared / (2 * np.power(sigma, 2)))
    # Sigma:
    # Low => High bias & Low variance
    # High => Low bias & High variance
    return radial


# =============================================================================
# ==== Defining Functions =====================================================
# =============================================================================
def objective(alpha):
    '''Objective is a function which takes a vector alpha as argument and
    returns a scalar value, effectively implementing the expression that should
    be minimized'''
    obj = 1/2 * np.dot(alpha, (np.dot(alpha, P))) - sum(alpha)
    return obj


def zerofun(alphas):
    '''Zerofun is a function which calculates the value which should be
    constrained to zero.'''
    zero = np.dot(alphas, targets)
    return zero


def precomputation():
    '''A precomputation for the support vector machine. Creates a global matrix
    P which is created using targets and selected Kernel function.'''

    global P

    N = len(inputs)
    P = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            P[i][j] = targets[i] * targets[j] * kernel(inputs[i], inputs[j])
    return P


def minimize_function(C=None):
    '''Main function that will find the vector which minimizes the function
    objective within the bounds B and the constraints XC.'''

    global alphas

    # Initialize
    B = [(0, C) for b in range(N)]

    # Initial guess for alpha
    start = np.zeros(N)

    # Constraints
    XC = {'type': 'eq', 'fun': zerofun}

    minimized = minimize(objective, start, bounds=B, constraints=XC)
    alphas = minimized['x']
    converged = minimized['success']
    return converged


def extract_alphas(threshold=10**(-5)):
    '''Extracing valid alphas, i.e. alphas larger than 0. Alphas larger than
    zero are assumed to be alphas larger than 10^-5.'''

    global sv, idx

    sv = []
    idx = []
    for i, a in enumerate(alphas):
        if a > threshold:
            sv.append(a)
            idx.append(i)
    return sv, idx


def calculate_threshold(s):
    '''Calculating the threshold (equation 7). This can be done from the fact
    that the indicator function for any support vector has a value equal to its
    target value, since we know that it is exactly on the margin.'''
    b = 0  # threshold/bias
    for i in idx:
        b += alphas[i] * targets[i] * kernel(s, inputs[i])
    b -= indicator(s)
    return b


def indicator(s):
    '''The indicator function (equation 6) which uses the non-zero alphas
    together with their datapoints and targets to classify new points.'''
    ind = 0  # indicator
    for i in idx:
        ind += alphas[i] * targets[i] * kernel(s, inputs[i])
    return ind


def decision_boundry():
    '''Creating datapoints for decision boundry'''
    xgrid = np.linspace(-5, 5)
    ygrid = np.linspace(-4, 4)
    grid = np.array([[indicator(np.array([x, y]))
                      for x in xgrid] for y in ygrid])
    return xgrid, ygrid, grid


# =============================================================================
# ==== Generating datapoints ==================================================
# =============================================================================
def generate_data(samples=20, std=0.2, xi_mu=1.5, xj_mu=0.5):
    '''Generating datapoints for a training dataset.'''

    global targets, inputs, N

    classA = np.concatenate(
        (np.random.randn(int(samples/2), 2) * std + [xi_mu, xj_mu],
         np.random.randn(int(samples/2), 2) * std + [-xi_mu, xj_mu]))
    classB = np.random.randn(samples, 2) * std + [xi_mu*0, -xj_mu]

    inputs = np.concatenate((classA, classB))
    targets = np.concatenate(
        (np.ones(classA.shape[0]),
         -np.ones(classB.shape[0])))

    N = inputs.shape[0]  # Number of Rows = Number of Samples

    permute = list(range(N))  # rearrange sequence
    rnd.shuffle(permute)

    inputs = inputs[permute, :]
    targets = targets[permute]

    # print('====================================')
    # print(f'The input datapoints are \n{inputs}')
    # print(f'with target classes \n{targets}')

    return classA, classB


def generate_advanced_data(samples=30, std=0.7, xi_mu=1.5, xj_mu=0.5):
    '''Generating datapoints for a training dataset.'''

    global targets, inputs, N

    classA = np.concatenate(
        (np.random.randn(int(samples/2), 2) * std + [xi_mu, xj_mu],
         np.random.randn(int(samples/2), 2) * std + [-xi_mu, -2*xj_mu]))
    classB = np.random.randn(samples, 2) * std + [xi_mu*0, -xj_mu]

    inputs = np.concatenate((classA, classB))
    targets = np.concatenate(
        (np.ones(classA.shape[0]),
         -np.ones(classB.shape[0])))

    N = inputs.shape[0]  # Number of Rows = Number of Samples

    permute = list(range(N))  # rearrange sequence
    rnd.shuffle(permute)

    inputs = inputs[permute, :]
    targets = targets[permute]

    # print('====================================')
    # print(f'The input datapoints are \n{inputs}')
    # print(f'with target classes \n{targets}')

    return classA, classB


# =============================================================================
# ==== Generate Support Vector ================================================
# =============================================================================
def run_svm():
    '''Main function. This function calls all other functions defined in this
    file. This function is in turn called when running the file.'''

    # Setting global variables
    global kernel, C

    # ==== SELECT KERNEL ==== #
    '''Select which Kernel to use.'''
    # kernel = linear_kernel
    # kernel = polynomial_kernel
    kernel = radial_basis_kernel

    # ==== SET SLACK: ==== #
    '''Select slack.
    Slack is the maximum value for the SV alphas.
    Large slack has no effect on the decision boundry.
     - Large slack does not lower the complexity.
    Smaller slack-values increases the margin.
     - Small slack decreases the complexitity -> Lower variance.'''
    Cval = 20
    # Cval = None

    # Generating datapoints:
    # classA, classB = generate_data(samples=20)
    classA, classB = generate_advanced_data(samples=40)

    # Precomputation of the P-matrix:
    precomputation()

    # Minimize
    converged = minimize_function(C=Cval)
    print('====================================')
    print(f'Minimization successfull: {converged}')
    if converged is False:
        raise ValueError('Minimization did not converge.')

    # Extract non-zero alphas
    extract_alphas()
    print('====================================')
    print(f'The Support Vector is \n{inputs[idx]}')
    print(f'with alphas \n {alphas[idx]}')
    print('====================================')

    # Generate decision boundry
    XGrid, YGrid, Grid = decision_boundry()
    XYGrid = [XGrid, YGrid, Grid]

    return classA, classB, XYGrid


def plot_results(classA, classB, XYGrid):

    # Plot data
    # plot_data(classA, classB)

    # Plot Data and SV
    # print(Grid)
    # filename = 'plt-res_advanced_C-1.png'
    # print(classA)
    plot_data(classA, classB,
              XYGrid)
    # plot_data(classA, classB,
    #           XYGrid, SaveAs=filename)


# =============================================================================
# ==== Run main file ==========================================================
# =============================================================================
if __name__ == '__main__':
    np.random.seed(100)
    classA, classB, XYGrid = run_svm()

    # Test classifier:
    tx = [(0, 0), (2, 2), (-2, -2), (-2, 2), (2, -2)]
    print('====================================')
    print('TESTING:')
    for t in tx:
        ind = indicator(t)
        if ind >= 0:
            c = 'Class +1 "Blue"'
        else:
            c = 'Class -1 "Red"'
        print(f'Datapoint {t} = {c}')
    print('====================================')

    plot_results(classA, classB, XYGrid)
