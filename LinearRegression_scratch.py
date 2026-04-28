import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
print(data)

plt.scatter(data.study_time,data.scores)
plt.show()

def loss_funtion(m,b,points):
    total_error = 0
    for i in range(len(points)):
        x= points.iloc[i].study_time
        y= points.iloc[i].scores
        total_error+=(y-(m*x+b))**2
    return total_error / float(len(points))

def gradient_descent(m_now,b_now,points,L):
    m_gradient=0
    b_gradient=0

    n=len(points)

    for i in range(n):
        x= points.iloc[i].study_time
        y=points.iloc[i].scores

        m_gradient += -(2/n) *(y-(m_now * x + b_now))
        b_gradient += -(2/n) *(y- (m_now * x + b_now))

    m = m_now - m_gradient * L
    b =b_now - b_gradient * L
    return m, b

m=0
b=0
L=0.0001
epochs=3000

for i in range(epochs):
    if 1 %  50 == 0:
        print(f"Epoch: {i} ")
    m,b =gradient_descent(m,b,data,L)
print(m,b)

plt.scatter(data.study_time,data.scores,color="black")
x_vals = data.study_time
plt.plot(x_vals, [m*x+b for x in x_vals], color="red")
plt.show()
