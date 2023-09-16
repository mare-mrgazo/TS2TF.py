# TS2TF.py - *time series 2 transfer function*
Estimate the transfer function of a system, from its **step response** (time series data).

<p align="center">
  <img width="40%" src="https://github.com/mare-mrgazo/TS2TF/assets/132171582/bf45a50d-389d-4b24-bc45-1543849149c2">
</p>

 $$\ F(s)=\frac{73.5}{s^2+8.12*s+98} $$

</br>

## Quickstart
1. Clone the repo
   ```cmd
   git clone https://github.com/mare-mrgazo/TS2TF.py.git
   ```
2. Run example
   ```cmd
   python /TS2TF/example/main.py
   ```

</br>
</br>

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
