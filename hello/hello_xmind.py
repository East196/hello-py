from xmindparser import xmind_to_dict

d = xmind_to_dict('your.xmind')
print(d)

for target_list in d:
    pass