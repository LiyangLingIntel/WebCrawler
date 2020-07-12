import re


def category_to_suffix(cate_name):
    cate_name = cate_name.lower()
    if cate_name == 'intel-soc-fpga-embedded':
        return cate_name[6:] + '-development-suite'
    elif cate_name.startswith('intel'):
        return cate_name[6:]
    else:
        return cate_name
