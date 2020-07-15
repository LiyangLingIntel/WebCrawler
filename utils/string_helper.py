import re
from web_crawler.settings import CATEGORY_choices


def category_to_suffix(cate_name):
    if cate_name == 'intel-soc-fpga-embedded':
        return cate_name[6:] + '-development-suite'
    elif cate_name == 'application-acceleration-with':
        return 'application-acceleration-fpgas'
    elif cate_name == 'intel-fpga-software-installation':
        return cate_name[6:] + '-licensing'
    elif cate_name == 'fpga-soc-and-cpld-boards-and':
        return 'fpga-soc-cpld-boards-kits'
    elif cate_name == 'intel-trusted-execution':
        return cate_name[6:] + 'technology'
    elif cate_name == 'intel-embree-ray-tracing-kernels':
        return 'embree'
    elif cate_name == CATEGORY_choices['software'][7]:
        return 'media-products'
    elif cate_name == CATEGORY_choices['software'][8]:
        return cate_name[6:] + '-analyzers'
    elif cate_name.startswith('Intel'):
        return cate_name[6:]
    return cate_name.lower()


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
