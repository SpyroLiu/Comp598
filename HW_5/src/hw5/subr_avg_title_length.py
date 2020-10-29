def get_subr_avg_title_length(subr):
    n = len(subr)
    acc = 0
    for i in subr:
        acc = acc + len(i['data']['title'])
    return acc/n