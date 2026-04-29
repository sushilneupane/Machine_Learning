# first ma modle ley weighted sum nikalxa ie similar to linear regression
# z = θ0 + θ1*x1 + θ2*x2 + θ3*x3 + θ4*x4

#sigmoid funtion
#ℎ𝜃(𝑥)=1/1+𝑒^−𝑧 
# Interpretation:
# hθ(x) ≈ 1  → high probability of PASS
# hθ(x) ≈ 0  → high probability of FAIL

# COST FUNCTION (LOG LOSS) error measure garna use garni
# J(θ) = -(1/m) * Σ [ y*log(hθ(x)) + (1 - y)*log(1 - hθ(x)) ]


# GRADIENT OF COST FUNCTION
# ∇J(θ) = (1/m) * Xᵀ (hθ(X) - Y)
# Expanded form:
# ∂J/∂θj = (1/m) * Σ (hθ(xᵢ) - yᵢ) * xᵢⱼ


# GRADIENT DESCENT (OPTIMIZATION)
# update parameters using:
# θ := θ - α * ∇J(θ),,,,,α = learning rate


# PREDICTION (PROBABILITY)
# P(y = 1 | x) = hθ(x)

# Step 1: Compute z = θᵀx
# Step 2: Apply sigmoid → probability
# Step 3: Compute cost (log loss)
# Step 4: Compute gradient
# Step 5: Update θ using gradient descent
# Step 6: Repeat until convergence
# Step 7: Predict pass/fail using threshold








import numpy as np 
import pandas as pd

def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

    #sigmoid funtion ley value lai probability ma convert garxa(0or1)

def calculate_gradient(theta, X, Y):
    m = Y.size   # fixed
    return (X.T @ (sigmoid(X @ theta) - Y)) / m 
    #X@theta = linear combination of theta("@ bhaneko matrix multiplication ho")
    #X@error = direction to adjust weight

def gradient_descend(X, Y, alpha=0.1, num_iter=1000, tol=1e-7):
    X_b = np.c_[np.ones((X.shape[0],1)), X]
    theta = np.zeros(X_b.shape[1])
    
    #gradient descend training loop, error ghataudai jani"remember the U shape of parabola and minimizing to the least point"
    for i in range(num_iter):
        grad = calculate_gradient(theta, X_b , Y)  
        theta -= alpha * grad #updating weights θ:=θ−α∇J(θ)


        if np.linalg.norm(grad) < tol: #theta minimum point ma pugesi stop gareko"parabolic minima"
            break
    return theta

def predict_proba(X, theta):
    X_b = np.c_[np.ones((X.shape[0],1)), X]
    return sigmoid(X_b @ theta) #sigmid lagayera probability measure gareko [0.2, 0.8, 0.95, 0.1]  

def predict(X, theta, threshold=0.5):
    return (predict_proba(X,theta)>=threshold).astype(int)


# LOAD DATASET

data = pd.read_csv("dataset.csv")

# Features (multiple now)
X = data[['attendance_pct','homework_pct','midterm_score','study_hours_per_week']].values

# Target
y = data['pass'].values

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# TRAIN MODEL

theta_hat = gradient_descend(X_train_scaled, y_train, alpha=0.1)


# PREDICTION

y_pred_train = predict(X_train_scaled, theta_hat)
y_pred_test = predict(X_test_scaled, theta_hat)

train_acc = accuracy_score(y_train,y_pred_train)
test_acc = accuracy_score(y_test,y_pred_test)

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)