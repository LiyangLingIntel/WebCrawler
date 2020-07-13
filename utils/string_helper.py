import re


def category_to_suffix(cate_name):
    cate_name = cate_name.lower()
    if cate_name == 'intel-soc-fpga-embedded':
        return cate_name[6:] + '-development-suite'
    elif cate_name == 'application-acceleration-with':
        return 'application-acceleration-fpgas'
    elif cate_name.startswith('intel'):
        return cate_name[6:]
    else:
        return cate_name


def remove_blank(content):
    """
    remove \t \n and multiple space in content
    :param content:
    :return:
    """
    content = content.strip()
    if content:
        result = re.subn(r'\s+', ' ', content)[0]
        return result + ' '
    else:
        return content  # empty string
