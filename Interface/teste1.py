import matplotlib.pyplot as plt

sinal = [
    2.6242, 2.9520, 3.5850, 3.3723, 3.5682, 3.7157, 3.7942, 4.2733, 4.2022, 4.5370,
    4.0371, 4.1663, 4.0309, 3.9905, 3.1460, 3.2307, 2.4408, 2.6788, 1.9924, 1.9715,
    1.8410, 0.6633, 1.0104, 1.3747, 0.6818, 0.8329, 1.0726, 0.8716, 0.9811, 1.5295,
    1.2092, 1.7890, 1.9146, 2.4159, 2.6029, 2.8258, 2.8948, 3.3058, 4.0191, 4.1735,
    4.2451, 3.8471, 4.5970, 3.8423, 3.5241, 4.0714, 3.4436, 3.2899, 2.8236, 2.5919
]

amostras = range(1, len(sinal) + 1)

plt.figure(figsize=(12, 6))
plt.plot(amostras, sinal, 'o-', linewidth=2, markersize=5)

plt.title('Sinal Amostrado')
plt.xlabel('Amostra')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.xlim(1, 50)

plt.tight_layout()
plt.show()