"""
    [TS2TF]

        [Estimates the transfer function of a system from its step response (time series data)]

            Author: [mrgazo.com]
            Version: [1.0.0]
            Date: [16.9.2023]

            [Special thanks to]
            https://www.derivative-calculator.net/
            https://www.electrical4u.com/time-response-of-second-order-control-system/

        [Function definitions]

            [TS2TF.FOS]

            Estimates the tf as a first order tf

                [Accepts, Example value]

                    x, y - step response data (normallized)
                    epochs - number of training cycles, 1000 ~ 5000
                    L - learing rate, 0.01 ~ 0.09
                    K - first iteration gain, 0.6 ~ 0.8
                    T - first iteration time constant, 0.6 ~ 0.8

                [Returns]

                    K - gain
                    T - time constant
                    tf - transfer function coefficients 
                    y - tf step response time series data
                    rms - root mean square

            [TS2TF.SOS]

            Estimates the tf as a second order tf

                [Accepts, Example value]

                    x, y - step response data (normallized)
                    epochs - number of training cycles, 1000 ~ 5000
                    L - learing rate, 0.1 ~ 0.9
                    K - first iteration gain, 0.6 ~ 0.8
                    ωn - first iteration natural frequency, 0.6 ~ 0.8
                    ζ - first iteration damping ratio 0.1 ~ 0.9

                [Returns]

                    K - gain
                    ωn - natural frequency
                    ζ - damping ratio
                    tf - transfer function coefficients 
                    y - tf step response time series data
                    rms - root mean square

"""
import math
import time


def FOS(x, y, epochs, L, K, T):

    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    elif not (isinstance(epochs, int) and int(epochs) > 0):
        raise ValueError("Number of epochs has to be a positive non-zero integer")
    elif not (isinstance(L, float) and L > 0):
        raise ValueError(
            "The learing rate L has to be a positive floating-point number"
        )

    def RMS(a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))

    def FOS(K, T, x):
        return K * (1 - math.exp(-x / T))

    t, r, n = time.process_time(), dict(), len(x)
    r["y"] = [0] * n
    r["rms"] = 1

    def GD(K_now, T_now, L):
        K_gradient = 0
        T_gradient = 0

        for i in range(n):
            K_gradient += (
                (2 / n)
                * (math.exp(-x[i] / T_now) - 1)
                * (y[i] - (1 - math.exp(-x[i] / T_now)) * K_now)
            )
            T_gradient += (
                (2 / n)
                * K_now
                * x[i]
                * (y[i] - K_now * (1 - math.exp(-x[i] / T_now)))
                * math.exp(-x[i] / T_now)
            ) / (T_now**2)

        K = K_now - K_gradient * L
        T = T_now - T_gradient * L

        return K, T

    for i in range(epochs):
        K, T = GD(K, T, L)
        if i % (epochs / 20) == 0 or i == (epochs - 1):
            for j in range(n):
                r["y"][j] = FOS(K, T, x[j])
            rms = round(RMS(r["y"], y), 2)
            print(
                "On epoch {}. {}% completed. {}s elapsed. RMS is: {}%".format(
                    i,
                    round(i / epochs * 100),
                    round(time.process_time() - t, 2),
                    int(rms * 100),
                )
            )
            print("K: {}, T: {}".format(round(K, 2), round(T, 2)))
            print("\n")
            if rms > r["rms"]:
                raise ValueError("The learing rate L is to large" "\n")
            r["rms"] = rms

    r["K"] = round(K, 2)
    r["T"] = round(T, 2)
    r["rms"] = round(RMS(r["y"], y), 2)
    r["tf"] = [r["K"], [r["T"], 1]]

    return r


def SOS(x, y, epochs, L, K, ωn, ζ):

    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    elif not (isinstance(epochs, int) and int(epochs) > 0):
        raise ValueError("Number of epochs has to be a positive non-zero integer")
    elif not (isinstance(L, float) and L > 0):
        raise ValueError(
            "The learing rate L has to be a positive floating-point number"
        )

    def RMS(a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))

    def SOS(K, ωn, ζ, x):
        ωc = ωn * math.sqrt(1 - ζ**2)
        return K * (
            1
            - (math.exp(-ζ * ωn * x) * math.sin(ωc * x + math.acos(ζ)))
            / (math.sqrt(1 - ζ**2))
        )

    t, r, n = time.process_time(), dict(), len(x)
    r["y"] = [0] * n
    r["rms"] = 1

    def GD(K_now, ωn_now, ζ_now, L):
        K_gradient = 0
        ωn_gradient = 0
        ζ_gradient = 0

        for i in range(n):
            K_gradient += (
                (2 / n)
                * (
                    (
                        math.exp(-ωn_now * x[i] * ζ_now)
                        * math.sin(
                            math.acos(ζ_now) + ωn_now * x[i] * math.sqrt(1 - ζ_now**2)
                        )
                    )
                    / math.sqrt(1 - ζ_now**2)
                    - 1
                )
                * (
                    y[i]
                    - (
                        1
                        - (
                            math.exp(-ωn_now * x[i] * ζ_now)
                            * math.sin(
                                math.acos(ζ_now)
                                + ωn_now * x[i] * math.sqrt(1 - ζ_now**2)
                            )
                        )
                        / math.sqrt(1 - ζ_now**2)
                    )
                    * K_now
                )
            )

            ωn_gradient += (
                (2 / n)
                * K_now
                * x[i]
                * math.exp(-2 * x[i] * ζ_now * ωn_now)
                * (
                    K_now
                    * math.sin(
                        x[i] * math.sqrt(1 - ζ_now**2) * ωn_now + math.acos(ζ_now)
                    )
                    + (y[i] - K_now)
                    * math.sqrt(1 - ζ_now**2)
                    * math.exp(x[i] * ζ_now * ωn_now)
                )
                * (
                    ζ_now
                    * math.sin(
                        x[i] * math.sqrt(1 - ζ_now**2) * ωn_now + math.acos(ζ_now)
                    )
                    - math.sqrt(1 - ζ_now**2)
                    * math.cos(
                        x[i] * math.sqrt(1 - ζ_now**2) * ωn_now + math.acos(ζ_now)
                    )
                )
            ) / (ζ_now**2 - 1)

            ζ_gradient += (
                (2 / n)
                * K_now
                * math.exp(-2 * ωn_now * x[i] * ζ_now)
                * (
                    K_now
                    * math.sin(
                        math.acos(ζ_now) + ωn_now * x[i] * math.sqrt(1 - ζ_now**2)
                    )
                    + (y[i] - K_now)
                    * math.sqrt(1 - ζ_now**2)
                    * math.exp(ωn_now * x[i] * ζ_now)
                )
                * (
                    (ωn_now * x[i] * ζ_now**2 + ζ_now - ωn_now * x[i])
                    * math.sin(
                        math.acos(ζ_now) + ωn_now * x[i] * math.sqrt(1 - ζ_now**2)
                    )
                    + (-ωn_now * x[i] * ζ_now - 1)
                    * math.sqrt(1 - ζ_now**2)
                    * math.cos(
                        math.acos(ζ_now) + ωn_now * x[i] * math.sqrt(1 - ζ_now**2)
                    )
                )
            ) / (ζ_now**2 - 1) ** 2

        K = K_now - K_gradient * L
        ωn = ωn_now - ωn_gradient * L
        ζ = ζ_now - ζ_gradient * L
        ζ = max(0, min(ζ, 0.99))

        return K, ωn, ζ

    for i in range(epochs):
        K, ωn, ζ = GD(K, ωn, ζ, L)
        if i % (epochs / 20) == 0 or i == (epochs - 1):
            for j in range(n):
                r["y"][j] = SOS(K, ωn, ζ, x[j])
            rms = round(RMS(r["y"], y), 2)
            print(
                "On epoch {}. {}% completed. {}s elapsed. RMS is: {}%".format(
                    i,
                    round(i / epochs * 100),
                    round(time.process_time() - t, 2),
                    int(rms * 100),
                )
            )
            print("K: {}, ωn: {}, ζ: {}".format(round(K, 2), round(ωn, 2), round(ζ, 2)))
            print("\n")
            if rms > r["rms"]:
                raise ValueError("The learing rate L is to large" "\n")
            r["rms"] = rms

    r["K"] = round(K, 2)
    r["ωn"] = round(ωn, 2)
    r["ζ"] = round(ζ, 2)
    r["tf"] = [
        round(r["K"] * r["ωn"] ** 2, 2),
        [1, round(2 * r["ζ"] * r["ωn"], 2), round(r["ωn"] ** 2, 2)],
    ]

    return r