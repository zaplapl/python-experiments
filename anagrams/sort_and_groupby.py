from itertools import groupby

key_func = lambda x: sorted(x.lower().replace("'", "").replace("\n", ""))

word_list = sorted(
    (line for line in open("./wordlist.txt", "r").readlines()), key=key_func
)
grouped = groupby(word_list, key=key_func)
with open("./grouped_grams", "w") as outfile:
    for key, group in grouped:
        group_list = [item.replace("\n", "") for item in list(group)]
        if len(group_list) > 1:
            outfile.write(" ".join(group_list) + "\n")
