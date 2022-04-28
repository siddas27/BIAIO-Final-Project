import json
import matplotlib.pyplot as plt
import pandas as pd

problems = {
    "Sphere",
    "Rosenbrock",
    "Rastrigin"}

dic = {}
for prob in problems:
    df = pd.read_json(f'{prob}_abc.json')
    # print(df.describe())
    # df = df.loc[:100,:]
    # print('shape',df.shape)
    df.loc[:, 'Mean'] = df.mean(axis=1)
    df.loc[:, 'Max'] = df.max(axis=1)
    df.loc[:, 'Min'] = df.min(axis=1)
    df.loc[:, 'Std'] = df.std(axis=1)

    fitness = df['Mean']
    itr = range(len(fitness))
    print(prob)
    print(f"Mean:{fitness[24000]}")
    print(f"Max:{df['Max'][24000]}")
    print(f"Min:{df['Min'][24000]}")
    print(f"Std:{df['Std'][:10]}")
    dic[prob] = fitness.to_list()
    for j in ['Max', 'Min', 'Mean']:
        plt.plot(itr, df[j], label=j)

    plt.xlabel('# function evaluations')
    plt.ylabel('fitness')
    plt.title(f'{prob} test function')
    plt.legend()
    plt.savefig(f'{prob}_abc1.png')
    plt.show()
    plt.close()
    with open('../export/abc.json', 'w') as js:
        json.dump(dic, js)
