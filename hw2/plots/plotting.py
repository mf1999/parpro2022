from matplotlib import pyplot as plt
import numpy as np
def main():
    measurements = [[11.98417043685913, 11.747772693634033],
                    [14.204771757125854, 14.193306684494019],
                    [7.81282114982605, 7.763521909713745],
                    [7.5909082889556885, 7.685786962509155],
                    [7.717994689941406, 7.6324241161346436],
                    [7.914175510406494, 8.43274450302124],
                    [7.902430534362793, 7.9300196170806885],
                    [7.671202182769775,  8.011813402175903]]

    measurements_average = [np.mean(x) for x in measurements]

    relative_effectivness = []
    speedup = []
    for i in range(1, 9):
        tmp = measurements_average[0] / (i * measurements_average[i-1])
        relative_effectivness.append(tmp)
        tmp *= i
        speedup.append(tmp)
    plt.plot(range(1, 9), relative_effectivness, label='Actual speedup')
    #plt.plot(range(1, 9), range(1, 9), label='Ideal speedup')
    plt.title('Effectiveness graph')
    plt.xlabel('N processors')
    plt.ylabel('Relative effectiveness')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()