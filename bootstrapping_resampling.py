import random
import scorer
import json

def bootstrapping(inputs, N, n):

    sample = random.sample(inputs, N)
    bootstrapped_sample_list = [random.choices(sample, k=N) for _ in range(n)]
    return bootstrapped_sample_list

def statistical_significance_eval(inputs, baselines, golds, N):

    bootstrapped_sample_list = bootstrapping(list(range(len(inputs))), len(inputs), N)
    
    count = 0.0
    for sample in bootstrapped_sample_list:
        si = []
        sb = []
        sg = []
        for i in sample:
            si.append(inputs[i])
            sb.append(baselines[i])
            sg.append(golds[i])

        _, _, f1_0 = scorer.score(sg, sb)
        _, _, f1_1 = scorer.score(sg, si)

        if f1_1 <= f1_0:
            count += 1.0

    return count/N

origin = json.load(open('/Users/zheng/Documents/GitHub/syn-GCN/tacred/data/json/test.json'))
golds = [item["relation"] for item in origin]
inputs = [line.strip() for line in open("output_132_test_best_model_6.txt")]
baselines = [line.strip() for line in open("output_132_test_best_model_10.txt")]

print (statistical_significance_eval(inputs, baselines, golds, 10000))