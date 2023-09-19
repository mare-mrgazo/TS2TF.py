# TS2TF.py - *time series 2 transfer function*
*Estimate the **transfer function** of a dynaimc system, from its **step response***.

<p align="center">
  <img width="40%" src="https://github.com/mare-mrgazo/TS2TF.py/assets/132171582/13056431-ae36-4e3b-8c99-ae9c1ab9681b">
</p>

 $$\ F(s)=\frac{73.5}{s^2+8.12*s+98} $$
 
## Quickstart
1. Clone the repo
   ```python
   git clone https://github.com/mare-mrgazo/TS2TF.py.git
   ```
3. Run the example 
   ```python
   python /TS2TF.py/example/main.py
   ```
## Explanation
*With this python module you can estimate the [transfer function](https://en.wikipedia.org/wiki/Transfer_function) of a dynamic system based on its [step response](https://en.wikipedia.org/wiki/Step_response). Under the hood, there's a simple iterative [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) optimization algorithm with a customizable [learning rate](https://en.wikipedia.org/wiki/Learning_rate) (denoted as **"L"**). This optimization algorithm seeks local minima of a user-selectable **error function***.

## Error functions
The arrays x and y each have a length of **n** and are **[normalized](https://www.statology.org/normalize-data-between-0-and-1/)**.

1. ***ISE** (Integral of Squared Error):*
 $$ISE =\frac{1}{n}\sum_{i=0}^{n}(y_i-y)^2$$
 
2. ***ITSE** (Integral of Time Squared Error):*
 $$ITSE =\frac{1}{n}\sum_{i=0}^{n}x_i(y_i-y)^2$$

3. ***IITSE** (Integral of Inverse Time Squared Error):*
 $$IITSE =\frac{1}{n}\sum_{i=0}^{n}(1-x_i)(y_i-y)^2$$

## 

 ## TS2TF.SOS(x, y, epochs, L, K, ωn, ζ)

*Estimates the system as a second order tf.*

#### Example Usage

```python
estimate = TS2TF.SOS(
    x_data, y_data, 
    epochs = 1000, 
    L = 0.9,
    K = 0.7,
    ωn = 5,
    ζ = 0.7
)
print(estimate['tf'])
plt.plot(x_data, y_data)
plt.plot(x_data, estimate['y'])
```

#### Inputs
      
  - x, y - step response data (normallized)
  - epochs - number of training cycles, 1000 ~ 5000
  - L - learing rate, 0.1 ~ 0.9
  - K - first iteration gain, 0.6 ~ 0.8
  - ωn - first iteration natural frequency, 0.6 ~ 0.8
  - ζ - first iteration damping ratio 0.1 ~ 0.9
  
#### Outputs
    
  - K - gain
  - ωn - natural frequency
  - ζ - damping ratio
  - tf - transfer function coefficients 
  - y - tf step response time series data
  - rms - root mean square

</br>
</br>


## TS2TF.FOS(x, y, epochs, L, K, T)

*Estimates the system as a first order tf.*

#### Example Usage

```python
estimate = TS2TF.FOS(
    x_data, y_data, 
    epochs = 1000, 
    L = 0.01,
    K = 0.7,
    T = 0.5
)
print(estimate['tf'])
plt.plot(x_data, y_data)
plt.plot(x_data, estimate['y'])
```

#### Inputs
      
  - x, y - step response data (normalized)
  - epochs - number of training cycles, 1000 ~ 5000
  - L - learning rate, 0.01 ~ 0.09
  - K - first iteration gain, 0.6 ~ 0.8
  - T - first iteration time constant, 0.6 ~ 0.8
  
#### Outputs
    
  - K - gain
  - T - time constant
  - tf - transfer function coefficients 
  - y - tf step response time series data
  - rms - root mean square

</br>
</br>

## Acknowledgements
  *Special thanks to:*
 - https://www.derivative-calculator.net/
 - https://www.electrical4u.com/time-response-of-second-order-control-system/
