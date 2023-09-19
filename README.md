# TS2TF.py - *time series 2 transfer function*
*Estimate the **transfer function** of a dynaimc system, from its **step response***.

<p align="center">
  <img width="60%" src="https://github.com/mare-mrgazo/TS2TF.py/assets/132171582/13056431-ae36-4e3b-8c99-ae9c1ab9681b">
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

## Error Functions
The arrays x and y each have a length of **n** and are **[normalized](https://www.statology.org/normalize-data-between-0-and-1/)**.

<div align="center">

***ISE** (Integral of Squared Error):*

$$ISE =\frac{1}{n}\sum_{i=0}^{n}(y_i-y)^2$$
 
***ITSE** (Integral of Time Squared Error):*

$$ITSE =\frac{1}{n}\sum_{i=0}^{n}x_i(y_i-y)^2$$

***IITSE** (Integral of Inverse Time Squared Error):*

$$IITSE =\frac{1}{n}\sum_{i=0}^{n}(1-x_i)(y_i-y)^2$$

#### *Examples*

</div>

<p align="center">
  <img width="70%" src="https://github.com/mare-mrgazo/TS2TF.py/assets/132171582/c4d4775a-c4a5-4a36-95de-8785bc04d02b">
</p>

</div>

## Function Definitions

- ### TS2TF.SOS(x, y, iters, L, K, ωn, ζ)

    *Estimates the system as a **[second order](https://apmonitor.com/pdc/index.php/Main/SecondOrderSystems)** transfer function.*

    #### Inputs

    - **iters** - *number of iterations*
    - **L** - *learing rate, typicaly 0.9*

    - **K** - *first iteration "gain" 0.01 ~ 0.99*
    - **ωn** - *first iteration natural frequency 1 ~ 50*
    - **ζ** - *first iteration damping ratio 0.01 ~ 0.99*

    #### Example Usage

    ```python
    e = TS2TF.SOS(
        x_data, y_data, 
        err = 'ISE'
        iters = 200, 
        L = 0.9,

        K = 0.7,
        ωn = 5,
        ζ = 0.7
    )
    print(e['K'], e['ωn'], e['ζ'])
    print(e['tf'])
    print(e['ISE'])

    plt.plot(x_data, y_data)
    plt.plot(x_data, e['y'])
    ```

- ### TS2TF.FOS(x, y, iters, L, K, T)

    *Estimates the system as a **[first order](https://courses.engr.illinois.edu/ece486/fa2017/documents/set6.pdf)** transfer function.*

    #### Inputs

    - **iters** - *number of iterations*
    - **L** - *learing rate, typicaly 0.9*

    - **K** - *first iteration gain 0.01 ~ 0.99*
    - **T** - *first iteration time constant 0.01 ~ 0.99*


    ```python
    e = TS2TF.FOS(
        x_data, y_data, 
        err = 'ITSE'
        iters = 200, 
        L = 0.9,

        K = 0.7,
        T = 0.5
    )
    print(e['K'], e['T'])
    print(e['tf'])
    print(e['ITSE'])

    plt.plot(x_data, y_data)
    plt.plot(x_data, e['y'])
    ```

## The Problem of Local Minima

*Machine learning algorithms, such as gradient descent algorithms, may become trapped in local minima during model training. That's why it is more efficient to reduce the number of **iterations** and increase the variety of initial values for independent variables.*

```python
estimate = TS2TF.SOS(
    x_data, y_data, 
    err = 'ISE'
    L = 0.9
    iters = 10, 

    K = 0.7,
    ωn = [5, 10, 15],
    ζ = 0.7,
)
```

*Instead of passing just one value for ωn, we pass a **list** of values. This may increase computation time but decreases the likelihood of becoming stuck in a local minimum.*

```python
refining = TS2TF.SOS(
    x_data, y_data, 
    err = 'ISE'
    L = 0.9
    iters = 200, 

    K = estimate['K'],
    ωn = estimate['ωn'],
    ζ = estimate['ζ'],
)
```

*When we are confident that we are converging towards the global minimum, we can refine the results by increasing the number of iterations.*


## Acknowledgements
  *Special thanks to:*
 - https://www.derivative-calculator.net/
 - https://www.electrical4u.com/time-response-of-second-order-control-system/
