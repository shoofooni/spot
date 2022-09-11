def logenst_substring(i, string, sub_string):
    if i == len(string) - 1:
        return sub_string
    if string[i] in sub_string:
        return sub_string
    return max(logenst_substring(i + 1, string, sub_string + string[i]), logenst_substring(i + 1, string, ''), key=len)


def longet_uniuqe_substring(string):
    return logenst_substring(0, string, '')

if __name__ == '__main__':
    logenst_substring("abcabcbb")
